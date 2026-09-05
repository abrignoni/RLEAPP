"""
storage_safety.py — Network-aware SQLite journal mode selection.

WAL (Write-Ahead Logging) mode significantly improves SQLite write performance,
but per the SQLite documentation it is NOT safe over network filesystems:

    https://www.sqlite.org/wal.html
    "All processes using a database must be on the same host computer; WAL does
     not work over a network filesystem."

Forensic examiners commonly write LEAPP output directly to network storage
(NAS/SAN, mapped drives, UNC paths). Enabling WAL on such a path risks database
corruption or a crashed run — unacceptable when processing evidence.

Strategy (safe by default):
  1. Only enable WAL when the output path can be AFFIRMATIVELY confirmed local.
  2. If the path is network-backed, or if we cannot determine its nature with
     confidence, stay on SQLite's default rollback journal (works everywhere).
  3. After attempting to set WAL, verify the journal mode actually took effect
     before tuning synchronous mode (WAL can silently fall back on some
     filesystems). This is the backstop suggested by @JamesHabben.
  4. Before the report is finalized, switch the database back to the delete
     (rollback) journal mode. journal_mode=WAL is persisted in the database
     header, and a WAL-mode file cannot be opened from read-only media (SQLite
     needs to create the -shm file), which would break read-only consumers such
     as the LAVA viewer (sqlite3.OPEN_READONLY) when the report is archived or
     write-blocked. Leaving WAL mode also checkpoints and removes the -wal/-shm
     sidecars, guaranteeing the .db file is complete and standalone.
"""

import os
import re
import subprocess
import sys


# Filesystem types that indicate network-backed storage on Unix-like systems.
_NETWORK_FSTYPES = frozenset({
    'nfs', 'nfs4', 'cifs', 'smbfs', 'smb3', 'fuse.sshfs', 'afpfs',
    'ncpfs', 'fuse.s3fs', 'fuse.rclone', '9p', 'fuse.glusterfs',
    'lustre', 'ceph', 'gfs', 'gfs2', 'ocfs2',
})


# Windows extended-length path prefixes. These are NOT network indicators:
#   \\?\C:\dir         -> a LOCAL drive-letter path (the \\?\ just lifts MAX_PATH)
#   \\?\UNC\srv\share  -> a UNC (network) path in extended-length form
# LEAPP prepends \\?\ to every drive-letter output path (rleapp.py), so the path
# handed to us is routinely extended-length and must be normalized before the
# leading-\\ UNC test, or a local \\?\X:\... is misread as a network share.
_EXT_PREFIX = '\\\\?\\'          # \\?\
_EXT_UNC_PREFIX = '\\\\?\\UNC\\'  # \\?\UNC\


def _strip_extended_prefix(path):
    r"""Normalize a Windows extended-length path to its plain form.

    \\?\UNC\server\share -> \\server\share   (still UNC/network)
    \\?\C:\dir           -> C:\dir            (plain drive-letter)
    Anything else is returned unchanged.
    """
    p = str(path)
    if p.startswith(_EXT_UNC_PREFIX):
        return '\\\\' + p[len(_EXT_UNC_PREFIX):]
    if p.startswith(_EXT_PREFIX):
        return p[len(_EXT_PREFIX):]
    return p


def _is_unc_path(path):
    r"""True if path is a UNC network path (\\server\share or //server/share).

    The Windows extended-length prefix is stripped first so that a local
    \\?\<drive>: path is not mistaken for UNC, while \\?\UNC\... is preserved
    as UNC.
    """
    p = _strip_extended_prefix(path)
    return p.startswith('\\\\') or p.startswith('//')


def _windows_path_is_network(path):
    """
    On Windows, determine whether path resides on a network drive.

    Returns True (network), False (local), or None (undetermined).
    Uses the Win32 API GetDriveType against the path's drive root.
    UNC paths are treated as network without an API call.
    """
    path = _strip_extended_prefix(path)
    if _is_unc_path(path):
        return True

    try:
        import ctypes

        abs_path = os.path.abspath(path)
        drive, _ = os.path.splitdrive(abs_path)
        if not drive:
            return None  # no drive letter and not UNC — undetermined
        drive_root = drive + '\\'

        # GetDriveTypeW returns:
        #   0 DRIVE_UNKNOWN, 1 DRIVE_NO_ROOT_DIR, 2 DRIVE_REMOVABLE,
        #   3 DRIVE_FIXED, 4 DRIVE_REMOTE, 5 DRIVE_CDROM, 6 DRIVE_RAMDISK
        DRIVE_REMOTE = 4
        drive_type = ctypes.windll.kernel32.GetDriveTypeW(ctypes.c_wchar_p(drive_root))
        if drive_type == DRIVE_REMOTE:
            return True
        if drive_type in (3, 2, 5, 6):  # FIXED, REMOVABLE, CDROM, RAMDISK = local
            return False
        return None  # UNKNOWN / NO_ROOT_DIR — undetermined
    except (ImportError, AttributeError, OSError, ValueError):
        return None  # API unavailable or error — undetermined


def _unix_path_is_network(path, mounts_text=None):
    """
    On Unix-like systems, determine whether path resides on a network mount by
    finding the longest matching mount point in /proc/mounts and checking its
    filesystem type.

    Returns True (network), False (local), or None (undetermined).
    mounts_text is injectable for testing.
    """
    try:
        if mounts_text is None:
            # /proc/mounts is Linux. macOS/BSD lack it; fall back to undetermined.
            if not os.path.exists('/proc/mounts'):
                return None
            with open('/proc/mounts', 'r', encoding='utf-8', errors='replace') as f:
                mounts_text = f.read()

        abs_path = os.path.abspath(path)
        best_mount = ''
        best_fstype = ''
        for line in mounts_text.strip().splitlines():
            parts = line.split()
            if len(parts) < 3:
                continue
            mount_point, fstype = parts[1], parts[2]
            if abs_path == mount_point or abs_path.startswith(mount_point.rstrip('/') + '/'):
                if len(mount_point) >= len(best_mount):
                    best_mount = mount_point
                    best_fstype = fstype

        if not best_fstype:
            return None
        return best_fstype.lower() in _NETWORK_FSTYPES
    except OSError:
        return None


# Matches macOS/BSD `mount` output lines: <device> on <mount point> (<options>)
# The first comma-separated token in <options> is the filesystem type, and
# local filesystems carry the 'local' option (the MNT_LOCAL statfs flag).
_MOUNT_LINE_RE = re.compile(r'^.+ on (.+) \(([^)]*)\)$')


def _macos_path_is_network(path, mount_text=None):
    """
    On macOS (and BSDs with the same `mount` output format), determine whether
    path resides on a network mount by finding the longest matching mount point
    in `mount` output and checking its options.

    A local filesystem advertises the 'local' option (the MNT_LOCAL flag), e.g.
        /dev/disk3s5 on /System/Volumes/Data (apfs, local, journaled, nobrowse)
    while network mounts do not, e.g.
        //user@server/share on /Volumes/share (smbfs, nodev, nosuid)

    Returns True (network), False (local), or None (undetermined).
    mount_text is injectable for testing.
    """
    try:
        if mount_text is None:
            mount_text = subprocess.run(
                ['/sbin/mount'], capture_output=True, text=True, timeout=10,
                check=True).stdout

        abs_path = os.path.abspath(path)
        best_mount = None
        best_opts = ()
        for line in mount_text.strip().splitlines():
            match = _MOUNT_LINE_RE.match(line.strip())
            if not match:
                continue
            mount_point, opts = match.group(1), match.group(2)
            if abs_path == mount_point or abs_path.startswith(mount_point.rstrip('/') + '/'):
                if best_mount is None or len(mount_point) >= len(best_mount):
                    best_mount = mount_point
                    best_opts = tuple(opt.strip() for opt in opts.split(','))

        if best_mount is None:
            return None
        if 'local' in best_opts:
            return False  # MNT_LOCAL flag — affirmatively local
        fstype = best_opts[0].lower() if best_opts else ''
        if fstype in _NETWORK_FSTYPES:
            return True
        return None  # not flagged local, type unrecognized — undetermined
    except (OSError, subprocess.SubprocessError):
        return None


def path_is_network(path):
    """
    Best-effort determination of whether path is on network-backed storage.

    Returns:
        True  — confirmed network storage
        False — confirmed local storage
        None  — could not determine (caller should treat as unsafe for WAL)
    """
    # Normalize away the Windows extended-length prefix first so a local
    # \\?\<drive>: path is not misread as UNC.
    path = _strip_extended_prefix(path)

    # UNC is network on any platform that understands it
    if _is_unc_path(path):
        return True

    if sys.platform == 'win32':
        return _windows_path_is_network(path)
    if sys.platform == 'darwin':
        return _macos_path_is_network(path)
    return _unix_path_is_network(path)


def configure_lava_journal_mode(lava_db, output_path, logfunc=None):
    """
    Configure the SQLite journal mode for the LAVA database safely.

    Enables WAL only when output_path is AFFIRMATIVELY local. On network or
    undetermined paths, leaves SQLite on its default rollback journal, which is
    safe over network filesystems.

    After attempting WAL, verifies the mode actually took effect before setting
    synchronous=NORMAL (WAL can silently fall back on some filesystems).

    Args:
        lava_db:     an open sqlite3 Connection (or cursor-capable object).
        output_path: the path where the LAVA database is being written.
        logfunc:     optional logging callable (e.g. ilapfuncs.logfunc).

    Returns:
        The effective journal mode string (e.g. 'wal', 'delete').
    """
    def _log(msg):
        if logfunc:
            logfunc(msg)

    network = path_is_network(output_path)

    if network is True:
        _log('LAVA DB: output path is network-backed storage; '
             'keeping default journal mode (WAL unsafe over network per SQLite docs).')
        # Ensure a safe, network-compatible journal mode explicitly.
        effective = lava_db.execute("PRAGMA journal_mode=DELETE").fetchone()[0]
        return effective.lower()

    if network is None:
        _log('LAVA DB: could not determine if output path is local or network; '
             'defaulting to safe journal mode (no WAL).')
        effective = lava_db.execute("PRAGMA journal_mode=DELETE").fetchone()[0]
        return effective.lower()

    # network is False — confirmed local storage; safe to attempt WAL.
    effective = lava_db.execute("PRAGMA journal_mode=WAL").fetchone()[0]
    if effective.lower() == 'wal':
        # WAL took effect — NORMAL sync is safe and faster under WAL.
        lava_db.execute("PRAGMA synchronous=NORMAL")
        _log('LAVA DB: local storage confirmed; WAL journaling enabled '
             '(synchronous=NORMAL).')
    else:
        # WAL did not take effect (filesystem refused it). Leave sync at default.
        _log(f'LAVA DB: WAL requested but filesystem returned journal_mode='
             f'{effective!r}; leaving synchronous at default for safety.')
    return effective.lower()


def finalize_lava_journal_mode(lava_db, logfunc=None):
    """
    Return the LAVA database to the delete (rollback) journal mode before the
    report is finalized.

    journal_mode=WAL is persisted in the database header. If the delivered
    .db file kept it, the report database could not be opened from read-only
    media (write-blocked storage, archived/burned reports) by read-only
    consumers such as the LAVA viewer, because SQLite must create a -shm file
    to read a WAL database. Switching back to DELETE also checkpoints the WAL
    and removes the -wal/-shm sidecar files, so the .db is complete and
    standalone no matter how the report folder is copied or zipped.

    Safe to call regardless of the current journal mode.

    Args:
        lava_db: an open sqlite3 Connection.
        logfunc: optional logging callable (e.g. ilapfuncs.logfunc).

    Returns:
        The effective journal mode string (expected 'delete').
    """
    def _log(msg):
        if logfunc:
            logfunc(msg)

    current = lava_db.execute("PRAGMA journal_mode").fetchone()[0].lower()
    if current != 'wal':
        return current

    # Flush the write-ahead log into the main database file, then leave WAL
    # mode (which resets the header and deletes the -wal/-shm sidecars).
    lava_db.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    effective = lava_db.execute("PRAGMA journal_mode=DELETE").fetchone()[0].lower()
    if effective == 'delete':
        _log('LAVA DB: WAL checkpointed and journal mode reset to DELETE; '
             'database file is complete and standalone.')
    else:
        _log(f'LAVA DB: could not leave WAL mode (journal_mode={effective!r}); '
             f'keep the -wal/-shm files with the database if copying the report.')
    return effective

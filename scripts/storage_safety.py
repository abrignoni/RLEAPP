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
"""

import os
import sys


# Filesystem types that indicate network-backed storage on Unix-like systems.
_NETWORK_FSTYPES = frozenset({
    'nfs', 'nfs4', 'cifs', 'smbfs', 'smb3', 'fuse.sshfs', 'afpfs',
    'ncpfs', 'fuse.s3fs', 'fuse.rclone', '9p', 'fuse.glusterfs',
    'lustre', 'ceph', 'gfs', 'gfs2', 'ocfs2',
})


def _is_unc_path(path):
    """A path beginning with \\\\ or // is a UNC network path (Windows/SMB)."""
    p = str(path)
    return p.startswith('\\\\') or p.startswith('//')


def _windows_path_is_network(path):
    """
    On Windows, determine whether path resides on a network drive.

    Returns True (network), False (local), or None (undetermined).
    Uses the Win32 API GetDriveType against the path's drive root.
    UNC paths are treated as network without an API call.
    """
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
    except Exception:
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
    except Exception:
        return None


def path_is_network(path):
    """
    Best-effort determination of whether path is on network-backed storage.

    Returns:
        True  — confirmed network storage
        False — confirmed local storage
        None  — could not determine (caller should treat as unsafe for WAL)
    """
    # UNC is network on any platform that understands it
    if _is_unc_path(path):
        return True

    if sys.platform == 'win32':
        return _windows_path_is_network(path)
    else:
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

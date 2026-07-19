__artifacts_v2__ = {
    "synchronoss_messages": {
        "name": "Synchronoss - Messages (SMS and MMS)",
        "description": "Parses SMS and MMS messages from Synchronoss/Verizon Cloud legal return daily CSVs",
        "author": "@OneSixForensics",
        "creation_date": "2026-06-24",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Synchronoss",
        "notes": "Located at <LCID>/messages/YYYYMMDD.csv. All daily CSVs are merged.",
        "paths": ('*/messages/2*.csv',),
        "output_types": "standard",
        "html_columns": ['Recipients'],
        "artifact_icon": "message",
    },
    "synchronoss_calls": {
        "name": "Synchronoss - Calls",
        "description": "Parses call records from Synchronoss/Verizon Cloud legal return daily CSVs",
        "author": "@OneSixForensics",
        "creation_date": "2026-06-24",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Synchronoss",
        "notes": "Located at <LCID>/messages/YYYYMMDD.csv. All daily CSVs are merged.",
        "paths": ('*/messages/2*.csv',),
        "output_types": "standard",
        "artifact_icon": "phone",
    },
    "synchronoss_mms_received": {
        "name": "Synchronoss - MMS Media Received",
        "description": "Parses received MMS media with inline display, linked to message CSV metadata",
        "author": "@OneSixForensics",
        "creation_date": "2026-06-24",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Synchronoss",
        "notes": "Media at <LCID>/messages/attachments/mms/in/YYYY-MM-DD/",
        "paths": (
            '*/messages/2*.csv',
            '*/messages/attachments/mms/in/*/*',
        ),
        "output_types": "standard",
        "html_columns": ['Recipients'],
        "artifact_icon": "photo",
    },
    "synchronoss_mms_sent": {
        "name": "Synchronoss - MMS Media Sent",
        "description": "Parses sent MMS media with inline display, linked to message CSV metadata",
        "author": "@OneSixForensics",
        "creation_date": "2026-06-24",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Synchronoss",
        "notes": "Media at <LCID>/messages/attachments/mms/out/YYYY-MM-DD/",
        "paths": (
            '*/messages/2*.csv',
            '*/messages/attachments/mms/out/*/*',
        ),
        "output_types": "standard",
        "html_columns": ['Recipients'],
        "artifact_icon": "photo",
    },
    "synchronoss_mms_unlinked": {
        "name": "Synchronoss - MMS Folder Media (Unlinked)",
        "description": "Media physically present in the MMS attachment folders that is not "
                       "tied to a specific message (e.g. extensionless '0' files referenced "
                       "only via SMIL placeholders). Surfaced so no sent/received media is lost.",
        "author": "@OneSixForensics",
        "creation_date": "2026-06-24",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Synchronoss",
        "notes": "Media at <LCID>/messages/attachments/mms/(in|out)/YYYY-MM-DD/ whose filename "
                 "is never referenced by a real-extension token in any message CSV. Dated by "
                 "the folder (upload date per Synchronoss FAQ); not attributed to a message. "
                 "Extensionless files are typed and rendered inline via magic-byte detection.",
        "paths": (
            '*/messages/2*.csv',
            '*/messages/attachments/mms/in/*/*',
            '*/messages/attachments/mms/out/*/*',
        ),
        "output_types": "standard",
        "artifact_icon": "folder",
    },
    "synchronoss_contacts": {
        "name": "Synchronoss - Contacts",
        "description": "Parses contacts from Synchronoss/Verizon Cloud JSON contacts file",
        "author": "@OneSixForensics",
        "creation_date": "2026-06-24",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Synchronoss",
        "notes": "Located alongside the zip as contacts_YYYYMMDD.txt (JSON format)",
        "paths": ('*contacts_*.txt',),
        "output_types": "standard",
        "artifact_icon": "users",
    },
    "synchronoss_dv_uploads": {
        "name": "Synchronoss - DV Access Log Uploads",
        "description": "Parses file upload events from Synchronoss DV access logs — rows with file checksums",
        "author": "@OneSixForensics",
        "creation_date": "2026-06-24",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Synchronoss",
        "notes": "Located alongside the zip as 'Dv Access logs mdn <LCID> <Month> <Year>.csv'. "
                 "Upload rows contain a SHA-256 checksum in the querystring. "
                 "Cross-reference checksums with CyberTip file hashes.",
        "paths": ('*[Dd][Vv] [Aa]ccess [Ll]ogs*.csv',),
        "output_types": "standard",
        "artifact_icon": "upload",
    },
    "synchronoss_dv_sync": {
        "name": "Synchronoss - DV Access Log Sync Events",
        "description": "Parses sync/conflict-resolve events from Synchronoss DV access logs",
        "author": "@OneSixForensics",
        "creation_date": "2026-06-24",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Synchronoss",
        "notes": "Located alongside the zip as 'Dv Access logs mdn <LCID> <Month> <Year>.csv'. "
                 "Sync rows show device activity without a specific file upload.",
        "paths": ('*[Dd][Vv] [Aa]ccess [Ll]ogs*.csv',),
        "output_types": "standard",
        "artifact_icon": "refresh",
    },
    "synchronoss_vzmobile": {
        "name": "Synchronoss - VZMOBILE Device Backup",
        "description": "Parses and displays media files from VZMOBILE device cloud backup folder",
        "author": "@OneSixForensics",
        "creation_date": "2026-06-24",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Synchronoss",
        "notes": "Located at <LCID>/VZMOBILE/YYYY-MM-DD/<device name>/. "
                 "Files are PNG device backups. Date folder = upload date per Synchronoss FAQ.",
        "paths": ('*/VZMOBILE/*/*/**',),
        "output_types": "standard",
        "artifact_icon": "device-mobile",
    },
}

import csv
import json
import os
import re
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, logfunc, check_in_media, convert_unix_ts_to_utc
from scripts.html_safe import safe_join


def _register_media(file_path, name):
    """Register a media file for inline HTML + LAVA rendering, returning its
    media-reference id (or '' if it can't be registered).

    Thin wrapper over the framework's check_in_media so the call sites read
    cleanly and never propagate a None into a media cell.
    """
    return check_in_media(file_path, name) or ''


def _detect_media_type(filepath):
    """
    Detect media type from file header magic bytes — no external libraries.
    Returns a file extension string (e.g. '.jpg') or None if not a
    recognised media format. Used only for the informative 'Detected Type'
    column on extensionless files; inline rendering is handled by the
    framework's media system (check_in_media + guess_mime).
    """
    try:
        with open(filepath, 'rb') as fh:
            h = fh.read(32)
    except OSError:
        return None

    if len(h) < 4:
        return None

    if h[:3] == b'\xff\xd8\xff':                   return '.jpg'   # JPEG
    if h[:8] == b'\x89PNG\r\n\x1a\n':              return '.png'   # PNG
    if h[:6] in (b'GIF87a', b'GIF89a'):            return '.gif'   # GIF
    if h[:2] == b'BM':                              return '.bmp'   # BMP
    if h[:4] == b'RIFF' and h[8:12] == b'WEBP':    return '.webp'  # WebP
    if h[4:8] == b'ftyp':
        brand = h[8:12]
        if brand == b'M4A ':                        return '.m4a'   # M4A audio
        if brand[:3] in (b'3gp', b'3g2'):           return '.3gp'   # 3GP video
        return '.mp4'                                                # MP4/MOV
    if h[:5] == b'#!AMR':                           return '.amr'   # AMR audio
    if h[:4] == b'\x1aE\xdf\xa3':                  return '.mkv'   # MKV/WebM
    if h[:4] == b'OggS':                            return '.ogg'   # OGG
    if h[:3] == b'ID3':                             return '.mp3'   # MP3 (ID3)
    if h[:2] in (b'\xff\xfb', b'\xff\xf3', b'\xff\xf2'): return '.mp3'  # MP3
    if h[:4] == b'fLaC':                            return '.flac'  # FLAC
    return None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _clean_path(path):
    """Strip Windows extended-length path prefix if present (\\\\?\\)."""
    p = str(path)
    if p.startswith('\\\\?\\'):
        return p[4:]
    return p


def _ts_utc(value):
    """
    Convert a source timestamp string to an aware-UTC datetime.

    Handles ISO-8601 forms ('2025-12-01 18:22:33', 'T' separator, fractional
    seconds, trailing 'Z' or ' UTC', explicit offsets) and bare epoch
    seconds/milliseconds. Values in any other format are returned unchanged
    as plain text rather than guessed at — never fabricate a timestamp.
    """
    if not value or not isinstance(value, str):
        return value
    text = value.strip()
    if text.endswith(' UTC'):
        text = text[:-4].strip()
    if text.endswith('Z'):
        text = text[:-1] + '+00:00'
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        if text.isdigit() and len(text) in (10, 13):
            return convert_unix_ts_to_utc(text)
        return value
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _dedupe(files_found):
    """
    Yield (raw_path, cleaned_path) for each unique real file in files_found.
    Case-insensitive globbing and overlapping patterns can surface the same
    file more than once; os.path.realpath collapses those duplicates.
    """
    seen = set()
    for raw in files_found:
        cf = _clean_path(str(raw))
        real = os.path.realpath(cf)
        if real in seen:
            continue
        seen.add(real)
        yield raw, cf


def _open_csv(file_found):
    """Return (headers, rows) for a CSV file, stripping BOM if present."""
    rows = []
    headers = []
    try:
        with open(file_found, 'r', encoding='utf-8-sig', errors='replace') as f:
            reader = csv.DictReader(f)
            if reader.fieldnames:
                headers = [h.strip() for h in reader.fieldnames]
            for row in reader:
                rows.append({k.strip(): v for k, v in row.items()})
    except (OSError, csv.Error, UnicodeError) as e:
        logfunc(f'Synchronoss CSV read error ({file_found}): {e}')
    return headers, rows


def _parse_all_message_csvs(context):
    """
    Read all daily message CSVs and return a list of row dicts.
    Each row gets injected 'source_file' (extraction-relative, for display
    columns) and 'source_path' (cleaned on-disk path) keys.
    Only processes files matching the YYYYMMDD.csv naming pattern.
    """
    all_rows = []
    pattern = re.compile(r'\d{8}\.csv$', re.IGNORECASE)
    for _, cf in _dedupe(context.get_files_found()):
        if not pattern.search(os.path.basename(cf)):
            continue
        rel = context.get_relative_path(cf)
        _, rows = _open_csv(cf)
        for row in rows:
            row['source_file'] = rel
            row['source_path'] = cf
        all_rows.extend(rows)
    # Sort by Date ascending
    all_rows.sort(key=lambda r: r.get('Date', ''))
    return all_rows


def _extract_checksum(querystring):
    """Extract SHA-256 checksum from DV log querystring if present."""
    m = re.search(r'checksum=([a-f0-9]{64})', querystring, re.IGNORECASE)
    return m.group(1) if m else ''


def _extract_user_ip(remoteipaddress):
    """
    The remoteipaddress field contains a comma-separated list:
    the first entry is the user's actual IP; subsequent entries are CDN IPs.
    Returns (user_ip, cdn_ips_string).
    """
    if not remoteipaddress or remoteipaddress.strip() in ('-', ''):
        return '', ''
    parts = [p.strip() for p in remoteipaddress.split(',')]
    user_ip = parts[0]
    cdn_ips = ', '.join(parts[1:]) if len(parts) > 1 else ''
    return user_ip, cdn_ips


# ---------------------------------------------------------------------------
# Artifact functions
#
# Each is decorated with @artifact_processor and returns
# (data_headers, data_list, source_path). The framework writes HTML, TSV,
# timeline, and the LAVA database from that single return — including inline
# media rendering for columns typed ('<name>', 'media'), whose cells hold a
# media reference id from check_in_media().
# ---------------------------------------------------------------------------

@artifact_processor
def synchronoss_messages(context):
    """
    messages/YYYYMMDD.csv — SMS and MMS rows only (Type = sms or mms).
    All daily CSVs merged and sorted by date.
    """
    data_headers = (
        ('Date (UTC)', 'datetime'), 'Type', 'Direction', ('Sender', 'phonenumber'),
        'Recipients', 'Body', 'Attachments', 'Message ID', 'Source File'
    )
    data_list = []
    source_path = ''
    for row in _parse_all_message_csvs(context):
        msg_type = row.get('Type', '').lower()
        if msg_type not in ('sms', 'mms'):
            continue
        source_path = row.get('source_path', '')
        recipients_fmt = safe_join(
            r.strip() for r in row.get('Recipients', '').split(';') if r.strip()
        )
        data_list.append((
            _ts_utc(row.get('Date', '')),
            row.get('Type', ''),
            row.get('Direction', ''),
            row.get('Sender', ''),
            recipients_fmt,
            row.get('Body', ''),
            row.get('Attachments', ''),
            row.get('Message ID', ''),
            row.get('source_file', ''),
        ))

    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def synchronoss_calls(context):
    """
    messages/YYYYMMDD.csv — Call records only (Type = call).
    All daily CSVs merged and sorted by date.

    Present the source CSV's Sender/Recipients fields verbatim rather than
    re-interpreting them as caller/account — the meaning flips with Direction
    (inbound: Sender = remote party; outbound: Recipients = dialed number),
    so faithful labels avoid mislabeling the dialed number as an "account".
    """
    data_headers = (
        ('Date (UTC)', 'datetime'), 'Direction', ('Sender', 'phonenumber'),
        'Recipients', 'Message ID', 'Source File'
    )
    data_list = []
    source_path = ''
    for row in _parse_all_message_csvs(context):
        if row.get('Type', '').lower() != 'call':
            continue
        source_path = row.get('source_path', '')
        data_list.append((
            _ts_utc(row.get('Date', '')),
            row.get('Direction', ''),
            row.get('Sender', ''),
            row.get('Recipients', ''),
            row.get('Message ID', ''),
            row.get('source_file', ''),
        ))

    return data_headers, data_list, context.get_relative_path(source_path)


def _synchronoss_mms_media(context, direction):
    """
    Shared implementation for MMS received and sent media artifacts.
    direction: 'in' or 'out'. Returns (data_headers, data_list, source_path).
    """
    # Separate CSVs from media files. Media lookups keep the RAW files_found
    # path because check_in_media resolves against the seeker's files_found /
    # file_infos by that exact string.
    csv_rows = []
    media_lookup = {}  # basename -> a raw full path (may be overwritten if non-unique)
    name_paths = {}    # basename -> [all raw full paths with that name across folders]

    csv_pattern = re.compile(r'\d{8}\.csv$', re.IGNORECASE)
    mms_path_fragment = f'/mms/{direction}/'

    for raw, cf in _dedupe(context.get_files_found()):
        basename = os.path.basename(cf)
        if csv_pattern.search(basename):
            rel = context.get_relative_path(cf)
            _, rows = _open_csv(cf)
            for row in rows:
                row['source_file'] = rel
                row['source_path'] = cf
            csv_rows.extend(rows)
        elif mms_path_fragment in cf.replace('\\', '/'):
            media_lookup[basename] = raw
            name_paths.setdefault(basename, []).append(raw)

    csv_rows.sort(key=lambda r: r.get('Date', ''))

    # Build date-folder to date string mapping from media paths
    # Path: .../mms/in/2025-12-01/filename
    def _date_from_path(path):
        parts = _clean_path(path).replace('\\', '/').split('/')
        for i, part in enumerate(parts):
            if part in ('in', 'out') and i + 1 < len(parts):
                return parts[i + 1]
        return ''

    # Build lookup: date_folder -> {filename -> raw_full_path}
    date_media = {}
    for fname, fpath in media_lookup.items():
        date_folder = _date_from_path(fpath)
        date_media.setdefault(date_folder, {})[fname] = fpath

    data_headers = (
        ('Date (UTC)', 'datetime'), 'Direction', ('Sender', 'phonenumber'),
        'Recipients', ('Media', 'media'), 'Filename', 'Link Status',
        'Message ID', 'Source File'
    )
    data_list = []
    source_path = ''

    for row in csv_rows:
        if row.get('Type', '').lower() != 'mms':
            continue
        if row.get('Direction', '').lower() != direction:
            continue

        source_path = row.get('source_path', '')
        msg_date = row.get('Date', '')
        date_folder = msg_date[:10] if msg_date else ''   # YYYY-MM-DD
        folder_files = date_media.get(date_folder, {})

        recipients_fmt = safe_join(
            r.strip() for r in row.get('Recipients', '').split(';') if r.strip()
        )

        # Resolve every attachment token against the ACTUAL media files on disk
        # rather than inferring from the token name. A token is real media iff it
        # maps to a file present in the message's own date folder (preferred), or
        # in some other folder when its name is globally unique. This recovers
        # extensionless "0" media (referenced as a bare token) and avoids linking
        # a non-unique name (image000000.jpg, "0") to a wrong-date file. Tokens
        # whose media file is absent are surfaced — per Synchronoss, flagged files
        # are quarantined out of the daily folder.
        for tok in (t.strip() for t in row.get('Attachments', '').split(';') if t.strip()):
            low = tok.lower()
            ext = os.path.splitext(low)[1]
            # SMIL / text layout descriptors are never media files.
            if low.startswith(('smil', 'null', 'text0')) or ext in ('.smi', '.sml', '.txt'):
                continue
            # Bare-numeric / extensionless tokens (e.g. the "0" in "null.smi;0;1")
            # are SMIL placeholders, not reliable file references: in a live test
            # return the extensionless "0" media files were referenced ONLY via that
            # placeholder, and some days had two such rows for a single "0" file —
            # so token-linking them would fabricate a message↔file attribution.
            # Only tokens carrying a real media extension are linked.
            if not ext:
                continue

            fpath = folder_files.get(tok)
            candidates = []
            if not fpath:
                candidates = name_paths.get(tok, [])
                if len(candidates) == 1:
                    fpath = candidates[0]

            if fpath:
                media_cell = _register_media(fpath, tok)
                link_status = 'linked' if media_cell else (
                    'matched on disk but media registration failed — review')
            elif len(candidates) > 1:
                media_cell = ''
                link_status = (f'not linked — name present in {len(candidates)} '
                               f'date folders, none matching message date '
                               f'{date_folder or "?"}; manual review required')
            else:
                # Media-looking token with no file present — likely quarantined/removed.
                media_cell = ''
                link_status = ('referenced — file not in daily folder; '
                               'possibly quarantined/removed')

            data_list.append((
                _ts_utc(msg_date),
                row.get('Direction', ''),
                row.get('Sender', ''),
                recipients_fmt,
                media_cell,
                tok,
                link_status,
                row.get('Message ID', ''),
                row.get('source_file', ''),
            ))

    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def synchronoss_mms_received(context):
    """MMS media received (direction 'in') — see _synchronoss_mms_media."""
    return _synchronoss_mms_media(context, direction='in')


@artifact_processor
def synchronoss_mms_sent(context):
    """MMS media sent (direction 'out') — see _synchronoss_mms_media."""
    return _synchronoss_mms_media(context, direction='out')


@artifact_processor
def synchronoss_mms_unlinked(context):
    """
    Media files present in the MMS attachment folders that are NOT referenced by
    a real-extension token in any message CSV — chiefly the extensionless "0"
    files, which appear in the CSV only via the 'null.smi;0;1' SMIL placeholder
    and therefore cannot be reliably tied to a specific message. Listed here so
    no sent/received media is lost, dated by the folder (upload date) but not
    attributed to a message. Extensionless files are typed (Detected Type) and
    rendered inline via the framework's magic-byte mime detection.

    'Upload Date' is a bare YYYY-MM-DD folder name with no time component, so
    it stays a plain-text column — typing it 'datetime' would fabricate a
    midnight timestamp.
    """
    csv_pattern = re.compile(r'\d{8}\.csv$', re.IGNORECASE)
    media_re = re.compile(r'/mms/(in|out)/([^/]+)/([^/]+)$', re.IGNORECASE)

    referenced = set()   # real-extension filenames referenced by any MMS message
    media = []           # (direction, date_folder, basename, raw_full_path, cleaned_path)

    for raw, cf in _dedupe(context.get_files_found()):
        norm = cf.replace('\\', '/')
        basename = os.path.basename(cf)
        if csv_pattern.search(basename):
            _, rows = _open_csv(cf)
            for row in rows:
                if (row.get('Type', '') or '').lower() != 'mms':
                    continue
                for tok in (t.strip() for t in (row.get('Attachments') or '').split(';') if t.strip()):
                    low = tok.lower()
                    ext = os.path.splitext(low)[1]
                    if low.startswith(('smil', 'null', 'text0')) or ext in ('.smi', '.sml', '.txt'):
                        continue
                    if ext:  # a real-extension token names an actual media file
                        referenced.add(tok)
        else:
            m = media_re.search(norm)
            if m:
                media.append((m.group(1).lower(), m.group(2), m.group(3), raw, cf))

    data_headers = (
        'Upload Date', 'Direction', ('Media', 'media'),
        'Filename', 'Detected Type', 'Source File'
    )
    data_list = []
    source_path = ''
    for direction, date_folder, basename, raw, cf in media:
        if basename in referenced:
            continue  # already shown in the message-linked MMS report
        source_path = cf
        ext = os.path.splitext(basename)[1].lower()
        media_cell = _register_media(raw, basename)
        if ext:
            detected = ext
        else:
            det = _detect_media_type(cf)
            detected = (det + ' (by magic bytes)') if det else 'unknown (magic bytes)'
        data_list.append((date_folder, direction, media_cell, basename, detected,
                          context.get_relative_path(cf)))

    data_list.sort(key=lambda r: (r[1], r[0], r[3]))

    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def synchronoss_contacts(context):
    """
    contacts_YYYYMMDD.txt — JSON format.
    Schema: {"contacts": {"itemcount": N, "contact": [...]}}
    Each contact has: firstname, lastname, source, created, deleted,
    itemguid, incaseofemergency, favorite, tel:[{type, number}]
    """
    data_headers = (
        'First Name', 'Last Name', ('Phone Number', 'phonenumber'), 'Phone Type',
        ('Created', 'datetime'), ('Deleted', 'datetime'), 'Source',
        'ICE', 'Favorite', 'Item GUID', 'Source File'
    )
    data_list = []
    source_path = ''

    for _, cf in _dedupe(context.get_files_found()):
        basename = os.path.basename(cf).lower()
        if 'contacts_' not in basename or not basename.endswith('.txt'):
            continue
        source_path = cf
        rel = context.get_relative_path(cf)
        try:
            with open(cf, 'r', encoding='utf-8-sig', errors='replace') as fh:
                data = json.load(fh)
        except (OSError, ValueError, UnicodeError) as e:
            logfunc(f'Synchronoss contacts JSON parse error ({cf}): {e}')
            continue

        contacts = data.get('contacts', {}).get('contact', [])
        for contact in contacts:
            first = contact.get('firstname', '')
            last = contact.get('lastname', '')
            created_raw = contact.get('created', '')
            deleted_raw = contact.get('deleted', '')
            created = _ts_utc(str(created_raw)) if created_raw not in (None, '') else ''
            deleted = _ts_utc(str(deleted_raw)) if deleted_raw not in (None, '') else ''
            source = contact.get('source', '')
            ice = str(contact.get('incaseofemergency', ''))
            favorite = str(contact.get('favorite', ''))
            guid = contact.get('itemguid', '')

            tel_list = contact.get('tel', [])
            if tel_list:
                for tel in tel_list:
                    data_list.append((
                        first, last,
                        tel.get('number', ''),
                        tel.get('type', ''),
                        created, deleted, source, ice, favorite, guid,
                        rel,
                    ))
            else:
                # Contact with no phone number — still surface it
                data_list.append((
                    first, last, '', '', created, deleted,
                    source, ice, favorite, guid, rel,
                ))

    return data_headers, data_list, context.get_relative_path(source_path)


def _parse_dv_log(context):
    """
    Parse all DV access log CSVs and return a list of row dicts.
    Handles quoted remoteipaddress fields with multiple IPs.
    Extracts user IP vs CDN IPs and checksum from querystring.
    """
    all_rows = []
    for _, cf in _dedupe(context.get_files_found()):
        if 'dv access' not in os.path.basename(cf).lower():
            continue
        rel = context.get_relative_path(cf)
        _, rows = _open_csv(cf)
        for row in rows:
            row['source_file'] = rel
            row['source_path'] = cf
            user_ip, cdn_ips = _extract_user_ip(row.get('remoteipaddress', ''))
            row['user_ip'] = user_ip
            row['cdn_ips'] = cdn_ips
            row['checksum'] = _extract_checksum(row.get('querystring', ''))
        all_rows.extend(rows)
    all_rows.sort(key=lambda r: r.get('server_ts', ''))
    return all_rows


@artifact_processor
def synchronoss_dv_uploads(context):
    """
    DV Access Log — upload events only (rows with a file checksum).
    These are the forensically significant rows — each checksum identifies
    a specific file uploaded to the cloud. Cross-reference with CyberTip
    file hashes to identify reported content.
    """
    data_headers = (
        ('Timestamp (UTC)', 'datetime'), 'User IP', 'CDN IPs', 'Device',
        'File Checksum (SHA-256)', 'LCID', 'Source File'
    )
    data_list = []
    source_path = ''
    for row in _parse_dv_log(context):
        if not row.get('checksum'):
            continue
        source_path = row.get('source_path', '')
        data_list.append((
            _ts_utc(row.get('server_ts', '')),
            row.get('user_ip', ''),
            row.get('cdn_ips', ''),
            row.get('clientidentifier', ''),
            row.get('checksum', ''),
            row.get('lcid', ''),
            row.get('source_file', ''),
        ))

    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def synchronoss_dv_sync(context):
    """
    DV Access Log — sync/conflict-resolve events (rows without a file checksum).
    These show device activity — when the app checked in — without a specific
    file upload. Useful for establishing device usage patterns and IP history.
    """
    data_headers = (
        ('Timestamp (UTC)', 'datetime'), 'User IP', 'CDN IPs', 'Device',
        'Operation', 'LCID', 'Source File'
    )
    data_list = []
    source_path = ''
    for row in _parse_dv_log(context):
        if row.get('checksum'):
            continue  # upload rows handled by synchronoss_dv_uploads
        source_path = row.get('source_path', '')
        # Extract operation name from querystring
        qs = row.get('querystring', '')
        op = qs.lstrip('?').split('=')[0] if qs and qs != '-' else qs
        data_list.append((
            _ts_utc(row.get('server_ts', '')),
            row.get('user_ip', ''),
            row.get('cdn_ips', ''),
            row.get('clientidentifier', ''),
            op,
            row.get('lcid', ''),
            row.get('source_file', ''),
        ))

    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def synchronoss_vzmobile(context):
    """
    VZMOBILE/<date>/<device name>/<files> — device cloud backup media.

    The date folder is the upload date per Synchronoss documentation.
    Files are PNG device backups; some may contain CSAM. Rendered inline with
    upload date and device name context via the framework's media system.

    'Upload Date' is a bare YYYY-MM-DD folder name with no time component, so
    it stays a plain-text column — typing it 'datetime' would fabricate a
    midnight timestamp.
    """
    data_headers = (
        'Upload Date', 'Device', ('Media', 'media'),
        'Filename', 'Source File'
    )
    data_list = []
    source_path = ''

    for raw, cf in _dedupe(context.get_files_found()):
        norm = cf.replace('\\', '/')

        # Extract date and device from path: .../VZMOBILE/<date>/<device>/<file>
        m = re.search(r'/VZMOBILE/(\d{4}-\d{2}-\d{2})/([^/]+)/([^/]+)$',
                      norm, re.IGNORECASE)
        if not m:
            continue

        upload_date = m.group(1)
        device = m.group(2)
        filename = m.group(3)
        source_path = cf

        media_cell = _register_media(raw, filename)

        data_list.append((
            upload_date,
            device,
            media_cell,
            filename,
            context.get_relative_path(cf),
        ))

    # Sort by upload date then device then filename
    data_list.sort(key=lambda r: (r[0], r[1], r[3]))

    return data_headers, data_list, context.get_relative_path(source_path)

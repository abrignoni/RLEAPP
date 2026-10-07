__artifacts_v2__ = {
    "synchronoss_messages": {
        "name": "Synchronoss - Messages (SMS and MMS)",
        "description": "Parses SMS and MMS messages from Synchronoss/Verizon Cloud legal return daily CSVs",
        "author": "@OneSixForensics, @AlexisBrignoni, Codex",
        "creation_date": "2026-06-24",
        "last_update_date": "2026-10-04",
        "requirements": "none",
        "category": "Synchronoss",
        "notes": 'Mixed time columns use text storage and do not populate timeline/date filters. Daily CSV SMS/MMS rows. Explicit offsets are converted to UTC; zone-less and unsupported date values remain text.',
        "paths": ('*/messages/2*.csv',),
        "output_types": "standard",
        "html_columns": ['Recipients'],
        "artifact_icon": "message",
    },
    "synchronoss_calls": {
        "name": "Synchronoss - Calls",
        "description": "Parses call records from Synchronoss/Verizon Cloud legal return daily CSVs",
        "author": "@OneSixForensics, @AlexisBrignoni, Codex",
        "creation_date": "2026-06-24",
        "last_update_date": "2026-10-04",
        "requirements": "none",
        "category": "Synchronoss",
        "notes": 'Mixed time columns use text storage and do not populate timeline/date filters. Daily CSV rows whose Type is call. Explicit offsets are converted to UTC; zone-less and unsupported date values remain text.',
        "paths": ('*/messages/2*.csv',),
        "output_types": "standard",
        "artifact_icon": "phone",
    },
    "synchronoss_mms_received": {
        "name": "Synchronoss - MMS Media Received",
        "description": "Parses received MMS media with inline display, linked to message CSV metadata",
        "author": "@AlexisBrignoni, Codex",
        "creation_date": "2026-06-24",
        "last_update_date": "2026-10-07",
        "requirements": "none",
        "category": "Synchronoss",
        "notes": "Mixed time columns use text storage and do not populate timeline/date filters. Media at <LCID>/messages/attachments/mms/in/YYYY-MM-DD/. "
                 "Link Status records how each attachment token that carries a file extension "
                 "resolved. Tokens that start with smil, null or text0, tokens ending .smi, .sml or "
                 ".txt, and tokens with no extension get no row here. 'linked' means a file of "
                 "that name in the message's own date folder, or -- when that name occurs in only one "
                 "folder in the return -- that single copy. Attachment names repeat across date "
                 "folders in these returns (image000000.jpg and the extensionless '0' recur daily), so "
                 "where a name is in more than one folder and none is the message's own date, the "
                 "token is reported as not linked, with the number of folders carrying the name, "
                 "rather than linked to another date's copy. A Link Status that begins 'referenced' "
                 "means no file of that name was found in any mms/in/ date folder of the return; a "
                 "missing file is not on its own a finding about the file. The status does not establish "
                 "quarantine, removal or any other cause for a missing match. Direction is "
                 "constant in this artifact by construction, since the artifact selects one direction. "
                 "Original contribution credited to @OneSixForensics.",
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
        "author": "@AlexisBrignoni, Codex",
        "creation_date": "2026-06-24",
        "last_update_date": "2026-10-07",
        "requirements": "none",
        "category": "Synchronoss",
        "notes": "Mixed time columns use text storage and do not populate timeline/date filters. Media at <LCID>/messages/attachments/mms/out/YYYY-MM-DD/. "
                 "Link Status records how each attachment token that carries a file extension "
                 "resolved. Tokens that start with smil, null or text0, tokens ending .smi, .sml or "
                 ".txt, and tokens with no extension get no row here. 'linked' means a file of "
                 "that name in the message's own date folder, or -- when that name occurs in only one "
                 "folder in the return -- that single copy. Attachment names repeat across date "
                 "folders in these returns (image000000.jpg and the extensionless '0' recur daily), so "
                 "where a name is in more than one folder and none is the message's own date, the "
                 "token is reported as not linked, with the number of folders carrying the name, "
                 "rather than linked to another date's copy. A Link Status that begins 'referenced' "
                 "means no file of that name was found in any mms/out/ date folder of the return; a "
                 "missing file is not on its own a finding about the file. The status does not establish "
                 "quarantine, removal or any other cause for a missing match. Direction is "
                 "constant in this artifact by construction, since the artifact selects one direction. "
                 "Original contribution credited to @OneSixForensics.",
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
                       "only via SMIL placeholders). Lists folder media not resolved to a real-extension attachment token.",
        "author": "@OneSixForensics, @AlexisBrignoni, Codex",
        "creation_date": "2026-06-24",
        "last_update_date": "2026-10-04",
        "requirements": "none",
        "category": "Synchronoss",
        "notes": 'Mixed time columns use text storage and do not populate timeline/date filters. Files not resolved by the same direction/date-folder and unique-name rules as linked MMS media. Repeating names in other folders remain listed. Date Folder is the folder name, with no upload meaning inferred.',
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
        "author": "@OneSixForensics, @AlexisBrignoni, Codex",
        "creation_date": "2026-06-24",
        "last_update_date": "2026-10-04",
        "requirements": "none",
        "category": "Synchronoss",
        "notes": 'Mixed time columns use text storage and do not populate timeline/date filters. One row per phone number; contacts with no number receive one row. created and deleted are stored fields. Explicit offsets convert to UTC; zone-less and numeric values remain text because their time basis is not established.',
        "paths": ('*contacts_*.txt',),
        "output_types": "standard",
        "artifact_icon": "users",
    },
    "synchronoss_dv_uploads": {
        "name": "Synchronoss - DV Access Log Rows With Checksum",
        "description": "Parses Synchronoss DV access log rows whose querystring carries a file checksum",
        "author": "@OneSixForensics, @AlexisBrignoni, Codex",
        "creation_date": "2026-06-24",
        "last_update_date": "2026-10-04",
        "requirements": "openpyxl",
        "category": "Synchronoss",
        "notes": 'Mixed time columns use text storage and do not populate timeline/date filters. CSV/workbook rows selected by a 64-character hexadecimal checksum parameter, with no hash algorithm or upload meaning inferred. Explicit offsets convert to UTC; zone-less values remain text. The first IP and subsequent IPs are split by position; their roles are not established.',
        "paths": ('*[Dd][Vv]*[Aa]ccess*[Ll]ogs*.csv', '*.xlsx'),
        "output_types": "standard",
        "artifact_icon": "upload",
    },
    "synchronoss_dv_sync": {
        "name": "Synchronoss - DV Access Log Rows Without Checksum",
        "description": "Synchronoss DV access log rows that carry no file checksum, with the operation named in the querystring",
        "author": "@OneSixForensics, @AlexisBrignoni, Codex",
        "creation_date": "2026-06-24",
        "last_update_date": "2026-10-04",
        "requirements": "openpyxl",
        "category": "Synchronoss",
        "notes": 'Mixed time columns use text storage and do not populate timeline/date filters. CSV/workbook rows without the selected checksum parameter. Operation is the first querystring key; no sync event meaning is inferred. Explicit offsets convert to UTC; zone-less values remain text.',
        "paths": ('*[Dd][Vv]*[Aa]ccess*[Ll]ogs*.csv', '*.xlsx'),
        "output_types": "standard",
        "artifact_icon": "refresh",
    },
    "synchronoss_quarantined": {
        "name": "Synchronoss - Quarantined Media (CyberTip)",
        "description": "Files from the return's quarantined archive (names of the form "
                       "<container>_<sha256>.zip_file_<N>), each joined on the SHA-256 in its file "
                       "name to a Synchronoss DV access log row that carries the same checksum, "
                       "where one exists.",
        "author": "@OneSixForensics, Claude, @AlexisBrignoni, Codex",
        "creation_date": "2026-09-02",
        "last_update_date": "2026-10-04",
        "requirements": "openpyxl",
        "category": "Synchronoss",
        "notes": 'Mixed time columns use text storage and do not populate timeline/date filters. Each matching filename is hashed as a standalone file and joined to log rows by checksum. Hash Verified compares SHA-256 with the filename hash. Comparable explicit-offset times sort chronologically; other values sort as text. The first matched row is shown, without claiming it is the earliest upload. No reporting to NCMEC is inferred.',
        "paths": (
            '*[Qq]uarantined*.zip_file_*',
            '*[Dd][Vv]*[Aa]ccess*[Ll]ogs*.csv',
            '*.xlsx',
        ),
        "output_types": "standard",
        "artifact_icon": "alert-triangle",
    },
    "synchronoss_vzmobile": {
        "name": "Synchronoss - VZMOBILE Device Backup",
        "description": "Parses and displays media files from VZMOBILE device cloud backup folder",
        "author": "@OneSixForensics, @AlexisBrignoni, Codex",
        "creation_date": "2026-06-24",
        "last_update_date": "2026-10-04",
        "requirements": "none",
        "category": "Synchronoss",
        "notes": 'Mixed time columns use text storage and do not populate timeline/date filters. Files under VZMOBILE date/device folders are listed. Date Folder is the folder name, with no upload meaning inferred.',
        "paths": ('*/VZMOBILE/*/*/**',),
        "output_types": "standard",
        "artifact_icon": "device-mobile",
    },
}

import csv
import hashlib
import json
import os
import re
from datetime import datetime, timedelta, timezone

from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException

from scripts.ilapfuncs import artifact_processor, logfunc, check_in_media
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
    Detect media type from file header magic bytes; no external libraries.
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

def _rel(context, path):
    """Extraction-relative path, always with forward slashes.

    A reported path is an evidence reference and must not change with the operating
    system the tool ran on. get_relative_path yields backslashes on Windows, which
    makes the same return produce different report values, and different recorded
    test baselines, on Windows and on Linux.
    """
    return str(context.get_relative_path(path)).replace('\\', '/')


def _clean_path(path):
    """Strip Windows extended-length path prefix if present (\\\\?\\)."""
    p = str(path)
    if p.startswith('\\\\?\\'):
        return p[4:]
    return p


_CLF_MONTHS = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
               'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}

_CLF_TS_RE = re.compile(
    r'^\[?(\d{1,2})/([A-Za-z]{3})/(\d{4}):(\d{2}):(\d{2}):(\d{2})\s*([+-]\d{4})?\]?$')


def _ts_utc(value):
    """Convert only stated offsets; preserve unsupported or zone-less values."""
    if isinstance(value, datetime):
        return value.isoformat(sep=' ') if value.tzinfo is None else value.astimezone(timezone.utc)
    if not value or not isinstance(value, str):
        return value
    text = value.strip()
    clf = _CLF_TS_RE.match(text)
    if clf:
        day, mon, year, hh, mm, ss, offset = clf.groups()
        month = _CLF_MONTHS.get(mon.lower())
        if not month or not offset:
            return value
        try:
            sign = -1 if offset[0] == '-' else 1
            tz = timezone(sign * timedelta(hours=int(offset[1:3]), minutes=int(offset[3:5])))
            return datetime(int(year), month, int(day), int(hh), int(mm), int(ss),
                            tzinfo=tz).astimezone(timezone.utc)
        except ValueError:
            return value
    if text.endswith(' UTC'):
        text = text[:-4].strip() + '+00:00'
    try:
        dt = datetime.fromisoformat(text.replace('Z', '+00:00'))
    except ValueError:
        return value
    return value if dt.tzinfo is None else dt.astimezone(timezone.utc)


def _time_order(row):
    """Order comparable instants first; other values retain text ordering only."""
    value = _ts_utc(row.get('server_ts', ''))
    if isinstance(value, datetime):
        return 0, value.isoformat()
    return 1, str(value or '')


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


def _open_xlsx(file_found, accept=None):
    """
    Return (headers, rows) for the first worksheet of a workbook, mirroring
    _open_csv so both delivery shapes of the DV access log feed the same code.

    Header keys are lower-cased, and row dicts are keyed by that lower-cased
    header. A workbook written for a person to read may capitalise its column
    titles, and every read downstream is lower case; keying rows by the text as
    written let such a file pass the header check and then read back empty.

    `accept` is called with the headers before any body row is read, and a false
    result abandons the file. An unrelated workbook elsewhere in the return then
    costs one row rather than a full read of a spreadsheet that is discarded.
    """
    headers, rows = [], []
    try:
        workbook = load_workbook(file_found, read_only=True, data_only=True)
    except (OSError, InvalidFileException, KeyError, ValueError) as e:
        logfunc(f'Synchronoss workbook read error ({file_found}): {e}')
        return headers, rows
    try:
        sheet = workbook.worksheets[0]
        for i, row in enumerate(sheet.iter_rows(values_only=True)):
            if i == 0:
                headers = [str(c).strip().lower() if c is not None else '' for c in row]
                if accept is not None and not accept(headers):
                    return headers, rows
                continue
            rows.append({h: ('' if v is None else v) for h, v in zip(headers, row)})
    finally:
        workbook.close()
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
        rel = _rel(context, cf)
        _, rows = _open_csv(cf)
        for row in rows:
            row['source_file'] = rel
            row['source_path'] = cf
        all_rows.extend(rows)
    # Sort by Date ascending
    all_rows.sort(key=lambda r: r.get('Date', ''))
    return all_rows


def _extract_checksum(querystring):
    """Extract a 64-character hexadecimal checksum parameter without inferring its algorithm."""
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
# timeline, and the LAVA database from that single return; including inline
# media rendering for columns typed ('<name>', 'media'), whose cells hold a
# media reference id from check_in_media().
# ---------------------------------------------------------------------------

@artifact_processor
def synchronoss_messages(context):
    """
    messages/YYYYMMDD.csv; SMS and MMS rows only (Type = sms or mms).
    All daily CSVs merged and sorted by date.
    """
    data_headers = (
        'Date', 'Type', 'Direction', ('Sender', 'phonenumber'),
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

    return data_headers, data_list, _rel(context, source_path)


@artifact_processor
def synchronoss_calls(context):
    """
    messages/YYYYMMDD.csv; Call records only (Type = call).
    All daily CSVs merged and sorted by date.

    Present the source CSV's Sender/Recipients fields verbatim rather than
    re-interpreting them as caller/account; the meaning flips with Direction
    (inbound: Sender = remote party; outbound: Recipients = dialed number),
    so faithful labels avoid mislabeling the dialed number as an "account".
    """
    data_headers = (
        'Date', 'Direction', ('Sender', 'phonenumber'),
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

    return data_headers, data_list, _rel(context, source_path)


def _date_from_media_path(path):
    """Return the date-folder name from an MMS media path, e.g.
    '.../mms/in/2025-12-01/image000000.jpg' -> '2025-12-01'."""
    parts = _clean_path(path).replace('\\', '/').split('/')
    for i, part in enumerate(parts):
        if part in ('in', 'out') and i + 1 < len(parts):
            return parts[i + 1]
    return ''


def _index_mms_media(media_paths):
    """
    Index MMS media files, returning (name_paths, date_media):

        name_paths   basename    -> [every raw path carrying that name]
        date_media   date folder -> {basename: the raw path in that folder}

    date_media is built from every path recorded for a name, not from a dict
    holding one path per name. Names are not unique across date folders --
    image000000.jpg and the extensionless "0" are pervasive in real returns --
    so keeping a single path per name leaves only whichever one the seeker
    returned last with a date-folder entry, and a message then resolves or
    fails to resolve depending on the order the files arrive in. That order
    differs between platforms: the same return linked a message on Windows and
    reported it unlinked on Linux, and the unlinked wording named a date folder
    that did hold a copy, so the report stated something false rather than
    merely leaving it out. Indexing every path makes the result independent of
    file order; admin/test/scripts/test_synchronoss_media_order.py holds that
    invariant, because a fixture cannot -- it is the ordering that varies.
    """
    name_paths = {}
    for raw in media_paths:
        name_paths.setdefault(os.path.basename(raw), []).append(raw)
    date_media = {}
    for fname, fpaths in name_paths.items():
        for fpath in fpaths:
            date_media.setdefault(_date_from_media_path(fpath), {})[fname] = fpath
    return name_paths, date_media


def _synchronoss_mms_media(context, direction):
    """
    Shared implementation for MMS received and sent media artifacts.
    direction: 'in' or 'out'. Returns (data_headers, data_list, source_path).
    """
    # Separate CSVs from media files. Media lookups keep the RAW files_found
    # path because check_in_media resolves against the seeker's files_found /
    # file_infos by that exact string.
    csv_rows = []
    media_paths = []   # raw full paths of every media file under this direction

    csv_pattern = re.compile(r'\d{8}\.csv$', re.IGNORECASE)
    mms_path_fragment = f'/mms/{direction}/'

    for raw, cf in _dedupe(context.get_files_found()):
        basename = os.path.basename(cf)
        if csv_pattern.search(basename):
            rel = _rel(context, cf)
            _, rows = _open_csv(cf)
            for row in rows:
                row['source_file'] = rel
                row['source_path'] = cf
            csv_rows.extend(rows)
        elif mms_path_fragment in cf.replace('\\', '/'):
            media_paths.append(raw)

    csv_rows.sort(key=lambda r: r.get('Date', ''))

    name_paths, date_media = _index_mms_media(media_paths)

    data_headers = (
        'Date', 'Direction', ('Sender', 'phonenumber'),
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
        # whose media file is absent are surfaced; per Synchronoss, flagged files
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
                    'matched on disk but media registration failed; review')
            elif len(candidates) > 1:
                media_cell = ''
                link_status = (f'not linked; name present in {len(candidates)} '
                               f'date folders, none matching message date '
                               f'{date_folder or "?"}; manual review required')
            else:
                # Media-looking token with no matching file present.
                media_cell = ''
                link_status = 'referenced; file not in daily folder'

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

    return data_headers, data_list, _rel(context, source_path)


@artifact_processor
def synchronoss_mms_received(context):
    """MMS media received (direction 'in'); see _synchronoss_mms_media."""
    return _synchronoss_mms_media(context, direction='in')


@artifact_processor
def synchronoss_mms_sent(context):
    """MMS media sent (direction 'out'); see _synchronoss_mms_media."""
    return _synchronoss_mms_media(context, direction='out')


@artifact_processor
def synchronoss_mms_unlinked(context):
    """MMS folder files not resolved to a message token. Date Folder is stored text."""
    csv_pattern = re.compile(r'\d{8}\.csv$', re.IGNORECASE)
    media_re = re.compile(r'/mms/(in|out)/([^/]+)/([^/]+)$', re.IGNORECASE)

    message_rows = []
    referenced = set()   # actual file paths resolved by the linked artifacts
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
                        message_rows.append((row, tok))
        else:
            m = media_re.search(norm)
            if m:
                media.append((m.group(1).lower(), m.group(2), m.group(3), raw, cf))

    for direction in ('in', 'out'):
        paths = [raw for media_direction, _, _, raw, _ in media if media_direction == direction]
        name_paths, date_media = _index_mms_media(paths)
        for row, tok in message_rows:
            if (row.get('Direction') or '').lower() != direction:
                continue
            date_folder = (row.get('Date') or '')[:10]
            resolved = date_media.get(date_folder, {}).get(tok)
            candidates = name_paths.get(tok, [])
            if not resolved and len(candidates) == 1:
                resolved = candidates[0]
            if resolved:
                referenced.add(os.path.realpath(_clean_path(resolved)))

    data_headers = (
        'Date Folder', 'Direction', ('Media', 'media'),
        'Filename', 'Detected Type', 'Source File'
    )
    data_list = []
    source_path = ''
    for direction, date_folder, basename, raw, cf in media:
        if os.path.realpath(cf) in referenced:
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
                          _rel(context, cf)))

    data_list.sort(key=lambda r: (r[1], r[0], r[3]))

    return data_headers, data_list, _rel(context, source_path)


@artifact_processor
def synchronoss_contacts(context):
    """
    contacts_YYYYMMDD.txt; JSON format.
    Schema: {"contacts": {"itemcount": N, "contact": [...]}}
    Each contact has: firstname, lastname, source, created, deleted,
    itemguid, incaseofemergency, favorite, tel:[{type, number}]
    """
    data_headers = (
        'Created', 'Deleted',
        'First Name', 'Last Name', ('Phone Number', 'phonenumber'), 'Phone Type', 'Source',
        'ICE', 'Favorite', 'Item GUID', 'Source File'
    )
    data_list = []
    source_path = ''

    for _, cf in _dedupe(context.get_files_found()):
        basename = os.path.basename(cf).lower()
        if 'contacts_' not in basename or not basename.endswith('.txt'):
            continue
        source_path = cf
        rel = _rel(context, cf)
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
                        created, deleted, first, last,
                        tel.get('number', ''),
                        tel.get('type', ''), source, ice, favorite, guid,
                        rel,
                    ))
            else:
                # Contact with no phone number; still surface it
                data_list.append((
                    created, deleted, first, last, '', '',
                    source, ice, favorite, guid, rel,
                ))

    return data_headers, data_list, _rel(context, source_path)


# Providers have shipped the access log under several column and filename spellings.
# The four non-timestamp columns have been stable; the timestamp column has not.
_DV_CORE_COLUMNS = ('remoteipaddress', 'clientidentifier', 'querystring', 'lcid')
_DV_TS_COLUMNS = ('server_ts', 'logtimestamp')


def _is_dv_filename(basename):
    """True for any separator spelling of 'Dv Access Logs' (space, underscore, none)."""
    return 'dvaccesslogs' in re.sub(r'[^a-z0-9]', '', basename.lower())


def _dv_headers_match(headers):
    """Accept a workbook as an access log on its columns, since its filename may
    carry no marker at all (some returns name it for the account only)."""
    lower = {h.lower() for h in headers}
    return set(_DV_CORE_COLUMNS).issubset(lower) and bool(lower & set(_DV_TS_COLUMNS))


def _parse_dv_log(context):
    """
    Parse the DV access log and return a list of row dicts.

    The log is delivered in either of two shapes: the monthly
    'Dv Access logs mdn <LCID> <Month> <Year>.csv' files, or a single
    '<LCID>.xlsx' workbook covering the whole account (seen on 2026-format
    returns). Both carry the same five columns.

    The workbook's filename holds no 'DV' marker; it is just the account
    number; so workbooks are accepted on their column headers instead. That
    keeps an unrelated spreadsheet elsewhere in the return from being read as
    an access log.

    Handles quoted remoteipaddress fields with multiple IPs. Extracts user IP
    vs CDN IPs and the checksum from the querystring.
    """
    all_rows = []
    for _, cf in _dedupe(context.get_files_found()):
        basename = os.path.basename(cf).lower()
        if basename.endswith('.csv'):
            if not _is_dv_filename(basename):
                continue
            _, rows = _open_csv(cf)
            # Same reason the workbook reader lower-cases its headers: this CSV is
            # identified by filename, not by its columns, so a capitalised title row
            # is accepted and then read blank by the lower-case reads below. Scoped
            # to this branch on purpose -- _open_csv is shared with messages, calls
            # and both MMS artifacts, which key rows on 'Type', 'Date', 'Direction',
            # 'Sender', 'Body', 'Attachments' and 'Message ID'.
            rows = [{k.lower(): v for k, v in row.items()} for row in rows]
        elif basename.endswith('.xlsx'):
            # Headers are checked before the body is read, so a workbook that is
            # not an access log is abandoned after one row.
            _, rows = _open_xlsx(cf, accept=_dv_headers_match)
            if not rows:
                continue
        else:
            continue
        rel = _rel(context, cf)
        for row in rows:
            row['source_file'] = rel
            row['source_path'] = cf
            # Normalise the timestamp column so downstream code has one name.
            if not row.get('server_ts'):
                for alt in _DV_TS_COLUMNS:
                    if row.get(alt):
                        row['server_ts'] = row[alt]
                        break
            # Write the text columns back as text. A workbook cell can arrive as a
            # number or a date, and a consumer that calls a string method on the raw
            # cell (synchronoss_dv_sync does, on querystring) would fail the whole
            # artifact on one such cell. server_ts is left alone: _ts_utc handles a
            # datetime itself, and stringifying it here would lose that.
            for column in ('remoteipaddress', 'querystring', 'clientidentifier', 'lcid'):
                row[column] = str(row.get(column, '') or '')
            user_ip, cdn_ips = _extract_user_ip(row['remoteipaddress'])
            row['user_ip'] = user_ip
            row['cdn_ips'] = cdn_ips
            row['checksum'] = _extract_checksum(row['querystring'])
        all_rows.extend(rows)
    # Explicit-offset values are comparable; other values retain text ordering.
    all_rows.sort(key=_time_order)
    return all_rows


@artifact_processor
def synchronoss_dv_uploads(context):
    """DV access log rows carrying a 64-character hexadecimal checksum parameter."""
    data_headers = (
        'Timestamp', 'User IP', 'CDN IPs', 'Device',
        'checksum (as stored)', 'LCID', 'Source File'
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

    return data_headers, data_list, _rel(context, source_path)


@artifact_processor
def synchronoss_dv_sync(context):
    """DV access log rows with no selected checksum parameter."""
    data_headers = (
        'Timestamp', 'User IP', 'CDN IPs', 'Device',
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

    return data_headers, data_list, _rel(context, source_path)


_QUARANTINE_NAME_RE = re.compile(
    r'^(?P<container>[0-9a-f]+)_(?P<sha256>[0-9a-f]{64})\.zip_file_(?P<seq>\d+)$',
    re.IGNORECASE)


def _sha256_file(path):
    """Stream a file's SHA-256. Read-only; the source is never modified."""
    digest = hashlib.sha256()
    try:
        with open(path, 'rb') as fh:
            for chunk in iter(lambda: fh.read(1024 * 1024), b''):
                digest.update(chunk)
    except OSError as e:
        logfunc(f'Synchronoss quarantine hash error ({path}): {e}')
        return ''
    return digest.hexdigest()


@artifact_processor
def synchronoss_quarantined(context):
    """Files matching the quarantined filename pattern, hashed and joined to log checksums. The first matching row in the report order is shown; no upload or reporting event is inferred."""
    # checksum -> matching access log rows, in report order
    uploads = {}
    for row in _parse_dv_log(context):
        checksum = row.get('checksum', '')
        if checksum:
            uploads.setdefault(checksum.lower(), []).append(row)

    data_headers = (
        'Matched Log Timestamp', 'User IP', 'Device', ('Media', 'media'),
        'Detected Type', 'Size (bytes)', 'SHA-256', 'Hash Verified', 'DV Correlation',
        'Sequence', 'Filename', 'Source File'
    )
    data_list = []
    source_path = ''

    for raw, cf in _dedupe(context.get_files_found()):
        basename = os.path.basename(cf)
        match = _QUARANTINE_NAME_RE.match(basename)
        if not match:
            continue
        source_path = cf
        claimed = match.group('sha256').lower()

        actual = _sha256_file(cf)
        if not actual:
            verified = 'not verified; file unreadable'
        elif actual == claimed:
            verified = 'yes; content matches filename hash'
        else:
            # Report a mismatch between the delivered file bytes and filename hash.
            verified = f'NO; content hashes to {actual}'

        try:
            size = os.path.getsize(cf)
        except OSError:
            size = ''

        detected = _detect_media_type(cf)
        detected = f'{detected} (by magic bytes)' if detected else 'unknown (magic bytes)'

        events = uploads.get(claimed, [])
        if events:
            first = events[0]
            timestamp = _ts_utc(first.get('server_ts', ''))
            user_ip = first.get('user_ip', '')
            device = first.get('clientidentifier', '')
            correlation = 'matched DV access log row'
            if len(events) > 1:
                correlation = (f'matched DV access log row '
                               f'({len(events)} rows; first shown)')
        else:
            timestamp, user_ip, device = '', '', ''
            correlation = 'no matching checksum in DV access log'

        data_list.append((
            timestamp, user_ip, device,
            _register_media(raw, basename),
            detected, size, claimed, verified, correlation,
            int(match.group('seq')), basename,
            _rel(context, cf),
        ))

    data_list.sort(key=lambda r: r[9])

    return data_headers, data_list, _rel(context, source_path)


@artifact_processor
def synchronoss_vzmobile(context):
    """Files below VZMOBILE date/device folders; the folder date is stored text."""
    data_headers = (
        'Date Folder', 'Device', ('Media', 'media'),
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
            _rel(context, cf),
        ))

    # Sort by upload date then device then filename
    data_list.sort(key=lambda r: (r[0], r[1], r[3]))

    return data_headers, data_list, _rel(context, source_path)

__artifacts_v2__ = {
    "kik_subscriber": {
        "name": "Kik - Subscriber Info",
        "description": "Parses Kik subscriber/account fields from the returns package PDF",
        "author": "@OneSixForensics",
        "creation_date": "2026-05-08",
        "last_update_date": "2026-06-25",
        "requirements": "pdfminer.six",
        "category": "Kik",
        "notes": "Located at package/subscriber-data-<username>_<id>.pdf",
        "paths": ('*/package/subscriber-data-*.pdf',),
        "output_types": "standard",
        "artifact_icon": "user"
    },
    "kik_subscriber_pics": {
        "name": "Kik - Subscriber Profile Pics",
        "description": "Profile picture URLs and their original/scaled MD5s from the subscriber PDF",
        "author": "@OneSixForensics",
        "creation_date": "2026-05-08",
        "last_update_date": "2026-06-25",
        "requirements": "pdfminer.six",
        "category": "Kik",
        "notes": "Located at package/subscriber-data-<username>_<id>.pdf",
        "paths": ('*/package/subscriber-data-*.pdf',),
        "output_types": "standard",
        "html_columns": ['Profile Pic URL'],
        "artifact_icon": "photo"
    },
    "kik_subscriber_events": {
        "name": "Kik - Subscriber Events",
        "description": "Timestamped account events from the subscriber PDF event log",
        "author": "@OneSixForensics",
        "creation_date": "2026-05-08",
        "last_update_date": "2026-06-25",
        "requirements": "pdfminer.six",
        "category": "Kik",
        "notes": "Located at package/subscriber-data-<username>_<id>.pdf",
        "paths": ('*/package/subscriber-data-*.pdf',),
        "output_types": "standard",
        "artifact_icon": "activity"
    },
    "kik_group_legend": {
        "name": "Kik - Group Legend",
        "description": "Parses group-legend-<username>_<id>.csv — maps group JIDs to names and metadata",
        "author": "@OneSixForensics",
        "creation_date": "2026-05-08",
        "last_update_date": "2026-06-25",
        "requirements": "none",
        "category": "Kik",
        "notes": "Located at package/group-legend-<username>_<id>.csv",
        "paths": ('*/package/group-legend-*.csv',),
        "output_types": "standard",
        "artifact_icon": "users"
    },
    "kik_chat_text": {
        "name": "Kik - Chat Messages (Text)",
        "description": "Parses data-text.csv from Kik returns content folder - direct message text content",
        "author": "@OneSixForensics",
        "creation_date": "2026-05-08",
        "last_update_date": "2026-06-25",
        "requirements": "none",
        "category": "Kik",
        "notes": "Located at package/content/data-text.csv",
        "paths": ('*/package/content/data-text.csv',),
        "output_types": "standard",
        "artifact_icon": "message"
    },
    "kik_chat_media": {
        "name": "Kik - Chat Messages (Media)",
        "description": "Parses data-media.csv from Kik returns content folder - media message metadata",
        "author": "@OneSixForensics",
        "creation_date": "2026-05-08",
        "last_update_date": "2026-06-25",
        "requirements": "none",
        "category": "Kik",
        "notes": "Located at package/content/data-media.csv. Filenames in medias/ folder are Base64-encoded.",
        "paths": ('*/package/content/data-media.csv', '*/package/content/medias/*'),
        "output_types": "standard",
        "artifact_icon": "photo"
    },
    "kik_chat_sent": {
        "name": "Kik - Sent Chats (Log)",
        "description": "Parses chat_sent.csv from the logs folder",
        "author": "@OneSixForensics",
        "creation_date": "2026-05-08",
        "last_update_date": "2026-06-25",
        "requirements": "none",
        "category": "Kik",
        "notes": "Located at package/logs/chat_sent.csv",
        "paths": ('*/package/logs/chat_sent.csv',),
        "output_types": "standard",
        "artifact_icon": "message"
    },
    "kik_chat_sent_received": {
        "name": "Kik - Sent and Received Chats (Log)",
        "description": "Parses chat_sent_received.csv from the logs folder",
        "author": "@OneSixForensics",
        "creation_date": "2026-05-08",
        "last_update_date": "2026-06-25",
        "requirements": "none",
        "category": "Kik",
        "notes": "Located at package/logs/chat_sent_received.csv",
        "paths": ('*/package/logs/chat_sent_received.csv',),
        "output_types": "standard",
        "artifact_icon": "message"
    },
    "kik_chat_platform_sent": {
        "name": "Kik - Platform Chat Sent (Log)",
        "description": "Parses chat_platform_sent.csv from the logs folder",
        "author": "@OneSixForensics",
        "creation_date": "2026-05-08",
        "last_update_date": "2026-06-25",
        "requirements": "none",
        "category": "Kik",
        "notes": "Located at package/logs/chat_platform_sent.csv",
        "paths": ('*/package/logs/chat_platform_sent.csv',),
        "output_types": "standard",
        "artifact_icon": "message"
    },
    "kik_chat_platform_sent_received": {
        "name": "Kik - Platform Chat Sent and Received (Log)",
        "description": "Parses chat_platform_sent_received.csv from the logs folder",
        "author": "@OneSixForensics",
        "creation_date": "2026-05-08",
        "last_update_date": "2026-06-25",
        "requirements": "none",
        "category": "Kik",
        "notes": "Located at package/logs/chat_platform_sent_received.csv",
        "paths": ('*/package/logs/chat_platform_sent_received.csv',),
        "output_types": "standard",
        "artifact_icon": "message"
    },
    "kik_group_receive": {
        "name": "Kik - Group Messages Received (Log)",
        "description": "Parses group_receive.csv from the logs folder",
        "author": "@OneSixForensics",
        "creation_date": "2026-05-08",
        "last_update_date": "2026-06-25",
        "requirements": "none",
        "category": "Kik",
        "notes": "Located at package/logs/group_receive.csv",
        "paths": ('*/package/logs/group_receive.csv',),
        "output_types": "standard",
        "artifact_icon": "users"
    },
    "kik_group_send": {
        "name": "Kik - Group Messages Sent (Log)",
        "description": "Parses group_send_msg_platform.csv from the logs folder",
        "author": "@OneSixForensics",
        "creation_date": "2026-05-08",
        "last_update_date": "2026-06-25",
        "requirements": "none",
        "category": "Kik",
        "notes": "Located at package/logs/group_send_msg_platform.csv",
        "paths": ('*/package/logs/group_send_msg_platform.csv',),
        "output_types": "standard",
        "artifact_icon": "users"
    },
    "kik_friends_added": {
        "name": "Kik - Friends Added (Log)",
        "description": "Parses friends_added.csv from the logs folder",
        "author": "@OneSixForensics",
        "creation_date": "2026-05-08",
        "last_update_date": "2026-06-25",
        "requirements": "none",
        "category": "Kik",
        "notes": "Located at package/logs/friends_added.csv",
        "paths": ('*/package/logs/friends_added.csv',),
        "output_types": "standard",
        "artifact_icon": "user-plus"
    },
    "kik_block_user": {
        "name": "Kik - Blocked Users (Log)",
        "description": "Parses block_user.csv from the logs folder",
        "author": "@OneSixForensics",
        "creation_date": "2026-05-08",
        "last_update_date": "2026-06-25",
        "requirements": "none",
        "category": "Kik",
        "notes": "Located at package/logs/block_user.csv",
        "paths": ('*/package/logs/block_user.csv',),
        "output_types": "standard",
        "artifact_icon": "user-x"
    },
    "kik_binds": {
        "name": "Kik - Binds (Log)",
        "description": "Parses binds.csv from the logs folder - device/session binding events",
        "author": "@OneSixForensics",
        "creation_date": "2026-05-08",
        "last_update_date": "2026-06-25",
        "requirements": "none",
        "category": "Kik",
        "notes": "Located at package/logs/binds.csv",
        "paths": ('*/package/logs/binds.csv',),
        "output_types": "standard",
        "artifact_icon": "device-mobile"
    },
}

import csv
import os
import re
from datetime import datetime, timedelta, timezone

from scripts.ilapfuncs import artifact_processor, check_in_media, logfunc

try:
    from pdfminer.high_level import extract_text as pdf_extract_text
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

_UNIX_EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)

# Human-readable timestamp formats observed in Kik returns (all values UTC)
_TS_FORMATS = (
    '%Y-%m-%d %H:%M:%S.%f',
    '%Y-%m-%d %H:%M:%S',
    '%Y/%m/%d %H:%M:%S',
    '%Y-%m-%dT%H:%M:%S',
)


def _clean_path(path):
    """Strip Windows extended-length path prefix if present (\\\\?\\)."""
    p = str(path)
    if p.startswith('\\\\?\\'):
        return p[4:]
    return p


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
    except Exception as e:  # pylint: disable=broad-except
        logfunc(f'Kik parser CSV read error ({file_found}): {e}')
    return headers, rows


def _fallback_rows(headers, rows):
    """Return all columns as-is when schema is unknown or unexpected."""
    return headers, [tuple(row.get(h, '') for h in headers) for row in rows]


def _ms_to_utc(ms_value):
    """
    Convert a Unix epoch in milliseconds (13-digit integer) to an aware UTC
    datetime, preserving millisecond precision.
    Returns the original value as a string if conversion fails.
    Example: 1764622464103 -> datetime(2025, 12, 1, 20, 54, 24, 103000, tzinfo=utc)
    """
    try:
        ms = int(ms_value)
        return _UNIX_EPOCH + timedelta(milliseconds=ms)
    except (ValueError, TypeError, OverflowError):
        return str(ms_value) if ms_value else ''


def _kik_ts(value):
    """
    Convert a human-readable Kik timestamp string (UTC per the return format)
    to an aware UTC datetime. Values that don't match a known format are kept
    as plain text so no source data is lost.
    """
    value = (value or '').strip()
    text = value[:-4].rstrip() if value.endswith(' UTC') else value
    for fmt in _TS_FORMATS:
        try:
            return datetime.strptime(text, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    return value


def _register_media(file_path, name):
    """Register a media file for inline HTML + LAVA rendering, returning its
    media-reference id (or '' if it can't be registered). Thin wrapper over the
    framework's check_in_media so call sites never propagate a None.
    """
    return check_in_media(file_path, name) or ''


def _iter_unique_files(context, basename_filter):
    """Yield (file_found, relative_source) for files whose basename passes
    basename_filter, deduplicated by real path."""
    seen = set()
    for file_found in context.get_files_found():
        file_found = _clean_path(str(file_found))
        if not basename_filter(os.path.basename(file_found)):
            continue
        real_path = os.path.realpath(file_found)
        if real_path in seen:
            continue
        seen.add(real_path)
        yield file_found, context.get_relative_path(file_found)


# ---------------------------------------------------------------------------
# Subscriber PDF (one PDF -> three artifacts: Info, Profile Pics, Events)
# ---------------------------------------------------------------------------

_PDF_TEXT_CACHE = {}


def _is_subscriber_pdf(basename):
    return basename.startswith('subscriber-data-') and basename.lower().endswith('.pdf')


def _get_pdf_text(file_found):
    """Extract (and cache) the text of a subscriber PDF. Returns '' on failure."""
    if file_found in _PDF_TEXT_CACHE:
        return _PDF_TEXT_CACHE[file_found]
    text = ''
    try:
        text = pdf_extract_text(file_found) or ''
    except Exception as e:  # pylint: disable=broad-except
        logfunc(f'Kik subscriber PDF read error ({file_found}): {e}')
    _PDF_TEXT_CACHE[file_found] = text
    return text


_SUB_FIELD_PATTERNS = [
    ('First Name',             r'First Name:\s*(.+)'),
    ('Last Name',              r'Last Name:[ \t]*([^\n]*)'),
    ('Email',                  r'Email:\s*(\S+)'),
    ('Email Confirmed',        r'Email:\s*\S+\s*(\(confirmed\))'),
    ('Username',               r'Username:\s*(\S+)'),
    ('Registration Timestamp', r'REGISTRATION_TIMESTAMP\s+([\d/]{10}\s[\d:]{8})'),
    ('User Locale',            r'USER_LOCALE\s+(\S+)'),
    ('Client Version',         r'CLIENT_VERSION[\s\S]*?([\d]+\.[\d]+\.[\d]+)'),
    ('User Location',          r'USER_LOCATION[\s\S]*?(\S.*?)\n'),
    ('System Version',         r'system-version=([\d.]+)'),
    ('App Version',            r'(?<!system-)version=([^\s]+)'),
    ('Country Code',           r'country-code=(\S+)'),
    ('Enterprise',             r'enterprise=(\S+)'),
]

_PIC_URL_PATTERN = re.compile(r'https?://profilepics\.kik\.com/[^\s)]+\.jpg', re.IGNORECASE)
_PIC_ORIG_MD5_PATTERN = re.compile(r'original MD5:\s*([A-F0-9]{32})', re.IGNORECASE)
_PIC_SCALED_MD5_PATTERN = re.compile(r'scaled[\s\S]*? MD5:\s*([A-F0-9]{32})', re.IGNORECASE)
_EVENT_PATTERN = re.compile(
    r'(\d{4}/\d{2}/\d{2}\s+\d{2}:\d{2}:\d{2}\s+UTC)\s+'
    r'(?!PROFILE_PIC_URL)([A-Z_]+)\s+(.+)'
)


@artifact_processor
def kik_subscriber(context):
    """subscriber-data-<username>_<id>.pdf — key subscriber fields."""
    data_headers = ('Field', 'Value', 'Source File')
    data_list = []
    source_path = ''
    if not PDF_SUPPORT:
        logfunc('Kik subscriber PDF: pdfminer.six not installed. '
                'Run: pip install pdfminer.six  then re-run RLEAPP.')
        return data_headers, data_list, source_path

    for file_found, rel_source in _iter_unique_files(context, _is_subscriber_pdf):
        raw_text = _get_pdf_text(file_found)
        if not raw_text:
            continue
        source_path = file_found
        for label, pattern in _SUB_FIELD_PATTERNS:
            m = re.search(pattern, raw_text, re.IGNORECASE)
            if m:
                data_list.append((label, m.group(1).strip(), rel_source))

    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def kik_subscriber_pics(context):
    """Profile picture URLs + original/scaled MD5s from the subscriber PDF."""
    data_headers = ('Profile Pic URL', 'Original MD5', 'Scaled MD5', 'Source File')
    data_list = []
    source_path = ''
    if not PDF_SUPPORT:
        return data_headers, data_list, source_path

    for file_found, rel_source in _iter_unique_files(context, _is_subscriber_pdf):
        raw_text = _get_pdf_text(file_found)
        if not raw_text:
            continue
        source_path = file_found
        # pdfminer splits each entry across lines and may inject page-break
        # content between the URL and its MD5 values; extract the three lists
        # independently and pair by index.
        pic_urls = _PIC_URL_PATTERN.findall(raw_text)
        pic_orig_md5s = _PIC_ORIG_MD5_PATTERN.findall(raw_text)
        pic_scaled_md5s = _PIC_SCALED_MD5_PATTERN.findall(raw_text)
        for i, url in enumerate(pic_urls):
            orig_md5 = pic_orig_md5s[i].upper() if i < len(pic_orig_md5s) else ''
            scaled_md5 = pic_scaled_md5s[i].upper() if i < len(pic_scaled_md5s) else ''
            data_list.append((
                f'<a href="{url}" style="color:#4dabf7;">{url}</a>',
                orig_md5, scaled_md5, rel_source
            ))

    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def kik_subscriber_events(context):
    """Timestamped account events from the subscriber PDF event log."""
    data_headers = (('Timestamp (UTC)', 'datetime'), 'Event Type', 'Value', 'Source File')
    data_list = []
    source_path = ''
    if not PDF_SUPPORT:
        return data_headers, data_list, source_path

    for file_found, rel_source in _iter_unique_files(context, _is_subscriber_pdf):
        raw_text = _get_pdf_text(file_found)
        if not raw_text:
            continue
        source_path = file_found
        for m in _EVENT_PATTERN.finditer(raw_text):
            data_list.append((_kik_ts(m.group(1).strip()), m.group(2).strip(),
                              m.group(3).strip(), rel_source))

    return data_headers, data_list, context.get_relative_path(source_path)


# ---------------------------------------------------------------------------
# Group legend
# ---------------------------------------------------------------------------

def _is_group_legend(basename):
    return basename.startswith('group-legend-') and basename.lower().endswith('.csv')


@artifact_processor
def kik_group_legend(context):
    """
    group-legend-<username>_<id>.csv
    Confirmed schema: gid, name, code, public, deleted, last_join_ts, last_activity
    """
    data_headers = (
        ('Last Join', 'datetime'), 'Last Activity', 'Group ID', 'Name', 'Code',
        'Public', 'Deleted', 'Source File'
    )
    data_list = []
    source_path = ''
    expected = {'gid', 'name', 'code', 'public', 'deleted', 'last_join_ts', 'last_activity'}
    for file_found, rel_source in _iter_unique_files(context, _is_group_legend):
        headers, rows = _open_csv(file_found)
        if not headers:
            continue
        source_path = file_found
        if not expected.issubset(set(headers)):
            logfunc(f'Kik group-legend: Unexpected schema. Found: {headers}. Raw fallback.')
            fb_headers, fb_list = _fallback_rows(headers, rows)
            return tuple(fb_headers), fb_list, rel_source
        for row in rows:
            data_list.append((
                _kik_ts(row.get('last_join_ts', '')), row.get('last_activity', ''),
                row.get('gid', ''), row.get('name', ''), row.get('code', ''),
                row.get('public', ''), row.get('deleted', ''), rel_source
            ))

    return data_headers, data_list, context.get_relative_path(source_path)


# ---------------------------------------------------------------------------
# content/data-text.csv
# ---------------------------------------------------------------------------

@artifact_processor
def kik_chat_text(context):
    """
    package/content/data-text.csv
    Schema: id, content_id, filename, message, sender_id, receiver_id,
            ip, port, parent_id, sent_at, sent_at_ts, app_name
    """
    data_headers = (
        ('Sent At', 'datetime'), 'Sent At (ms Epoch)', ('Sent At (Epoch UTC)', 'datetime'),
        'Sender ID', 'Receiver ID', 'Message', 'App Name',
        'ID', 'Content ID', 'Filename', 'IP', 'Port', 'Parent ID', 'Source File'
    )
    data_list = []
    source_path = ''
    expected = {'id', 'message', 'sender_id', 'receiver_id', 'sent_at', 'sent_at_ts', 'app_name'}
    for file_found, rel_source in _iter_unique_files(context, lambda b: b == 'data-text.csv'):
        headers, rows = _open_csv(file_found)
        if not headers:
            continue
        source_path = file_found
        if not expected.issubset(set(headers)):
            logfunc(f'Kik data-text.csv: Unexpected schema. Found: {headers}. Raw fallback.')
            fb_headers, fb_list = _fallback_rows(headers, rows)
            return tuple(fb_headers), fb_list, rel_source
        for row in rows:
            raw_ms = row.get('sent_at_ts', '')
            data_list.append((
                _kik_ts(row.get('sent_at', '')), raw_ms, _ms_to_utc(raw_ms),
                row.get('sender_id', ''), row.get('receiver_id', ''),
                row.get('message', ''), row.get('app_name', ''),
                row.get('id', ''), row.get('content_id', ''), row.get('filename', ''),
                row.get('ip', ''), row.get('port', ''), row.get('parent_id', ''),
                rel_source
            ))

    return data_headers, data_list, context.get_relative_path(source_path)


# ---------------------------------------------------------------------------
# content/data-media.csv + content/medias/*
# ---------------------------------------------------------------------------

@artifact_processor
def kik_chat_media(context):
    """
    package/content/data-media.csv  +  package/content/medias/*
    Inline media is registered through the framework's media pipeline
    (handles the Base64-encoded names), rendered in HTML and LAVA.
    Referenced-but-absent media shows the filename with an empty media cell.
    """
    csv_file = None
    media_lookup = {}  # basename -> raw files_found path
    for f in context.get_files_found():
        raw = str(f)
        cf = _clean_path(raw)
        if cf.endswith('data-media.csv'):
            csv_file = cf
        elif os.path.isfile(cf):
            media_lookup[os.path.basename(cf)] = raw

    data_headers = (
        ('Sent At', 'datetime'), 'Sent At (ms Epoch)', ('Sent At (Epoch UTC)', 'datetime'),
        'Sender ID', 'Receiver ID', ('Media', 'media'), 'Media Filename',
        'Message/Caption', 'App Name', 'ID', 'Content ID', 'IP', 'Port',
        'Parent ID', 'Source File'
    )
    data_list = []
    if not csv_file:
        logfunc('Kik data-media.csv: CSV not found in files_found')
        return data_headers, data_list, ''

    headers, rows = _open_csv(csv_file)
    rel_source = context.get_relative_path(csv_file)
    if not headers:
        return data_headers, data_list, ''

    expected = {'id', 'filename', 'sender_id', 'receiver_id', 'sent_at', 'sent_at_ts', 'app_name'}
    if not expected.issubset(set(headers)):
        logfunc(f'Kik data-media.csv: Unexpected schema. Found: {headers}. Raw fallback.')
        fb_headers, fb_list = _fallback_rows(headers, rows)
        return tuple(fb_headers), fb_list, rel_source

    for row in rows:
        raw_ms = row.get('sent_at_ts', '')
        fname = row.get('filename', '')
        media_cell = _register_media(media_lookup[fname], fname) if fname in media_lookup else ''
        data_list.append((
            _kik_ts(row.get('sent_at', '')), raw_ms, _ms_to_utc(raw_ms),
            row.get('sender_id', ''), row.get('receiver_id', ''),
            media_cell, fname, row.get('message', ''), row.get('app_name', ''),
            row.get('id', ''), row.get('content_id', ''), row.get('ip', ''),
            row.get('port', ''), row.get('parent_id', ''), rel_source
        ))

    return data_headers, data_list, rel_source


# ---------------------------------------------------------------------------
# logs/*.csv — shared hardened parser (aggregates rows, schema fallback)
# ---------------------------------------------------------------------------

def _parse_log(context, log_basename, expected_cols, data_headers, row_builder):
    """Shared parser for all logs/ CSVs. Returns (headers, data_list, source).
    Falls back to raw column output if a file's schema doesn't match."""
    data_list = []
    source_path = ''
    for file_found, rel_source in _iter_unique_files(context, lambda b: b == log_basename):
        headers, rows = _open_csv(file_found)
        if not headers:
            continue
        source_path = file_found
        if not expected_cols.issubset(set(headers)):
            logfunc(f'Kik log: Unexpected schema in {os.path.basename(file_found)}: '
                    f'{headers}. Raw fallback.')
            fb_headers, fb_list = _fallback_rows(headers, rows)
            return tuple(fb_headers), fb_list, rel_source
        data_list.extend(row_builder(r, rel_source) for r in rows)
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def kik_chat_sent(context):
    # logs/chat_sent.csv — Schema: user_jid, friend_user_jid, ip, ts, words
    return _parse_log(
        context, 'chat_sent.csv',
        expected_cols={'user_jid', 'friend_user_jid', 'ip', 'ts', 'words'},
        data_headers=(('Timestamp', 'datetime'), 'User JID', 'Friend User JID', 'IP',
                      'Word Count', 'Source File'),
        row_builder=lambda r, f: (
            _kik_ts(r.get('ts', '')), r.get('user_jid', ''), r.get('friend_user_jid', ''),
            r.get('ip', ''), r.get('words', ''), f
        )
    )


@artifact_processor
def kik_chat_sent_received(context):
    # logs/chat_sent_received.csv — Schema: user_jid, friend_user_jid, ip, ts, words
    return _parse_log(
        context, 'chat_sent_received.csv',
        expected_cols={'user_jid', 'friend_user_jid', 'ip', 'ts', 'words'},
        data_headers=(('Timestamp', 'datetime'), 'User JID', 'Friend User JID', 'IP',
                      'Word Count', 'Source File'),
        row_builder=lambda r, f: (
            _kik_ts(r.get('ts', '')), r.get('user_jid', ''), r.get('friend_user_jid', ''),
            r.get('ip', ''), r.get('words', ''), f
        )
    )


@artifact_processor
def kik_chat_platform_sent(context):
    # logs/chat_platform_sent.csv — Schema: user_jid, friend_user_jid, ip, ts, app_name, cid
    return _parse_log(
        context, 'chat_platform_sent.csv',
        expected_cols={'user_jid', 'friend_user_jid', 'ip', 'ts', 'app_name', 'cid'},
        data_headers=(('Timestamp', 'datetime'), 'User JID', 'Friend User JID', 'IP',
                      'App Name', 'CID', 'Source File'),
        row_builder=lambda r, f: (
            _kik_ts(r.get('ts', '')), r.get('user_jid', ''), r.get('friend_user_jid', ''),
            r.get('ip', ''), r.get('app_name', ''), r.get('cid', ''), f
        )
    )


@artifact_processor
def kik_chat_platform_sent_received(context):
    # logs/chat_platform_sent_received.csv — Schema: user_jid, friend_user_jid, ip, ts,
    # app_name, cid
    return _parse_log(
        context, 'chat_platform_sent_received.csv',
        expected_cols={'user_jid', 'friend_user_jid', 'ip', 'ts', 'app_name', 'cid'},
        data_headers=(('Timestamp', 'datetime'), 'User JID', 'Friend User JID', 'IP',
                      'App Name', 'CID', 'Source File'),
        row_builder=lambda r, f: (
            _kik_ts(r.get('ts', '')), r.get('user_jid', ''), r.get('friend_user_jid', ''),
            r.get('ip', ''), r.get('app_name', ''), r.get('cid', ''), f
        )
    )


_GROUP_COLS = {'sender', 'receiver', 'ts', 'group_jid', 'sender_ip', 'sender_device_type',
               'cid', 'app_name', 'app', 'receive_ip', 'dt', 'epoch'}
_GROUP_HEADERS = (
    ('Timestamp', 'datetime'), 'Epoch (ms)', ('Epoch (UTC)', 'datetime'), 'Sender', 'Receiver',
    'Group JID', 'Sender IP', 'Receive IP', 'Sender Device Type', 'App Name', 'App', 'CID',
    'Source File'
)


def _group_row(r, f):
    return (
        _kik_ts(r.get('ts', '')), r.get('epoch', ''), _ms_to_utc(r.get('epoch', '')),
        r.get('sender', ''), r.get('receiver', ''), r.get('group_jid', ''),
        r.get('sender_ip', ''), r.get('receive_ip', ''), r.get('sender_device_type', ''),
        r.get('app_name', ''), r.get('app', ''), r.get('cid', ''), f
    )


@artifact_processor
def kik_group_receive(context):
    # logs/group_receive.csv
    return _parse_log(context, 'group_receive.csv', _GROUP_COLS, _GROUP_HEADERS, _group_row)


@artifact_processor
def kik_group_send(context):
    # logs/group_send_msg_platform.csv
    return _parse_log(context, 'group_send_msg_platform.csv', _GROUP_COLS, _GROUP_HEADERS,
                      _group_row)


@artifact_processor
def kik_friends_added(context):
    # logs/friends_added.csv — Schema: user_jid, friend_user_jid, ts
    return _parse_log(
        context, 'friends_added.csv',
        expected_cols={'user_jid', 'friend_user_jid', 'ts'},
        data_headers=(('Timestamp', 'datetime'), 'User JID', 'Friend User JID', 'Source File'),
        row_builder=lambda r, f: (
            _kik_ts(r.get('ts', '')), r.get('user_jid', ''), r.get('friend_user_jid', ''), f
        )
    )


@artifact_processor
def kik_block_user(context):
    # logs/block_user.csv — Schema: user_jid, block_user_jid, ts
    return _parse_log(
        context, 'block_user.csv',
        expected_cols={'user_jid', 'block_user_jid', 'ts'},
        data_headers=(('Timestamp', 'datetime'), 'User JID', 'Blocked User JID', 'Source File'),
        row_builder=lambda r, f: (
            _kik_ts(r.get('ts', '')), r.get('user_jid', ''), r.get('block_user_jid', ''), f
        )
    )


@artifact_processor
def kik_binds(context):
    # logs/binds.csv — Schema: user_jid, ip, port, ts, device
    return _parse_log(
        context, 'binds.csv',
        expected_cols={'user_jid', 'ip', 'port', 'ts', 'device'},
        data_headers=(('Timestamp', 'datetime'), 'User JID', 'IP', 'Port', 'Device',
                      'Source File'),
        row_builder=lambda r, f: (
            _kik_ts(r.get('ts', '')), r.get('user_jid', ''), r.get('ip', ''),
            r.get('port', ''), r.get('device', ''), f
        )
    )

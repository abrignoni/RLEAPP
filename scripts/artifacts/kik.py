__artifacts_v2__ = {
    "kik_subscriber": {
        "name": "Kik - Subscriber Info",
        "description": "Parses Kik subscriber/account data from the returns package PDF",
        "author": "@OneSixForensics",
        "version": "0.3",
        "date": "2026-05-08",
        "requirements": "pdfminer.six",
        "category": "Kik",
        "notes": "Located at package/subscriber-data-<username>_<id>.pdf",
        "paths": ('*/package/subscriber-data-*.pdf',),
        "function": "get_kik_subscriber",
        "artifact_icon": "user"
    },
    "kik_group_legend": {
        "name": "Kik - Group Legend",
        "description": "Parses group-legend-<username>_<id>.csv — maps group JIDs to names and metadata",
        "author": "@OneSixForensics",
        "version": "0.1",
        "date": "2026-05-08",
        "requirements": "none",
        "category": "Kik",
        "notes": "Located at package/group-legend-<username>_<id>.csv",
        "paths": ('*/package/group-legend-*.csv',),
        "function": "get_kik_group_legend",
        "artifact_icon": "users"
    },
    "kik_chat_text": {
        "name": "Kik - Chat Messages (Text)",
        "description": "Parses data-text.csv from Kik returns content folder - direct message text content",
        "author": "@OneSixForensics",
        "version": "0.1",
        "date": "2026-05-08",
        "requirements": "none",
        "category": "Kik",
        "notes": "Located at package/content/data-text.csv",
        "paths": ('*/package/content/data-text.csv',),
        "function": "get_kik_chat_text",
        "artifact_icon": "message-square"
    },
    "kik_chat_media": {
        "name": "Kik - Chat Messages (Media)",
        "description": "Parses data-media.csv from Kik returns content folder - media message metadata",
        "author": "@OneSixForensics",
        "version": "0.1",
        "date": "2026-05-08",
        "requirements": "none",
        "category": "Kik",
        "notes": "Located at package/content/data-media.csv. Filenames in medias/ folder are Base64-encoded.",
        "paths": ('*/package/content/data-media.csv', '*/package/content/medias/*'),
        "function": "get_kik_chat_media",
        "artifact_icon": "image"
    },
    "kik_chat_sent": {
        "name": "Kik - Sent Chats (Log)",
        "description": "Parses chat_sent.csv from the logs folder",
        "author": "@OneSixForensics",
        "version": "0.1",
        "date": "2026-05-08",
        "requirements": "none",
        "category": "Kik",
        "notes": "Located at package/logs/chat_sent.csv",
        "paths": ('*/package/logs/chat_sent.csv',),
        "function": "get_kik_chat_sent",
        "artifact_icon": "message-square"
    },
    "kik_chat_sent_received": {
        "name": "Kik - Sent & Received Chats (Log)",
        "description": "Parses chat_sent_received.csv from the logs folder",
        "author": "@OneSixForensics",
        "version": "0.1",
        "date": "2026-05-08",
        "requirements": "none",
        "category": "Kik",
        "notes": "Located at package/logs/chat_sent_received.csv",
        "paths": ('*/package/logs/chat_sent_received.csv',),
        "function": "get_kik_chat_sent_received",
        "artifact_icon": "message-square"
    },
    "kik_chat_platform_sent": {
        "name": "Kik - Platform Chat Sent (Log)",
        "description": "Parses chat_platform_sent.csv from the logs folder",
        "author": "@OneSixForensics",
        "version": "0.1",
        "date": "2026-05-08",
        "requirements": "none",
        "category": "Kik",
        "notes": "Located at package/logs/chat_platform_sent.csv",
        "paths": ('*/package/logs/chat_platform_sent.csv',),
        "function": "get_kik_chat_platform_sent",
        "artifact_icon": "message-square"
    },
    "kik_chat_platform_sent_received": {
        "name": "Kik - Platform Chat Sent & Received (Log)",
        "description": "Parses chat_platform_sent_received.csv from the logs folder",
        "author": "@OneSixForensics",
        "version": "0.1",
        "date": "2026-05-08",
        "requirements": "none",
        "category": "Kik",
        "notes": "Located at package/logs/chat_platform_sent_received.csv",
        "paths": ('*/package/logs/chat_platform_sent_received.csv',),
        "function": "get_kik_chat_platform_sent_received",
        "artifact_icon": "message-square"
    },
    "kik_group_receive": {
        "name": "Kik - Group Messages Received (Log)",
        "description": "Parses group_receive.csv from the logs folder",
        "author": "@OneSixForensics",
        "version": "0.1",
        "date": "2026-05-08",
        "requirements": "none",
        "category": "Kik",
        "notes": "Located at package/logs/group_receive.csv",
        "paths": ('*/package/logs/group_receive.csv',),
        "function": "get_kik_group_receive",
        "artifact_icon": "users"
    },
    "kik_group_send": {
        "name": "Kik - Group Messages Sent (Log)",
        "description": "Parses group_send_msg_platform.csv from the logs folder",
        "author": "@OneSixForensics",
        "version": "0.1",
        "date": "2026-05-08",
        "requirements": "none",
        "category": "Kik",
        "notes": "Located at package/logs/group_send_msg_platform.csv",
        "paths": ('*/package/logs/group_send_msg_platform.csv',),
        "function": "get_kik_group_send",
        "artifact_icon": "users"
    },
    "kik_friends_added": {
        "name": "Kik - Friends Added (Log)",
        "description": "Parses friends_added.csv from the logs folder",
        "author": "@OneSixForensics",
        "version": "0.1",
        "date": "2026-05-08",
        "requirements": "none",
        "category": "Kik",
        "notes": "Located at package/logs/friends_added.csv",
        "paths": ('*/package/logs/friends_added.csv',),
        "function": "get_kik_friends_added",
        "artifact_icon": "user-plus"
    },
    "kik_block_user": {
        "name": "Kik - Blocked Users (Log)",
        "description": "Parses block_user.csv from the logs folder",
        "author": "@OneSixForensics",
        "version": "0.1",
        "date": "2026-05-08",
        "requirements": "none",
        "category": "Kik",
        "notes": "Located at package/logs/block_user.csv",
        "paths": ('*/package/logs/block_user.csv',),
        "function": "get_kik_block_user",
        "artifact_icon": "user-x"
    },
    "kik_binds": {
        "name": "Kik - Binds (Log)",
        "description": "Parses binds.csv from the logs folder - device/session binding events",
        "author": "@OneSixForensics",
        "version": "0.1",
        "date": "2026-05-08",
        "requirements": "none",
        "category": "Kik",
        "notes": "Located at package/logs/binds.csv",
        "paths": ('*/package/logs/binds.csv',),
        "function": "get_kik_binds",
        "artifact_icon": "smartphone"
    },
}

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import csv
import os
from datetime import datetime, timezone

import re
from scripts.artifact_report import ArtifactHtmlReport
import scripts.ilapfuncs as ilapfuncs

try:
    from pdfminer.high_level import extract_text as pdf_extract_text
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

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
    except Exception as e:
        ilapfuncs.logfunc(f'Kik parser CSV read error ({file_found}): {e}')
    return headers, rows


def _write_report(report_folder, artifact_name, data_headers, data_list, source_file,
                  timeline_ts_col=None, html_no_escape=None):
    """Write HTML report, TSV, and optionally timeline for a Kik artifact.

    Files are written into a 'Kik' subfolder of report_folder so that
    RLEAPP's report.py derives SectionHeader='Kik' for icon lookup.
    """
    if not data_list:
        ilapfuncs.logfunc(f'Kik: No data found for {artifact_name}')
        return

    # Write into a Kik/ subfolder so report.py sets SectionHeader='Kik'
    kik_folder = os.path.join(report_folder, 'Kik')
    os.makedirs(kik_folder, exist_ok=True)

    report = ArtifactHtmlReport(artifact_name)
    report.start_artifact_report(kik_folder, artifact_name)
    report.add_script()
    if html_no_escape:
        report.write_artifact_data_table(data_headers, data_list, source_file,
                                         html_no_escape=html_no_escape)
    else:
        report.write_artifact_data_table(data_headers, data_list, source_file)
    report.end_artifact_report()

    ilapfuncs.tsv(report_folder, data_headers, data_list, artifact_name)

    if timeline_ts_col and timeline_ts_col in data_headers:
        ts_index = data_headers.index(timeline_ts_col)
        ilapfuncs.timeline(report_folder, artifact_name, data_list, [data_headers[ts_index]])


def _fallback_rows(headers, rows):
    """Return all columns as-is when schema is unknown or unexpected."""
    return headers, [tuple(row.get(h, '') for h in headers) for row in rows]


def _ms_epoch_to_utc(ms_value):
    """
    Convert a Unix epoch in milliseconds (13-digit integer) to a UTC string.
    Returns the original value as a string if conversion fails.
    Example: 1764622464103 -> '2025-12-01 20:54:24.103 UTC'
    """
    try:
        ms = int(ms_value)
        dt = datetime.fromtimestamp(ms / 1000.0, tz=timezone.utc)
        return dt.strftime('%Y-%m-%d %H:%M:%S.') + f'{ms % 1000:03d} UTC'
    except (ValueError, TypeError, OSError):
        return str(ms_value)


def _clean_path(path):
    """Strip Windows extended-length path prefix if present (\\\\?\\)."""
    p = str(path)
    if p.startswith('\\\\?\\'):
        return p[4:]
    return p


# ---------------------------------------------------------------------------
# Artifact functions
# ---------------------------------------------------------------------------

def get_kik_subscriber(files_found, report_folder, seeker, wrap_text):
    """
    subscriber-data-<username>_<id>.pdf
    Extracts key subscriber fields from the Kik legal return PDF using regex.
    Confirmed fields: First Name, Last Name, Email, Username, Registration Timestamp,
    Client Version, User Locale, User Location, Registration Client Info, Profile Pic URLs.
    """
    if not PDF_SUPPORT:
        ilapfuncs.logfunc(
            'Kik subscriber PDF: pdfminer.six not installed. '
            'Run: pip install pdfminer.six  then re-run RLEAPP.'
        )
        return

    # Regex patterns keyed to observed PDF format
    PATTERNS = [
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

    # Profile pic: pdfminer splits each entry across multiple lines and
    # may insert page-break content between the URL and its MD5 values.
    # Extract URLs and MD5 pairs independently then pair by index.
    PIC_URL_PATTERN = re.compile(
        r'https?://profilepics\.kik\.com/[^\s)]+\.jpg',
        re.IGNORECASE
    )
    # original MD5 may have a leading space after a newline
    # scaled MD5 for entry 2 may be separated by page-break content
    PIC_ORIG_MD5_PATTERN = re.compile(
        r'original MD5:\s*([A-F0-9]{32})',
        re.IGNORECASE
    )
    # 'scaled' and 'MD5:' may be separated by newlines and page-break
    # content (e.g. a CLIENT_VERSION line). Use lazy [\s\S]*? but anchor
    # to the literal 'MD5:' label so we don't overshoot into the next entry.
    PIC_SCALED_MD5_PATTERN = re.compile(
        r'scaled[\s\S]*? MD5:\s*([A-F0-9]{32})',
        re.IGNORECASE
    )

    # Event log lines: <date> <time> UTC <EVENT_TYPE> <value>
    # Exclude PROFILE_PIC_URL lines — those are handled in the pic table
    EVENT_PATTERN = re.compile(
        r'(\d{4}/\d{2}/\d{2}\s+\d{2}:\d{2}:\d{2}\s+UTC)\s+'
        r'(?!PROFILE_PIC_URL)([A-Z_]+)\s+(.+)'
    )

    for file_found in files_found:
        file_found = _clean_path(file_found)
        try:
            raw_text = pdf_extract_text(file_found)
        except Exception as e:
            ilapfuncs.logfunc(f'Kik subscriber PDF read error ({file_found}): {e}')
            continue

        if not raw_text:
            ilapfuncs.logfunc(f'Kik subscriber PDF: no text extracted from {file_found}')
            continue

        # ── Subscriber fields table ───────────────────────────────────
        sub_headers = ('Field', 'Value', 'Source File')
        sub_list = []
        for label, pattern in PATTERNS:
            m = re.search(pattern, raw_text, re.IGNORECASE)
            if m:
                sub_list.append((label, m.group(1).strip(), file_found))

        _write_report(report_folder, 'Kik - Subscriber Info', sub_headers, sub_list, file_found)

        # ── Profile picture URLs + MD5s ───────────────────────────────
        # pdfminer splits each entry across lines and may inject page-break
        # content between URL and MD5 values. Extract all three lists
        # independently and pair by index.
        pic_urls     = PIC_URL_PATTERN.findall(raw_text)
        pic_orig_md5s   = PIC_ORIG_MD5_PATTERN.findall(raw_text)
        pic_scaled_md5s = PIC_SCALED_MD5_PATTERN.findall(raw_text)

        pic_headers = ('Profile Pic URL', 'Original MD5', 'Scaled MD5', 'Source File')
        pic_list = []
        for i, url in enumerate(pic_urls):
            orig_md5   = pic_orig_md5s[i].upper()   if i < len(pic_orig_md5s)   else ''
            scaled_md5 = pic_scaled_md5s[i].upper() if i < len(pic_scaled_md5s) else ''
            pic_list.append((
                f'<a href="{url}" style="color:#4dabf7;">{url}</a>',
                orig_md5,
                scaled_md5,
                file_found
            ))

        if pic_list:
            _write_report(report_folder, 'Kik - Subscriber Profile Pics', pic_headers, pic_list,
                          file_found, html_no_escape=['Profile Pic URL'])

        # ── Raw event log table (all timestamped entries) ─────────────
        evt_headers = ('Timestamp (UTC)', 'Event Type', 'Value', 'Source File')
        evt_list = []
        for m in EVENT_PATTERN.finditer(raw_text):
            evt_list.append((m.group(1).strip(), m.group(2).strip(), m.group(3).strip(), file_found))

        if evt_list:
            _write_report(report_folder, 'Kik - Subscriber Events', evt_headers, evt_list, file_found,
                          timeline_ts_col='Timestamp (UTC)')


def get_kik_group_legend(files_found, report_folder, seeker, wrap_text):
    """
    group-legend-<username>_<id>.csv
    Confirmed schema: gid, name, code, public, deleted, last_join_ts, last_activity
    """
    for file_found in files_found:
        file_found = _clean_path(file_found)
        headers, rows = _open_csv(file_found)
        if not headers:
            continue

        EXPECTED = {'gid', 'name', 'code', 'public', 'deleted', 'last_join_ts', 'last_activity'}
        if not EXPECTED.issubset(set(headers)):
            ilapfuncs.logfunc(
                f'Kik group-legend: Unexpected schema. '
                f'Found: {headers}. Using raw fallback output.'
            )
            fb_headers, data_list = _fallback_rows(headers, rows)
            _write_report(report_folder, 'Kik - Group Legend', tuple(fb_headers), data_list, file_found)
            continue

        data_headers = (
            'Last Join', 'Last Activity', 'Group ID', 'Name', 'Code',
            'Public', 'Deleted', 'Source File'
        )
        data_list = []
        for row in rows:
            data_list.append((
                row.get('last_join_ts', ''),
                row.get('last_activity', ''),
                row.get('gid', ''),
                row.get('name', ''),
                row.get('code', ''),
                row.get('public', ''),
                row.get('deleted', ''),
                file_found
            ))

        _write_report(report_folder, 'Kik - Group Legend', data_headers, data_list, file_found,
                      timeline_ts_col='Last Join')


def get_kik_chat_text(files_found, report_folder, seeker, wrap_text):
    """
    package/content/data-text.csv
    Confirmed schema:
        id, content_id, filename, message, sender_id, receiver_id,
        ip, port, parent_id, sent_at, sent_at_ts, app_name
    """
    for file_found in files_found:
        file_found = _clean_path(file_found)
        headers, rows = _open_csv(file_found)
        if not headers:
            continue

        EXPECTED = {'id', 'message', 'sender_id', 'receiver_id', 'sent_at', 'sent_at_ts', 'app_name'}
        if not EXPECTED.issubset(set(headers)):
            ilapfuncs.logfunc(
                f'Kik data-text.csv: Unexpected schema. '
                f'Found headers: {headers}. Using raw fallback output.'
            )
            data_headers, data_list = _fallback_rows(headers, rows)
            _write_report(report_folder, 'Kik - Chat Messages (Text)', tuple(data_headers), data_list, file_found)
            continue

        data_headers = (
            'Sent At', 'Sent At (ms Epoch)', 'Sent At (Epoch UTC)',
            'Sender ID', 'Receiver ID', 'Message', 'App Name',
            'ID', 'Content ID', 'Filename', 'IP', 'Port', 'Parent ID', 'Source File'
        )
        data_list = []
        for row in rows:
            raw_ms = row.get('sent_at_ts', '')
            data_list.append((
                row.get('sent_at', ''),
                raw_ms,
                _ms_epoch_to_utc(raw_ms),
                row.get('sender_id', ''),
                row.get('receiver_id', ''),
                row.get('message', ''),
                row.get('app_name', ''),
                row.get('id', ''),
                row.get('content_id', ''),
                row.get('filename', ''),
                row.get('ip', ''),
                row.get('port', ''),
                row.get('parent_id', ''),
                file_found
            ))

        _write_report(report_folder, 'Kik - Chat Messages (Text)', data_headers, data_list, file_found,
                      timeline_ts_col='Sent At')


def get_kik_chat_media(files_found, report_folder, seeker, wrap_text):
    """
    package/content/data-media.csv  +  package/content/medias/*
    Confirmed schema: id, content_id, filename, message, sender_id, receiver_id,
                      ip, port, parent_id, sent_at, sent_at_ts, app_name

    files_found contains both the CSV and all media files.
    Builds a filename->path lookup from the media files, then renders
    inline <img>/<video> tags in the Media column of the HTML report.
    """
    # ── Separate the CSV from the media files ─────────────────────────
    csv_file = None
    media_lookup = {}  # basename -> absolute path
    for f in files_found:
        f = str(f)
        if f.endswith('data-media.csv'):
            csv_file = _clean_path(f)
        else:
            media_lookup[os.path.basename(f)] = _clean_path(f)

    if not csv_file:
        ilapfuncs.logfunc('Kik data-media.csv: CSV not found in files_found')
        return

    headers, rows = _open_csv(csv_file)
    if not headers:
        return

    EXPECTED = {'id', 'filename', 'sender_id', 'receiver_id', 'sent_at', 'sent_at_ts', 'app_name'}
    if not EXPECTED.issubset(set(headers)):
        ilapfuncs.logfunc(
            f'Kik data-media.csv: Unexpected schema. '
            f'Found headers: {headers}. Using raw fallback output.'
        )
        data_headers, data_list = _fallback_rows(headers, rows)
        _write_report(report_folder, 'Kik - Chat Messages (Media)', tuple(data_headers), data_list, csv_file)
        return

    def _media_tag(filename):
        """
        Return an HTML img or video tag pointing to the media file.
        RLEAPP extracts the zip into report_folder/data/..., so the media
        files already exist there. The artifact HTML lives in _HTML/, so
        the relative path is ../data/package/content/medias/<filename>.
        """
        if not filename:
            return ''
        if filename not in media_lookup:
            return filename  # not in return — show name only
        # Build relative path from _HTML/ to the data folder
        rel_path = '../data/package/content/medias/' + filename
        ext = os.path.splitext(filename)[1].lower()
        if ext in ('.mp4', '.mov', '.avi', '.3gp'):
            return (
                f'<video width="300" controls>'
                f'<source src="{rel_path}">'
                f'</video>'
            )
        else:
            return f'<img src="{rel_path}" width="300">'

    data_headers = (
        'Sent At', 'Sent At (ms Epoch)', 'Sent At (Epoch UTC)',
        'Sender ID', 'Receiver ID', 'Media', 'Media Filename', 'Message/Caption',
        'App Name', 'ID', 'Content ID', 'IP', 'Port', 'Parent ID', 'Source File'
    )
    data_list = []
    for row in rows:
        raw_ms = row.get('sent_at_ts', '')
        fname = row.get('filename', '')
        data_list.append((
            row.get('sent_at', ''),
            raw_ms,
            _ms_epoch_to_utc(raw_ms),
            row.get('sender_id', ''),
            row.get('receiver_id', ''),
            _media_tag(fname),
            fname,
            row.get('message', ''),
            row.get('app_name', ''),
            row.get('id', ''),
            row.get('content_id', ''),
            row.get('ip', ''),
            row.get('port', ''),
            row.get('parent_id', ''),
            csv_file
        ))

    _write_report(report_folder, 'Kik - Chat Messages (Media)', data_headers, data_list, csv_file,
                  timeline_ts_col='Sent At', html_no_escape=['Media'])


def _parse_log(files_found, report_folder, artifact_name, expected_cols, data_headers, row_builder):
    """
    Shared hardened parser for all logs/ CSV files.
    Falls back to raw column output if schema doesn't match expected.
    """
    for file_found in files_found:
        file_found = _clean_path(file_found)
        headers, rows = _open_csv(file_found)
        if not headers:
            continue
        if not expected_cols.issubset(set(headers)):
            ilapfuncs.logfunc(
                f'Kik {artifact_name}: Unexpected schema. '
                f'Found: {headers}. Using raw fallback output.'
            )
            fb_headers, data_list = _fallback_rows(headers, rows)
            _write_report(report_folder, artifact_name, tuple(fb_headers), data_list, file_found)
            continue
        data_list = [row_builder(row, file_found) for row in rows]
        _write_report(report_folder, artifact_name, data_headers, data_list, file_found,
                      timeline_ts_col='Timestamp')


# ---------------------------------------------------------------------------
# logs/chat_sent.csv
# Schema: user_jid, friend_user_jid, ip, ts, words
# ---------------------------------------------------------------------------
def get_kik_chat_sent(files_found, report_folder, seeker, wrap_text):
    _parse_log(
        files_found, report_folder,
        'Kik - Sent Chats (Log)',
        expected_cols={'user_jid', 'friend_user_jid', 'ip', 'ts', 'words'},
        data_headers=('Timestamp', 'User JID', 'Friend User JID', 'IP', 'Word Count', 'Source File'),
        row_builder=lambda r, f: (
            r.get('ts', ''),
            r.get('user_jid', ''),
            r.get('friend_user_jid', ''),
            r.get('ip', ''),
            r.get('words', ''),
            f
        )
    )


# ---------------------------------------------------------------------------
# logs/chat_sent_received.csv
# Schema: user_jid, friend_user_jid, ip, ts, words
# ---------------------------------------------------------------------------
def get_kik_chat_sent_received(files_found, report_folder, seeker, wrap_text):
    _parse_log(
        files_found, report_folder,
        'Kik - Sent & Received Chats (Log)',
        expected_cols={'user_jid', 'friend_user_jid', 'ip', 'ts', 'words'},
        data_headers=('Timestamp', 'User JID', 'Friend User JID', 'IP', 'Word Count', 'Source File'),
        row_builder=lambda r, f: (
            r.get('ts', ''),
            r.get('user_jid', ''),
            r.get('friend_user_jid', ''),
            r.get('ip', ''),
            r.get('words', ''),
            f
        )
    )


# ---------------------------------------------------------------------------
# logs/chat_platform_sent.csv
# Schema: user_jid, friend_user_jid, ip, ts, app_name, cid
# ---------------------------------------------------------------------------
def get_kik_chat_platform_sent(files_found, report_folder, seeker, wrap_text):
    _parse_log(
        files_found, report_folder,
        'Kik - Platform Chat Sent (Log)',
        expected_cols={'user_jid', 'friend_user_jid', 'ip', 'ts', 'app_name', 'cid'},
        data_headers=('Timestamp', 'User JID', 'Friend User JID', 'IP', 'App Name', 'CID', 'Source File'),
        row_builder=lambda r, f: (
            r.get('ts', ''),
            r.get('user_jid', ''),
            r.get('friend_user_jid', ''),
            r.get('ip', ''),
            r.get('app_name', ''),
            r.get('cid', ''),
            f
        )
    )


# ---------------------------------------------------------------------------
# logs/chat_platform_sent_received.csv
# Schema: user_jid, friend_user_jid, ip, ts, app_name, cid
# ---------------------------------------------------------------------------
def get_kik_chat_platform_sent_received(files_found, report_folder, seeker, wrap_text):
    _parse_log(
        files_found, report_folder,
        'Kik - Platform Chat Sent & Received (Log)',
        expected_cols={'user_jid', 'friend_user_jid', 'ip', 'ts', 'app_name', 'cid'},
        data_headers=('Timestamp', 'User JID', 'Friend User JID', 'IP', 'App Name', 'CID', 'Source File'),
        row_builder=lambda r, f: (
            r.get('ts', ''),
            r.get('user_jid', ''),
            r.get('friend_user_jid', ''),
            r.get('ip', ''),
            r.get('app_name', ''),
            r.get('cid', ''),
            f
        )
    )


# ---------------------------------------------------------------------------
# logs/group_receive.csv
# Schema: sender, receiver, ts, group_jid, sender_ip, sender_device_type,
#         cid, app_name, app, receive_ip, dt, epoch
# ---------------------------------------------------------------------------
def get_kik_group_receive(files_found, report_folder, seeker, wrap_text):
    _parse_log(
        files_found, report_folder,
        'Kik - Group Messages Received (Log)',
        expected_cols={'sender', 'receiver', 'ts', 'group_jid', 'sender_ip',
                       'sender_device_type', 'cid', 'app_name', 'app', 'receive_ip', 'dt', 'epoch'},
        data_headers=(
            'Timestamp', 'Epoch (ms)', 'Epoch (UTC)', 'Sender', 'Receiver', 'Group JID',
            'Sender IP', 'Receive IP', 'Sender Device Type',
            'App Name', 'App', 'CID', 'Source File'
        ),
        row_builder=lambda r, f: (
            r.get('ts', ''),
            r.get('epoch', ''),
            _ms_epoch_to_utc(r.get('epoch', '')),
            r.get('sender', ''),
            r.get('receiver', ''),
            r.get('group_jid', ''),
            r.get('sender_ip', ''),
            r.get('receive_ip', ''),
            r.get('sender_device_type', ''),
            r.get('app_name', ''),
            r.get('app', ''),
            r.get('cid', ''),
            f
        )
    )


# ---------------------------------------------------------------------------
# logs/group_send_msg_platform.csv
# Schema: sender, receiver, ts, group_jid, sender_ip, sender_device_type,
#         cid, app_name, app, receive_ip, dt, epoch
# ---------------------------------------------------------------------------
def get_kik_group_send(files_found, report_folder, seeker, wrap_text):
    _parse_log(
        files_found, report_folder,
        'Kik - Group Messages Sent (Log)',
        expected_cols={'sender', 'receiver', 'ts', 'group_jid', 'sender_ip',
                       'sender_device_type', 'cid', 'app_name', 'app', 'receive_ip', 'dt', 'epoch'},
        data_headers=(
            'Timestamp', 'Epoch (ms)', 'Epoch (UTC)', 'Sender', 'Receiver', 'Group JID',
            'Sender IP', 'Receive IP', 'Sender Device Type',
            'App Name', 'App', 'CID', 'Source File'
        ),
        row_builder=lambda r, f: (
            r.get('ts', ''),
            r.get('epoch', ''),
            _ms_epoch_to_utc(r.get('epoch', '')),
            r.get('sender', ''),
            r.get('receiver', ''),
            r.get('group_jid', ''),
            r.get('sender_ip', ''),
            r.get('receive_ip', ''),
            r.get('sender_device_type', ''),
            r.get('app_name', ''),
            r.get('app', ''),
            r.get('cid', ''),
            f
        )
    )


# ---------------------------------------------------------------------------
# logs/friends_added.csv
# Schema: user_jid, friend_user_jid, ts
# ---------------------------------------------------------------------------
def get_kik_friends_added(files_found, report_folder, seeker, wrap_text):
    _parse_log(
        files_found, report_folder,
        'Kik - Friends Added (Log)',
        expected_cols={'user_jid', 'friend_user_jid', 'ts'},
        data_headers=('Timestamp', 'User JID', 'Friend User JID', 'Source File'),
        row_builder=lambda r, f: (
            r.get('ts', ''),
            r.get('user_jid', ''),
            r.get('friend_user_jid', ''),
            f
        )
    )


# ---------------------------------------------------------------------------
# logs/block_user.csv
# Schema: user_jid, block_user_jid, ts
# ---------------------------------------------------------------------------
def get_kik_block_user(files_found, report_folder, seeker, wrap_text):
    _parse_log(
        files_found, report_folder,
        'Kik - Blocked Users (Log)',
        expected_cols={'user_jid', 'block_user_jid', 'ts'},
        data_headers=('Timestamp', 'User JID', 'Blocked User JID', 'Source File'),
        row_builder=lambda r, f: (
            r.get('ts', ''),
            r.get('user_jid', ''),
            r.get('block_user_jid', ''),
            f
        )
    )


# ---------------------------------------------------------------------------
# logs/binds.csv
# Schema: user_jid, ip, port, ts, device
# ---------------------------------------------------------------------------
def get_kik_binds(files_found, report_folder, seeker, wrap_text):
    _parse_log(
        files_found, report_folder,
        'Kik - Binds (Log)',
        expected_cols={'user_jid', 'ip', 'port', 'ts', 'device'},
        data_headers=('Timestamp', 'User JID', 'IP', 'Port', 'Device', 'Source File'),
        row_builder=lambda r, f: (
            r.get('ts', ''),
            r.get('user_jid', ''),
            r.get('ip', ''),
            r.get('port', ''),
            r.get('device', ''),
            f
        )
    )

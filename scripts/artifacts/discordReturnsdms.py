__artifacts_v2__ = {
    "discordReturnsdms": {
        "name": "Discord - Direct Messages",
        "description": "Direct messages from a Discord law enforcement return (messages/dms/*.csv).",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-12-04",
        "last_update_date": "2026-06-28",
        "requirements": "none",
        "category": "Discord Returns",
        "notes": "",
        "paths": ('*/attachments/*.*', '*/messages/dms/*.csv'),
        "output_types": "standard",
        "artifact_icon": "message-circle",
    }
}

import csv
import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc, check_in_media


def _discord_ts(value):
    value = (value or '').strip()
    if not value:
        return value
    if value.isdigit():
        return convert_unix_ts_to_utc(int(value))
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)
    except ValueError:
        return value


def _media_refs(field):
    refs = []
    for part in (field or '').split('\n'):
        part = part.strip()
        if not part:
            continue
        segs = part.split('/')
        attachment_id = segs[-2] if len(segs) >= 2 else part
        ref = check_in_media(attachment_id, attachment_id)
        if ref:
            refs.append(ref)
    return refs


@artifact_processor
def discordReturnsdms(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('.csv') or os.path.basename(file_found).startswith('._'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8', errors='backslashreplace') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader, None)  # header
            for item in reader:
                if len(item) < 7:
                    continue
                data_list.append((_discord_ts(item[3]), item[4], item[5], _media_refs(item[6]),
                                  item[1], item[0], item[2]))

    data_headers = (('Timestamp', 'datetime'), 'Username', 'Contents', ('Media', 'media'), 'ID',
                    'Channel ID', 'Author ID')
    return data_headers, data_list, context.get_relative_path(source_path)

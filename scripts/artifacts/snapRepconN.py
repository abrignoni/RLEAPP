__artifacts_v2__ = {
    "snapRepconN": {
        "name": "Snapchat - Reported Conversations",
        "description": "Reported conversations parsed from a Snapchat law enforcement return (reported_conversations.csv).",
        "author": "@AlexisBrignoni",
        "creation_date": "2024-06-13",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Snapchat Returns",
        "notes": "",
        "paths": ('*/reported_conversations.csv', '*/*.*'),
        "output_types": "standard",
        "artifact_icon": "flag",
    }
}

import csv
import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, check_in_media

_MONTHS = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
           'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}


def _snap_ts(value):
    parts = (value or '').split(' ')
    try:
        return datetime(int(parts[5]), _MONTHS[parts[1]], int(parts[2]),
                        *(int(x) for x in parts[3].split(':')), tzinfo=timezone.utc)
    except (IndexError, KeyError, ValueError):
        return value


def _read_multiline_csv(file_path):
    rows = []
    start = False
    with open(file_path, 'r', newline='', encoding='utf-8') as f:
        for row in csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL):
            if start:
                rows.append(row)
            elif '===========================' in row:
                start = True
    return rows


@artifact_processor
def snapRepconN(context):
    ts_idx, msg_ts_idx, media_idx = 15, 8, 13
    data_headers = (('Timestamp', 'datetime'), 'Reporter_user_id', 'Reason', 'Context',
                    'Reported_user_id', 'Reported_profile_type', 'Conversation_id',
                    'Reported_message_id', ('Message_timestamp', 'datetime'), 'Message_id',
                    'Sender_user_id', 'Sender_username', 'Text', 'Media_id', 'Reply_to_message_id',
                    'Message_type', ('Media', 'media'))
    non_media = len(data_headers) - 1

    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).startswith('reported_conversations.csv'):
            continue
        source_path = file_found
        rows = _read_multiline_csv(file_found)
        for raw in rows[1:]:
            if len(raw) <= ts_idx:
                continue
            entry = list(raw)
            entry.insert(0, _snap_ts(entry[ts_idx]))
            del entry[ts_idx + 1]
            if len(entry) > msg_ts_idx:
                entry[msg_ts_idx] = _snap_ts(entry[msg_ts_idx])
            media_raw = entry[media_idx] if len(entry) > media_idx else ''
            media_parts = media_raw.split(':')
            media_val = media_parts[1] if len(media_parts) > 1 else media_raw
            refs = [r for r in (check_in_media(m.strip(), m.strip())
                                for m in media_val.split(';') if m.strip()) if r]
            entry = (entry + [''] * non_media)[:non_media]
            entry.append(refs)
            data_list.append(entry)

    return data_headers, data_list, context.get_relative_path(source_path)

__artifacts_v2__ = {
    "snapChathistory": {
        "name": "Snapchat - Chat History",
        "description": "Chat history from a Snapchat data archive (chat_history.json).",
        "author": "@AlexisBrignoni",
        "creation_date": "2022-04-05",
        "last_update_date": "2026-07-03",
        "requirements": "none",
        "category": "Snapchat Archive",
        "notes": "",
        "paths": ('*/chat_history.json',),
        "output_types": "standard",
        "artifact_icon": "message-square",
        "data_views": {
            "conversation": {
                "conversationDiscriminatorColumn": "Other Party",
                "textColumn": "Text",
                "directionColumn": "Direction",
                "directionSentValue": "Sent",
                "timeColumn": "Timestamp",
                "senderColumn": "Other Party",
                "sentMessageStaticLabel": "Local User"
            }
        },
    }
}

import json
import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc

_MONTHS = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
           'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}


def _snap_ts(value):
    # Snapchat archive timestamps vary: ISO ('2021-08-19 12:00:00 UTC'), epoch, or
    # the return-style 'Wed Aug 19 12:00:00 UTC 2021'. Best-effort to aware UTC, else raw.
    value = (value or '').strip()
    if not value:
        return value
    cleaned = value.replace(' UTC', '').strip()
    if cleaned.isdigit():
        return convert_unix_ts_to_utc(int(cleaned))
    try:
        dt = datetime.fromisoformat(cleaned.replace('Z', '+00:00'))
        return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)
    except ValueError:
        pass
    try:
        parts = value.split(' ')
        return datetime(int(parts[-1]), _MONTHS[parts[1]], int(parts[2]),
                        *(int(x) for x in parts[3].split(':')), tzinfo=timezone.utc)
    except (IndexError, KeyError, ValueError):
        return value


@artifact_processor
def snapChathistory(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).startswith('chat_history.json'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as fp:
            data = json.load(fp)

        for conv_type, messages in data.items():
            for mess in messages:
                if mess.get('From'):
                    directionality = 'From: ' + mess['From']
                    direction = 'Received'
                    other_party = mess['From']
                elif mess.get('To'):
                    directionality = 'To: ' + mess['To']
                    direction = 'Sent'
                    other_party = mess['To']
                else:
                    directionality = ''
                    direction = ''
                    other_party = ''
                data_list.append((_snap_ts(mess.get('Created', '')), directionality,
                                  mess.get('Text', ''), mess.get('Media Type', ''), conv_type,
                                  direction, other_party))

    data_headers = (('Timestamp', 'datetime'), 'Directionality', 'Text', 'Media Type',
                    'Message Type', 'Direction', 'Other Party')
    return data_headers, data_list, context.get_relative_path(source_path)

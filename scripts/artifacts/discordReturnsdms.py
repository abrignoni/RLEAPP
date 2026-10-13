__artifacts_v2__ = {
    "discordReturnsdms": {
        "name": "Discord - Direct Messages",
        "description": "Direct messages from a Discord law enforcement return "
                       "(messages/dms/*.csv). Columns are named by position; the file's own header "
                       "row is not read.",
        "author": "@AlexisBrignoni, @Snoop168",
        "creation_date": "2021-12-04",
        "last_update_date": "2026-10-13",
        "requirements": "none",
        "category": "Discord Returns",
        "notes": "Columns are assigned by position after the header row is skipped; the header "
                 "names are not read. ID is taken from the second column and Channel ID from the "
                 "first, the reverse of the Discord server and unknown-folder readers, which "
                 "take ID from the first and Channel ID from the second. Which order a return "
                 "uses was not checked: no test return is available, so one of the two orders "
                 "may be wrong.",
        "paths": ('*/attachments/*.*', '*/messages/dms/*.csv', '*/content/user_metadata/user.json'),
        "output_types": "standard",
        "artifact_icon": "message-circle",
        "data_views": {
            "conversation": {
                "conversationDiscriminatorColumn": "Channel ID",
                "conversationLabelColumn": "Channel ID",
                "textColumn": "Contents",
                "directionColumn": "Direction",
                "directionSentValue": "Sent",
                "timeColumn": "Timestamp",
                "senderColumn": "Username",
                "mediaColumn": "Media"
            }
        }
    }
}

import csv
import os
from datetime import datetime, timezone
import json

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


def _media_refs(field, sender, message_id):
    refs = []
    for part in (field or '').split('\n'):
        part = part.strip()
        if not part:
            continue
        segs = part.split('/')
        filename = segs[-1].split('?')[0]
        media_filename = '_'.join([segs[-3], message_id, segs[-2], filename])
        media_path = '/'.join([segs[-3], sender, media_filename])
        ref = check_in_media(media_path, media_filename)
        if ref:
            refs.append(ref)
    return refs


@artifact_processor
def discordReturnsdms(context):
    data_list = []
    source_path = ''
    local_user_id = None
    for file_found in context.get_files_found():
        if not file_found.endswith('user.json') or os.path.basename(file_found).startswith('._'):
            continue
        with open(file_found, encoding='utf-8', errors='backslashreplace') as f:
            data = json.load(f)
            local_user_id = data.get('id')

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
                author_id = item[2]
                message_id = item[1]
                direction = "Unknown" if not local_user_id else "Sent" if local_user_id == author_id else "Received"
                data_list.append((_discord_ts(item[3]), direction, item[4], item[5], _media_refs(item[6], author_id, message_id),
                                  message_id, item[0], author_id))

    data_headers = (('Timestamp', 'datetime'), 'Direction', 'Username', 'Contents', ('Media', 'media'), 'ID',
                    'Channel ID', 'Author ID')
    return data_headers, data_list, context.get_relative_path(source_path)

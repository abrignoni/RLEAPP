__artifacts_v2__ = {
    "get_fb_messages": {
        "name": "Messages",
        "description": "Processes messages from a facebook messenger JSON export",
        "author": "@C_Peter",
        "creation_date": "2026-06-01",
        "last_update_date": "2026-06-01",
        "requirements": "none",
        "category": "Facebook Messenger",
        "notes": "",
        "paths": ('*/*.json','*/media/*',),
        "output_types": "standard",
        'artifact_icon': 'message',
        'data_views': {
            'conversation': {
                'conversationDiscriminatorColumn': 'Thread',
                'conversationLabelColumn': 'Thread',
                'textColumn': 'Message',
                'directionColumn': 'Outgoing',
                'directionSentValue': 1,
                'timeColumn': 'Timestamp',
                'senderColumn': 'Sender',
                'mediaColumn': 'Attachment File'
            }
        }
    }
}

import os
import datetime
import json
from scripts.ilapfuncs import artifact_processor, \
    check_in_media

@artifact_processor
def get_fb_messages(context):
    """Extracts chat messages from a Facebook Messenger JSON export"""
    files_found = context.get_files_found()
    data_list = []
    source_path = "messages"
    for file_found in files_found:
        file_found = str(file_found)
        filename = os.path.basename(file_found)

        if filename.endswith('.json'):

            with open(file_found, "r", encoding='utf-8') as fp:
                deserialized = json.load(fp)

            participants = deserialized.get('participants')
            owner = participants[0]
            without_owner = [p for p in participants if p != owner]
            without_owner = ", ".join(without_owner)

            thread = deserialized.get('threadName')

            for x in deserialized['messages']:
                sender_name = x.get('senderName', '')
                unsent = x.get('isUnsent', '')
                timestamp = x.get('timestamp', '')
                time_utc = datetime.datetime.fromtimestamp(timestamp/1000, tz=datetime.timezone.utc)
                message = x.get('text', '')
                media = x.get('media', None)
                if media:
                    for entry in media:
                        fpath = entry.get("uri")
                        if "Failed to download media" in fpath:
                            attach_file = None
                        else:
                            attach_file = check_in_media(fpath, fpath)
                else:
                    attach_file = None
                if sender_name == owner:
                    out = 1
                    receiver = without_owner
                else:
                    out = 0
                    without_sender = [p for p in participants if p != sender_name]
                    receiver = ", ".join(without_sender)
                data_list.append((time_utc, thread, sender_name, receiver, message, attach_file, out, unsent))

    data_headers = (('Timestamp', 'datetime'), "Thread", "Sender", "Receiver", "Message", ('Attachment File', 'media'), "Outgoing", "Unsent")

    return data_headers, data_list, source_path

__artifacts_v2__ = {
    "instagramPolls": {
        "name": "Instagram Archive - Polls",
        "description": "Parses story poll interactions from an Instagram data archive (polls.json)",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-27",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Instagram Archive",
        "notes": "",
        "paths": ('*/story_sticker_interactions/polls.json'),
        "output_types": "standard",
        "artifact_icon": "brand-instagram",
    }
}

import os
import json

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


@artifact_processor
def instagramPolls(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found).startswith('polls.json'):
            source_path = file_found
            with open(file_found, 'r', encoding='utf-8') as fp:
                deserialized = json.load(fp)

            for x in deserialized['story_activities_polls']:
                user = x.get('title', '')
                timestamp = x['string_list_data'][0].get('timestamp', '')
                timestamp = convert_unix_ts_to_utc(timestamp) if timestamp else ''
                data_list.append((timestamp, user))

    data_headers = (('Timestamp', 'datetime'), 'User')
    return data_headers, data_list, context.get_relative_path(source_path)

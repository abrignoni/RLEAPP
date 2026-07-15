__artifacts_v2__ = {
    "instagramPasswordchange": {
        "name": "Instagram Archive - Password Change",
        "description": "Parses password change activity from an Instagram data archive (password_change_activity.json)",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-27",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Instagram Archive",
        "notes": "",
        "paths": ('*/login_and_account_creation/password_change_activity.json'),
        "output_types": "standard",
        "artifact_icon": "brand-instagram",
    }
}

import os
import json

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


@artifact_processor
def instagramPasswordchange(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found).startswith('password_change_activity.json'):
            source_path = file_found
            with open(file_found, 'r', encoding='utf-8') as fp:
                deserialized = json.load(fp)

            for x in deserialized['account_history_password_change_history']:
                timestamp = x['string_map_data']['Time'].get('timestamp', '')
                timestamp = convert_unix_ts_to_utc(timestamp) if timestamp else ''
                data_list.append((timestamp,))

    data_headers = (('Timestamp', 'datetime'),)
    return data_headers, data_list, context.get_relative_path(source_path)

__artifacts_v2__ = {
    "instagramPrivacychange": {
        "name": "Instagram Archive - Privacy Change",
        "description": "Parses account privacy changes from an Instagram data archive (account_privacy_changes.json)",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-27",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Instagram Archive",
        "notes": "",
        "paths": ('*/login_and_account_creation/account_privacy_changes.json'),
        "output_types": "standard",
        "artifact_icon": "instagram",
    }
}

import os
import json

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


@artifact_processor
def instagramPrivacychange(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found).startswith('account_privacy_changes.json'):
            source_path = file_found
            with open(file_found, 'r', encoding='utf-8') as fp:
                deserialized = json.load(fp)

            for x in deserialized['account_history_account_privacy_history']:
                title = x.get('title', '')
                timestamp = x['string_map_data']['Time'].get('timestamp', '')
                timestamp = convert_unix_ts_to_utc(timestamp) if timestamp else ''
                data_list.append((timestamp, title))

    data_headers = (('Timestamp', 'datetime'), 'Title')
    return data_headers, data_list, context.get_relative_path(source_path)

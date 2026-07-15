__artifacts_v2__ = {
    "instagramSuggestedviewed": {
        "name": "Instagram Archive - Suggested Accounts Viewed",
        "description": "Parses suggested accounts viewed from an Instagram data archive (suggested_accounts_viewed.json)",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-27",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Instagram Archive",
        "notes": "",
        "paths": ('*/ads_and_content/suggested_accounts_viewed.json'),
        "output_types": "standard",
        "artifact_icon": "brand-instagram",
    }
}

import os
import json

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


@artifact_processor
def instagramSuggestedviewed(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found).startswith('suggested_accounts_viewed.json'):
            source_path = file_found
            with open(file_found, 'r', encoding='utf-8') as fp:
                deserialized = json.load(fp)

            for x in deserialized['impressions_history_chaining_seen']:
                username = x['string_map_data']['Username'].get('value', '')
                timestamp = x['string_map_data']['Time'].get('timestamp', '')
                timestamp = convert_unix_ts_to_utc(timestamp) if timestamp else ''
                data_list.append((timestamp, username))

    data_headers = (('Timestamp', 'datetime'), 'Username')
    return data_headers, data_list, context.get_relative_path(source_path)

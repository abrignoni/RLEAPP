__artifacts_v2__ = {
    "instagramNointerest": {
        "name": "Instagram Archive - Accounts No Interest",
        "description": "Parses accounts the user marked as not interested from an Instagram data archive",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-27",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Instagram Archive",
        "notes": "",
        "paths": ('*/ads_and_content/*re_not_interested_in.json'),
        "output_types": "standard",
        "artifact_icon": "instagram",
    }
}

import os
import json

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


@artifact_processor
def instagramNointerest(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found).startswith("accounts_you're_not_interested_in.json"):
            source_path = file_found
            with open(file_found, 'r', encoding='utf-8') as fp:
                deserialized = json.load(fp)

            for x in deserialized['impressions_history_recs_hidden_authors']:
                value = x['string_map_data']['Username'].get('value', '')
                timestamp = x['string_map_data']['Time'].get('timestamp', '')
                timestamp = convert_unix_ts_to_utc(timestamp) if timestamp else ''
                data_list.append((timestamp, value))

    data_headers = (('Timestamp', 'datetime'), 'Username')
    return data_headers, data_list, context.get_relative_path(source_path)

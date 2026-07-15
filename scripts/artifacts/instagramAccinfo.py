__artifacts_v2__ = {
    "instagramAccinfo": {
        "name": "Instagram Archive - Account Info",
        "description": "Parses profile account insights from an Instagram data archive (account_information.json)",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-20",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Instagram Archive",
        "notes": "",
        "paths": ('*/account_information/account_information.json'),
        "output_types": "standard",
        "artifact_icon": "brand-instagram",
    }
}

import os
import json

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


@artifact_processor
def instagramAccinfo(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found).startswith('account_information.json'):
            source_path = file_found
            with open(file_found, 'r', encoding='utf-8') as fp:
                deserialized = json.load(fp)

            for x in deserialized['profile_account_insights']:
                for values in x.values():
                    if not values:
                        continue
                    for insights_cat, b in values.items():
                        href = b.get('href', '')
                        value = b.get('value', '')
                        timestamp = b.get('timestamp', '')
                        timestamp = convert_unix_ts_to_utc(timestamp) if timestamp else ''
                        data_list.append((insights_cat, timestamp, value, href))

    data_headers = ('Insights Category', ('Timestamp', 'datetime'), 'Value', 'Href')
    return data_headers, data_list, context.get_relative_path(source_path)

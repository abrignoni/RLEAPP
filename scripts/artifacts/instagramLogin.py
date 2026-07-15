__artifacts_v2__ = {
    "instagramLogin": {
        "name": "Instagram Archive - Login Activity",
        "description": "Parses login activity from an Instagram data archive (login_activity.json)",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-21",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Instagram Archive",
        "notes": "",
        "paths": ('*/login_and_account_creation/login_activity.json'),
        "output_types": "standard",
        "artifact_icon": "brand-instagram",
    }
}

import os
import json

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


@artifact_processor
def instagramLogin(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found).startswith('login_activity.json'):
            source_path = file_found
            with open(file_found, 'r', encoding='utf-8') as fp:
                deserialized = json.load(fp)

            for x in deserialized['account_history_login_history']:
                smd = x['string_map_data']
                title = x.get('title', '')
                cookiename = smd['Cookie Name'].get('value', '')
                ipaddress = smd['IP Address'].get('value', '')
                langagecode = smd['Language Code'].get('value', '')
                timestamp = smd['Time'].get('timestamp', '')
                useragent = smd['User Agent'].get('value', '')
                timestamp = convert_unix_ts_to_utc(timestamp) if timestamp else ''
                data_list.append((timestamp, title, ipaddress, useragent, langagecode, cookiename))

    data_headers = (('Timestamp', 'datetime'), 'Title', 'IP Address', 'User Agent', 'Language Code', 'Cookie Name')
    return data_headers, data_list, context.get_relative_path(source_path)

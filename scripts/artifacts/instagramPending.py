__artifacts_v2__ = {
    "instagramPending": {
        "name": "Instagram Archive - Pending Follow Req",
        "description": "Parses pending follow requests sent from an Instagram data archive (pending_follow_requests.json)",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-27",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Instagram Archive",
        "notes": "",
        "paths": ('*/followers_and_following/pending_follow_requests.json'),
        "output_types": "standard",
        "artifact_icon": "brand-instagram",
    }
}

import os
import json

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


@artifact_processor
def instagramPending(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found).startswith('pending_follow_requests.json'):
            source_path = file_found
            with open(file_found, 'r', encoding='utf-8') as fp:
                deserialized = json.load(fp)

            for x in deserialized['relationships_follow_requests_sent']:
                entry = x['string_list_data'][0]
                href = entry.get('href', '')
                value = entry.get('value', '')
                timestamp = entry.get('timestamp', '')
                timestamp = convert_unix_ts_to_utc(timestamp) if timestamp else ''
                data_list.append((timestamp, value, href))

    data_headers = (('Timestamp', 'datetime'), 'User', 'Href')
    return data_headers, data_list, context.get_relative_path(source_path)

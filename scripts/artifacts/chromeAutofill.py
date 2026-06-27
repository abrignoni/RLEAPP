__artifacts_v2__ = {
    "chromeAutofill": {
        "name": "Chrome Autofill",
        "description": "Parses Google Chrome Autofill value information from Takeout",
        "author": "@upintheairsheep & @KevinPagano3",
        "creation_date": "2023-08-18",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": ('*/Chrome/Autofill.json'),
        "output_types": "standard",
        "artifact_icon": "edit-3",
    }
}

import json
import os

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


@artifact_processor
def chromeAutofill(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found) != 'Autofill.json':
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            data = json.load(f)

        for site in data.get('Autofill', []):
            name = site.get('name', '')
            value = site.get('value', '')
            for stamp in site.get('usage_timestamp', []):
                # Chrome/WebKit epoch: microseconds since 1601-01-01 -> Unix seconds
                timestamp = (int(stamp) / 1000000) - 11644473600 if stamp else ''
                timestamp = convert_unix_ts_to_utc(timestamp) if timestamp else ''
                data_list.append((timestamp, name, value))

    data_headers = (('Usage Timestamp', 'datetime'), 'Field Type', 'Typed Value')
    return data_headers, data_list, context.get_relative_path(source_path)

__artifacts_v2__ = {
    "chromeHistory": {
        "name": "Chrome Web History",
        "description": "Parses Google Chrome History from Takeout",
        "author": "@KevinPagano3",
        "creation_date": "2021-08-20",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": ('*/Chrome/BrowserHistory.json'),
        "output_types": "standard",
        "artifact_icon": "chrome",
    }
}

import json
import os

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


@artifact_processor
def chromeHistory(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found) != 'BrowserHistory.json':
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            data = json.load(f)

        for site in data.get('Browser History', []):
            timestamp = site.get('time_usec', '')
            timestamp = convert_unix_ts_to_utc(timestamp) if timestamp else ''
            data_list.append((timestamp, site.get('title', ''), site.get('url', ''),
                              site.get('page_transition', '')))

    data_headers = (('Timestamp', 'datetime'), 'Webpage Title', 'URL', 'Page Transition')
    return data_headers, data_list, context.get_relative_path(source_path)

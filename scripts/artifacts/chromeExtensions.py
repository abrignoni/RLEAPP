__artifacts_v2__ = {
    "chromeExtensions": {
        "name": "Chrome Extensions",
        "description": "Parses Google Chrome Extensions from Takeout",
        "author": "@KevinPagano3",
        "creation_date": "2021-08-20",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": ('*/Chrome/Extensions.json'),
        "output_types": "standard",
        "artifact_icon": "package",
    }
}

import json
import os

from scripts.ilapfuncs import artifact_processor


@artifact_processor
def chromeExtensions(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found) != 'Extensions.json':
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            data = json.load(f)

        for site in data.get('Extensions', []):
            data_list.append((site.get('name', ''), site.get('version', ''), site.get('id', ''),
                              site.get('enabled', ''), site.get('incognito_enabled', ''),
                              site.get('remote_install', '')))

    data_headers = ('Name', 'Version', 'ID', 'Enabled', 'Incognito Enabled', 'Remote Install')
    return data_headers, data_list, context.get_relative_path(source_path)

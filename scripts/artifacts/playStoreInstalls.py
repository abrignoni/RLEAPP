__artifacts_v2__ = {
    "playStoreInstalls": {
        "name": "Google Play Store Installs",
        "description": "List of your Google Play app installs.",
        "author": "@KevinPagano3",
        "creation_date": "2021-08-22",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": ('*/Google Play Store/Installs.json'),
        "output_types": "standard",
        "artifact_icon": "download",
    }
}

import json
import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor


def _iso_to_utc(value):
    if not value:
        return value
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(timezone.utc)
    except (ValueError, AttributeError):
        return value


@artifact_processor
def playStoreInstalls(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found) != 'Installs.json':
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            data = json.load(f)

        for x in data:
            install = x.get('install', {})
            doc = install.get('doc', {})
            device_attr = install.get('deviceAttribute', {})
            data_list.append((
                _iso_to_utc(install.get('firstInstallationTime', '')),
                _iso_to_utc(install.get('lastUpdateTime', '')),
                doc.get('title', ''), doc.get('documentType', ''),
                device_attr.get('manufacturer', ''), device_attr.get('model', ''),
                device_attr.get('carrier', ''), device_attr.get('deviceDisplayName', '')))

    data_headers = (('First Install Timestamp', 'datetime'), ('Last Update Timestamp', 'datetime'),
                    'Title', 'Type', 'Device Manufacturer', 'Device Model', 'Carrier',
                    'Device Display Name')
    return data_headers, data_list, context.get_relative_path(source_path)

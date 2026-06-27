__artifacts_v2__ = {
    "chromeDeviceInfo": {
        "name": "Chrome Device Info",
        "description": "Parses Google Chrome synced device information from Takeout",
        "author": "@KevinPagano3",
        "creation_date": "2023-08-24",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": ('*/Chrome/Device Information.json'),
        "output_types": "standard",
        "artifact_icon": "smartphone",
    }
}

import json

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


@artifact_processor
def chromeDeviceInfo(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            data = json.load(f)

        for device in data.get('Device Info', []):
            last_updated = device.get('last_updated_timestamp', '')
            last_updated = convert_unix_ts_to_utc(last_updated) if last_updated else ''
            manufacturer = device.get('manufacturer', '')
            model = device.get('model', '')
            client_name = device.get('client_name', '')
            os_type = device.get('os_type', '')[8:]
            device_type = device.get('device_type', '')[5:]
            chrome_version = device.get('chrome_version', '')
            sync_user_agent = device.get('sync_user_agent', '')
            signin_scoped_device_id = device.get('signin_scoped_device_id', '')
            data_list.append((last_updated, manufacturer, model, client_name, os_type,
                              device_type, chrome_version, sync_user_agent, signin_scoped_device_id))

    data_headers = (('Last Updated Timestamp', 'datetime'), 'Manufacturer', 'Model', 'Client Name',
                    'OS Type', 'Device Type', 'Chrome Version', 'User Agent', 'Device ID')
    return data_headers, data_list, context.get_relative_path(source_path)

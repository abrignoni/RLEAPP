__artifacts_v2__ = {
    "snapArchiveBasicInfo": {
        "name": "Snapchat - Account Basic Info",
        "description": "Account basic information from a Snapchat data archive (account.json).",
        "author": "@AlexisBrignoni", "creation_date": "2023-12-11",
        "last_update_date": "2026-06-28", "requirements": "none",
        "category": "Snapchat Archive", "notes": "",
        "paths": ('*/account.json',), "output_types": "standard", "artifact_icon": "user",
    },
    "snapArchiveDeviceInfo": {
        "name": "Snapchat - Device Information",
        "description": "Device information from a Snapchat data archive (account.json).",
        "author": "@AlexisBrignoni", "creation_date": "2023-12-11",
        "last_update_date": "2026-06-28", "requirements": "none",
        "category": "Snapchat Archive", "notes": "",
        "paths": ('*/account.json',), "output_types": "standard", "artifact_icon": "smartphone",
    },
    "snapArchiveDeviceHistory": {
        "name": "Snapchat - Device History",
        "description": "Device history from a Snapchat data archive (account.json).",
        "author": "@AlexisBrignoni", "creation_date": "2023-12-11",
        "last_update_date": "2026-06-28", "requirements": "none",
        "category": "Snapchat Archive", "notes": "",
        "paths": ('*/account.json',), "output_types": "standard", "artifact_icon": "clock",
    },
    "snapArchiveLoginHistory": {
        "name": "Snapchat - Login History",
        "description": "Login history from a Snapchat data archive (account.json).",
        "author": "@AlexisBrignoni", "creation_date": "2023-12-11",
        "last_update_date": "2026-06-28", "requirements": "none",
        "category": "Snapchat Archive", "notes": "",
        "paths": ('*/account.json',), "output_types": "standard", "artifact_icon": "log-in",
    }
}

import json
import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc

_MONTHS = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
           'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}


def _snap_ts(value):
    value = (value or '').strip()
    if not value:
        return value
    cleaned = value.replace(' UTC', '').strip()
    if cleaned.isdigit():
        return convert_unix_ts_to_utc(int(cleaned))
    try:
        dt = datetime.fromisoformat(cleaned.replace('Z', '+00:00'))
        return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)
    except ValueError:
        pass
    try:
        parts = value.split(' ')
        return datetime(int(parts[-1]), _MONTHS[parts[1]], int(parts[2]),
                        *(int(x) for x in parts[3].split(':')), tzinfo=timezone.utc)
    except (IndexError, KeyError, ValueError):
        return value


def _account_json(context):
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found).startswith('account.json'):
            with open(file_found, encoding='utf-8') as fp:
                return file_found, json.load(fp)
    return '', {}


@artifact_processor
def snapArchiveBasicInfo(context):
    source_path, data = _account_json(context)
    data_list = []
    bi = data.get('Basic Information')
    if bi:
        data_list.append((_snap_ts(bi.get('Creation Date', '')), bi.get('Username', ''),
                          bi.get('Name', ''), bi.get('Registration IP', ''), bi.get('Country', ''),
                          bi.get('PhoneNumber', ''), bi.get('Carrier', '')))
    data_headers = (('Timestamp', 'datetime'), 'Username', 'Name', 'Registration IP', 'Country',
                    ('Phone Number', 'phonenumber'), 'Carrier')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def snapArchiveDeviceInfo(context):
    source_path, data = _account_json(context)
    data_list = []
    di = data.get('Device Information')
    if di:
        data_list.append((di.get('Make', ''), di.get('Model ID', ''), di.get('Model Name', ''),
                          di.get('User Agent', ''), di.get('Language', ''), di.get('OS Type', ''),
                          di.get('OS Version', ''), di.get('Connection Type', '')))
    data_headers = ('Make', 'Model ID', 'Model Name', 'User Agent', 'Language', 'OS Type',
                    'OS Version', 'Connection Type')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def snapArchiveDeviceHistory(context):
    source_path, data = _account_json(context)
    data_list = []
    for item in data.get('Device History', []):
        data_list.append((_snap_ts(item.get('Start Time', '')), item.get('Make', ''),
                          item.get('Model', ''), item.get('Device Type', '')))
    data_headers = (('Start Time', 'datetime'), 'Make', 'Model', 'Device Type')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def snapArchiveLoginHistory(context):
    source_path, data = _account_json(context)
    data_list = []
    for item in data.get('Login History', []):
        data_list.append((_snap_ts(item.get('Created', '')), item.get('IP', ''),
                          item.get('Country', ''), item.get('Status', ''), item.get('Device', '')))
    data_headers = (('Timestamp', 'datetime'), 'IP', 'Country', 'Status', 'Device')
    return data_headers, data_list, context.get_relative_path(source_path)

__artifacts_v2__ = {
    "snapSubAccountInfo": {
        "name": "Snapchat - Account Information",
        "description": "Account information from a Snapchat law enforcement return (subscriber_info.csv).",
        "author": "@AlexisBrignoni", "creation_date": "2024-06-13",
        "last_update_date": "2026-06-27", "requirements": "none",
        "category": "Snapchat Returns", "notes": "",
        "paths": ('*/subscriber_info.csv',), "output_types": "standard", "artifact_icon": "user",
    },
    "snapSubHistory": {
        "name": "Snapchat - Account Change History",
        "description": "Account change history from a Snapchat law enforcement return (subscriber_info.csv).",
        "author": "@AlexisBrignoni", "creation_date": "2024-06-13",
        "last_update_date": "2026-06-27", "requirements": "none",
        "category": "Snapchat Returns", "notes": "",
        "paths": ('*/subscriber_info.csv',), "output_types": "standard", "artifact_icon": "clock",
    },
    "snapSubValueChanges": {
        "name": "Snapchat - Value Changes",
        "description": "Value changes from a Snapchat law enforcement return (subscriber_info.csv).",
        "author": "@AlexisBrignoni", "creation_date": "2024-06-13",
        "last_update_date": "2026-06-27", "requirements": "none",
        "category": "Snapchat Returns", "notes": "",
        "paths": ('*/subscriber_info.csv',), "output_types": "standard", "artifact_icon": "edit",
    },
    "snapSubDetails": {
        "name": "Snapchat - Account Details",
        "description": "Account details from a Snapchat law enforcement return (subscriber_info.csv).",
        "author": "@AlexisBrignoni", "creation_date": "2024-06-13",
        "last_update_date": "2026-06-27", "requirements": "none",
        "category": "Snapchat Returns", "notes": "",
        "paths": ('*/subscriber_info.csv',), "output_types": "standard", "artifact_icon": "info",
    },
    "snapSubPrivacy": {
        "name": "Snapchat - Privacy Settings",
        "description": "Privacy settings from a Snapchat law enforcement return (subscriber_info.csv).",
        "author": "@AlexisBrignoni", "creation_date": "2024-06-13",
        "last_update_date": "2026-06-27", "requirements": "none",
        "category": "Snapchat Returns", "notes": "",
        "paths": ('*/subscriber_info.csv',), "output_types": "standard", "artifact_icon": "lock",
    },
    "snapSubBitmoji": {
        "name": "Snapchat - Bitmoji",
        "description": "Bitmoji info from a Snapchat law enforcement return (subscriber_info.csv).",
        "author": "@AlexisBrignoni", "creation_date": "2024-06-13",
        "last_update_date": "2026-06-27", "requirements": "none",
        "category": "Snapchat Returns", "notes": "",
        "paths": ('*/subscriber_info.csv',), "output_types": "standard", "artifact_icon": "smile",
    }
}

import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor

_MONTHS = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
           'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}


def _snap_ts(value):
    parts = (value or '').split(' ')
    try:
        return datetime(int(parts[5]), _MONTHS[parts[1]], int(parts[2]),
                        *(int(x) for x in parts[3].split(':')), tzinfo=timezone.utc)
    except (IndexError, KeyError, ValueError):
        return value


def _clean_and_group(input_data):
    sections, current, exclude = [], [], False
    for line in input_data.split('\n'):
        if line.startswith('---') or line.startswith('==='):
            exclude = not exclude
            if not exclude and current:
                sections.append(current)
                current = []
            continue
        if not exclude and line.strip():
            current.append(line.strip())
    if current:
        sections.append(current)
    return sections


def _section(context, header_prefix):
    """Return (source_path, [split data rows]) for the subscriber_info section with the given header."""
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).startswith('subscriber_info.csv'):
            continue
        with open(file_found, encoding='utf-8') as f:
            for section in _clean_and_group(f.read()):
                if section[0].startswith(header_prefix):
                    return file_found, [line.strip().split(',') for line in section[1:]]
        return file_found, []
    return '', []


@artifact_processor
def snapSubAccountInfo(context):
    source_path, rows = _section(context, 'username,user_id,verified_email_address')
    data_list = []
    for item in rows:
        if len(item) < 12:
            continue
        ts = _snap_ts(item[5]) if item[5] else ''
        item[0], item[5] = ts, item[0]   # original swaps username (col 0) with the timestamp (col 5)
        data_list.append(tuple(item[:12]))
    data_headers = (('Timestamp', 'datetime'), 'User ID', 'Verified Email Address', 'Email status',
                    'Pending Email Address', 'Username', 'Creation IP',
                    ('Verified Phone Number', 'phonenumber'), 'Phone Status',
                    ('Pending Phone Number', 'phonenumber'), 'Display Name', 'Status')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def snapSubHistory(context):
    source_path, rows = _section(context, 'date,action,old_value,new_value,reason')
    data_list = []
    for item in rows:
        if len(item) < 5:
            continue
        item[0] = _snap_ts(item[0])
        data_list.append(tuple(item[:5]))
    data_headers = (('Timestamp', 'datetime'), 'Action', 'Old Value', 'New Value', 'Reason')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def snapSubValueChanges(context):
    source_path, rows = _section(context, 'old_value,new_value,timestamp')
    data_list = []
    for item in rows:
        if len(item) < 3:
            continue
        data_list.append((_snap_ts(item[2]), item[0], item[1]))
    data_headers = (('Timestamp', 'datetime'), 'Old Value', 'New Value')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def snapSubDetails(context):
    source_path, rows = _section(
        context, 'email_verified_timestamp,phone_verified_timestamp,birthdate,last_active,'
                 'follower_count,app_version,2FA_status')
    data_list = []
    for item in rows:
        if len(item) < 7:
            continue
        data_list.append((_snap_ts(item[0]), _snap_ts(item[1]), item[2], _snap_ts(item[3]),
                          item[4], item[5], item[6]))
    data_headers = (('Email Verified Timestamp', 'datetime'), ('Phone Verified Timestamp', 'datetime'),
                    'Birthdate', ('Last Active', 'datetime'), 'Follower Count', 'App Version',
                    '2FA Status')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def snapSubPrivacy(context):
    source_path, rows = _section(context, 'snap_privacy,story_privacy')
    data_list = [(item[0], item[1]) for item in rows if len(item) >= 2]
    data_headers = ('Snap Privacy', 'Story Privacy')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def snapSubBitmoji(context):
    source_path, rows = _section(context, 'is_bitmoji_user,bitmoji_gender')
    data_list = [(item[0], item[1]) for item in rows if len(item) >= 2]
    data_headers = ('Is Bitmoji User', 'Bitmoji Gender')
    return data_headers, data_list, context.get_relative_path(source_path)

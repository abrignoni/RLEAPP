__artifacts_v2__ = {
    "snapSubAccountInfo": {
        "name": "Snapchat - Account Information",
        "description": "Account information from a Snapchat law enforcement return (subscriber_info.csv).",
        "author": "@AlexisBrignoni", "creation_date": "2024-06-13",
        "last_update_date": "2026-07-09", "requirements": "none",
        "category": "Snapchat Returns", "notes": "",
        "paths": ('*/subscriber_info.csv',), "output_types": "standard", "artifact_icon": "user",
    },
    "snapSubHistory": {
        "name": "Snapchat - Account Change History",
        "description": "Account change history from a Snapchat law enforcement return (subscriber_info.csv or subscriber_account_change_history.csv).",
        "author": "@AlexisBrignoni", "creation_date": "2024-06-13",
        "last_update_date": "2026-07-09", "requirements": "none",
        "category": "Snapchat Returns", "notes": "",
        "paths": ('*/subscriber_info.csv', '*/subscriber_account_change_history.csv'),
        "output_types": "standard", "artifact_icon": "clock",
    },
    "snapSubValueChanges": {
        "name": "Snapchat - Value Changes",
        "description": "Value changes from a Snapchat law enforcement return (subscriber_info.csv).",
        "author": "@AlexisBrignoni", "creation_date": "2024-06-13",
        "last_update_date": "2026-07-09", "requirements": "none",
        "category": "Snapchat Returns", "notes": "",
        "paths": ('*/subscriber_info.csv',), "output_types": "standard", "artifact_icon": "edit",
    },
    "snapSubDetails": {
        "name": "Snapchat - Account Details",
        "description": "Account details from a Snapchat law enforcement return (subscriber_info.csv).",
        "author": "@AlexisBrignoni", "creation_date": "2024-06-13",
        "last_update_date": "2026-07-09", "requirements": "none",
        "category": "Snapchat Returns", "notes": "",
        "paths": ('*/subscriber_info.csv',), "output_types": "standard", "artifact_icon": "info-circle",
    },
    "snapSubPrivacy": {
        "name": "Snapchat - Privacy Settings",
        "description": "Privacy settings from a Snapchat law enforcement return (subscriber_info.csv).",
        "author": "@AlexisBrignoni", "creation_date": "2024-06-13",
        "last_update_date": "2026-07-09", "requirements": "none",
        "category": "Snapchat Returns", "notes": "",
        "paths": ('*/subscriber_info.csv',), "output_types": "standard", "artifact_icon": "lock",
    },
    "snapSubBitmoji": {
        "name": "Snapchat - Bitmoji",
        "description": "Bitmoji info from a Snapchat law enforcement return (subscriber_info.csv).",
        "author": "@AlexisBrignoni", "creation_date": "2024-06-13",
        "last_update_date": "2026-07-09", "requirements": "none",
        "category": "Snapchat Returns", "notes": "",
        "paths": ('*/subscriber_info.csv',), "output_types": "standard", "artifact_icon": "mood-smile",
    }
}

import csv
import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor

_MONTHS = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
           'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}


def _snap_ts(value):
    # Older returns: "Wed Aug 19 12:00:00 UTC 2021"; newer returns: "2026-04-11 04:02:00 UTC".
    value = (value or '').strip()
    if value.endswith(' UTC'):
        try:
            return datetime.strptime(value[:-4], '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    parts = value.split(' ')
    try:
        return datetime(int(parts[5]), _MONTHS[parts[1]], int(parts[2]),
                        *(int(x) for x in parts[3].split(':')), tzinfo=timezone.utc)
    except (IndexError, KeyError, ValueError):
        return value


def _read_sections(file_path):
    # The file holds one or more sections, each made of a quoted multi-line
    # legend, a row of '=' characters, a header row, then data rows. Legend
    # rows parse as a single cell, so rows with fewer than two cells are not data.
    sections = []
    rows = None
    pending_header = False
    with open(file_path, 'r', newline='', encoding='utf-8') as f:
        for row in csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL):
            if any(cell and set(cell) == {'='} for cell in row):
                pending_header = True
                rows = None
            elif pending_header:
                rows = []
                sections.append((row, rows))
                pending_header = False
            elif rows is not None and len(row) >= 2:
                rows.append(row)
    return sections


def _section_data(context, filename_prefixes, required_fields, ordered):
    """Build (data_headers, data_list, source_path) from every section whose header
    holds required_fields. Columns are mapped by header name, never by position (the
    layout changes across return versions, e.g. former_phone_number was added and the
    change history moved to its own file). `ordered` is a list of (field_name, header)
    pairs; a header tuple typed 'datetime' also converts the value with _snap_ts.
    Fields Snapchat adds later are appended as they appear."""
    known = [field for field, _ in ordered]
    extras = []
    records = []
    source_path = ''
    parsed = set()
    for file_found in context.get_files_found():
        file_found = str(file_found)
        base = os.path.basename(file_found)
        if not any(base.startswith(prefix) for prefix in filename_prefixes):
            continue
        real_path = os.path.realpath(file_found)
        if real_path in parsed:
            continue
        parsed.add(real_path)
        source_path = file_found
        for header, rows in _read_sections(file_found):
            header = [h.strip().lower() for h in header]
            if not set(required_fields).issubset(header):
                continue
            for name in header:
                if name not in known and name not in extras:
                    extras.append(name)
            for raw in rows:
                if any(cell.strip() for cell in raw):
                    records.append(dict(zip(header, raw)))

    data_headers = tuple(h for _, h in ordered) + tuple(n.capitalize() for n in extras)
    data_list = []
    for values in records:
        entry = []
        for field, spec in ordered:
            value = values.get(field, '')
            if isinstance(spec, tuple) and spec[1] == 'datetime' and value:
                value = _snap_ts(value)
            entry.append(value)
        entry.extend(values.get(name, '') for name in extras)
        data_list.append(entry)
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def snapSubAccountInfo(context):
    return _section_data(
        context, ('subscriber_info.csv',), ('username', 'user_id', 'created'),
        [('created', ('Timestamp', 'datetime')),
         ('user_id', 'User ID'),
         ('email_address', 'Verified Email Address'),
         ('email_status', 'Email status'),
         ('pending_email_address', 'Pending Email Address'),
         ('username', 'Username'),
         ('creation_ip', 'Creation IP'),
         ('phone_number', ('Verified Phone Number', 'phonenumber')),
         ('phone_status', 'Phone Status'),
         ('pending_phone_number', ('Pending Phone Number', 'phonenumber')),
         ('former_phone_number', ('Former Phone Number', 'phonenumber')),
         ('display_name', 'Display Name'),
         ('status', 'Status')])


@artifact_processor
def snapSubHistory(context):
    # Newer returns ship the change history as subscriber_account_change_history.csv;
    # older ones embed it as a section of subscriber_info.csv.
    return _section_data(
        context, ('subscriber_info.csv', 'subscriber_account_change_history.csv'),
        ('date', 'action', 'old_value', 'new_value', 'reason'),
        [('date', ('Timestamp', 'datetime')),
         ('action', 'Action'),
         ('old_value', 'Old Value'),
         ('new_value', 'New Value'),
         ('reason', 'Reason')])


@artifact_processor
def snapSubValueChanges(context):
    return _section_data(
        context, ('subscriber_info.csv',), ('old_value', 'new_value', 'timestamp'),
        [('timestamp', ('Timestamp', 'datetime')),
         ('old_value', 'Old Value'),
         ('new_value', 'New Value')])


@artifact_processor
def snapSubDetails(context):
    # last_active is reported by Snapchat in PDT/PST (per the file legend), so it is
    # kept verbatim as plain text instead of being typed/coerced as a UTC datetime.
    return _section_data(
        context, ('subscriber_info.csv',), ('birthdate', 'last_active'),
        [('email_verified_timestamp', ('Email Verified Timestamp', 'datetime')),
         ('phone_verified_timestamp', ('Phone Verified Timestamp', 'datetime')),
         ('birthdate', 'Birthdate'),
         ('last_active', 'Last Active'),
         ('follower_count', 'Follower Count'),
         ('app_version', 'App Version'),
         ('2fa_status', '2FA Status')])


@artifact_processor
def snapSubPrivacy(context):
    return _section_data(
        context, ('subscriber_info.csv',), ('snap_privacy', 'story_privacy'),
        [('snap_privacy', 'Snap Privacy'),
         ('story_privacy', 'Story Privacy')])


@artifact_processor
def snapSubBitmoji(context):
    return _section_data(
        context, ('subscriber_info.csv',), ('is_bitmoji_user', 'bitmoji_gender'),
        [('is_bitmoji_user', 'Is Bitmoji User'),
         ('bitmoji_gender', 'Bitmoji Gender')])

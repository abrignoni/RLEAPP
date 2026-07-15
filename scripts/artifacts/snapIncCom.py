__artifacts_v2__ = {
    "snapIncCom": {
        "name": "Snapchat - Inc Comms",
        "description": "Incoming email communications parsed from a Snapchat law enforcement return (snap_inc_communications.csv).",
        "author": "@AlexisBrignoni",
        "creation_date": "2024-06-13",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Snapchat Returns",
        "notes": "",
        "paths": ('*/snap_inc_communications.csv',),
        "output_types": "standard",
        "artifact_icon": "mail",
    },
    "snapIncComSms": {
        "name": "Snapchat - Inc Comms SMS",
        "description": "SMS events parsed from a Snapchat law enforcement return (snap_inc_communications.csv).",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-07-09",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Snapchat Returns",
        "notes": "",
        "paths": ('*/snap_inc_communications.csv',),
        "output_types": "standard",
        "artifact_icon": "device-mobile",
    },
    "snapIncComAppeals": {
        "name": "Snapchat - In App Appeals",
        "description": "In-app account appeals parsed from a Snapchat law enforcement return (snap_inc_communications.csv).",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-07-09",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Snapchat Returns",
        "notes": "",
        "paths": ('*/snap_inc_communications.csv',),
        "output_types": "standard",
        "artifact_icon": "help-circle",
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


def _section_data(context, required_fields, ordered):
    """Build (data_headers, data_list, source_path) from every section whose header
    holds required_fields (the file carries Email Events, SMS Events, and In App
    Appeals sections). Columns are mapped by header name, never by position; a
    header tuple typed 'datetime' also converts the value with _snap_ts. Fields
    Snapchat adds later are appended as they appear."""
    known = [field for field, _ in ordered]
    extras = []
    records = []
    source_path = ''
    parsed = set()
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).startswith('snap_inc_communications.csv'):
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
def snapIncCom(context):
    return _section_data(
        context, ('email_address', 'campaign_name', 'event_timestamp'),
        [('event_timestamp', ('Timestamp', 'datetime')),
         ('user_id', 'User ID'),
         ('email_address', 'Email Address'),
         ('user_agent', 'User Agent'),
         ('campaign_name', 'Campaign Name'),
         ('type', 'Type')])


@artifact_processor
def snapIncComSms(context):
    return _section_data(
        context, ('phone_number', 'feature', 'vendor'),
        [('message_timestamp', ('Timestamp', 'datetime')),
         ('user_id', 'User ID'),
         ('phone_number', ('Phone Number', 'phonenumber')),
         ('strategy', 'Strategy'),
         ('feature', 'Feature'),
         ('vendor', 'Vendor'),
         ('vendor_status', 'Vendor Status'),
         ('message_id', 'Message ID'),
         ('message_tracker_id', 'Message Tracker ID')])


@artifact_processor
def snapIncComAppeals(context):
    return _section_data(
        context, ('appeal_id', 'appeal_justification'),
        [('created_timestamp', ('Timestamp', 'datetime')),
         ('requester_user_id', 'Requester User ID'),
         ('requester_username', 'Requester Username'),
         ('requester_mutable_username', 'Requester Mutable Username'),
         ('requester_email', 'Requester Email'),
         ('appeal_id', 'Appeal ID'),
         ('appeal_justification', 'Appeal Justification')])

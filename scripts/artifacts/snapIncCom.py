__artifacts_v2__ = {
    "snapIncCom": {
        "name": "Snapchat - Inc Comms",
        "description": "Incoming communications parsed from a Snapchat law enforcement return (snap_inc_communications.csv).",
        "author": "@AlexisBrignoni",
        "creation_date": "2024-06-13",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Snapchat Returns",
        "notes": "",
        "paths": ('*/snap_inc_communications.csv',),
        "output_types": "standard",
        "artifact_icon": "mail",
    }
}

import csv
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


@artifact_processor
def snapIncCom(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).startswith('snap_inc_communications.csv'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            for section in _clean_and_group(f.read()):
                if not section[0].startswith('user_id,email_address,user_agent,campaign_name,type,event_timestamp'):
                    continue
                for line in section[1:]:
                    rows = list(csv.reader([line], skipinitialspace=True))
                    if not rows or len(rows[0]) < 6:
                        continue
                    x = rows[0]
                    # source order: user_id, email, user_agent, campaign, type, event_timestamp
                    data_list.append((_snap_ts(x[5]), x[0], x[1], x[2], x[3], x[4]))

    data_headers = (('Timestamp', 'datetime'), 'User ID', 'Email Address', 'User Agent',
                    'Campaign Name', 'Type')
    return data_headers, data_list, context.get_relative_path(source_path)

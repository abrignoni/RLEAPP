__artifacts_v2__ = {
    "snapIPd": {
        "name": "Snapchat - IP Data",
        "description": "IP data parsed from a Snapchat law enforcement return (ip_data.csv).",
        "author": "@AlexisBrignoni",
        "creation_date": "2024-06-13",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Snapchat Returns",
        "notes": "",
        "paths": ('*/ip_data.csv',),
        "output_types": "standard",
        "artifact_icon": "globe",
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


@artifact_processor
def snapIPd(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).startswith('ip_data.csv'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            for section in _clean_and_group(f.read()):
                if not section[0].startswith('ip,first seen time,last seen time'):
                    continue
                for line in section[1:]:
                    item = line.strip().split(',')
                    if len(item) < 3:
                        continue
                    first_seen = _snap_ts(item[1]) if item[1] else ''
                    last_seen = _snap_ts(item[2]) if item[2] else ''
                    data_list.append((item[0], first_seen, last_seen))

    data_headers = ('IP', ('First Seen Time', 'datetime'), ('Last Seen Time', 'datetime'))
    return data_headers, data_list, context.get_relative_path(source_path)

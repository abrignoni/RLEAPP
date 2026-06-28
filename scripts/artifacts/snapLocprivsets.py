__artifacts_v2__ = {
    "snapLocprivsets": {
        "name": "Snapchat - Location Privacy Settings",
        "description": "Location privacy settings parsed from a Snapchat law enforcement return (loc_priv_sets.csv).",
        "author": "@AlexisBrignoni",
        "creation_date": "2024-06-13",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Snapchat Returns",
        "notes": "",
        "paths": ('*/loc_priv_sets.csv',),
        "output_types": "standard",
        "artifact_icon": "map-pin",
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
def snapLocprivsets(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).startswith('loc_priv_sets.csv'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            for section in _clean_and_group(f.read()):
                if not section[0].startswith('timestamp,audience,allowlist,blocklist,ghost_mode'):
                    continue
                for line in section[1:]:
                    item = line.strip().split(',')
                    if len(item) < 8:
                        continue
                    data_list.append((_snap_ts(item[0]), item[1], item[2], item[3], item[4],
                                      item[5], item[6], item[7]))

    data_headers = (('Timestamp', 'datetime'), 'Audience', 'Allow List', 'Block List', 'Ghost Mode',
                    'Ghost Mode Expiration', 'Live Session IDS', 'Live Session Expirations')
    return data_headers, data_list, context.get_relative_path(source_path)

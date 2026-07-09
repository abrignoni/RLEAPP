__artifacts_v2__ = {
    "snapLocprivsets": {
        "name": "Snapchat - Location Privacy Settings",
        "description": "Location privacy settings parsed from a Snapchat law enforcement return (loc_priv_sets.csv).",
        "author": "@AlexisBrignoni",
        "creation_date": "2024-06-13",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Snapchat Returns",
        "notes": "",
        "paths": ('*/loc_priv_sets.csv',),
        "output_types": "standard",
        "artifact_icon": "map-pin",
    }
}

import csv
import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor

_MONTHS = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
           'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

_DISPLAY = {'allowlist': 'Allow List', 'blocklist': 'Block List', 'ghost_mode': 'Ghost Mode',
            'ghost_mode_expiration': 'Ghost Mode Expiration', 'live_session_ids': 'Live Session IDS',
            'live_session_expirations': 'Live Session Expirations'}


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


@artifact_processor
def snapLocprivsets(context):
    # Columns are mapped by header name, never by position (the layout changes across
    # return versions). Known fields are pre-seeded to keep a stable column order;
    # any new fields Snapchat adds are appended as they appear.
    field_names = ['audience', 'allowlist', 'blocklist', 'ghost_mode', 'ghost_mode_expiration',
                   'live_session_ids', 'live_session_expirations']
    records = []
    source_path = ''
    parsed = set()
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).startswith('loc_priv_sets.csv'):
            continue
        real_path = os.path.realpath(file_found)
        if real_path in parsed:
            continue
        parsed.add(real_path)
        source_path = file_found
        for header, rows in _read_sections(file_found):
            header = [h.strip().lower() for h in header]
            if not {'timestamp', 'audience', 'ghost_mode'}.issubset(header):
                continue
            for name in header:
                if name != 'timestamp' and name not in field_names:
                    field_names.append(name)
            for raw in rows:
                if not any(cell.strip() for cell in raw):
                    continue
                values = dict(zip(header, raw))
                timestamp = _snap_ts(values.pop('timestamp', ''))
                records.append((timestamp, values))

    data_headers = tuple([('Timestamp', 'datetime')]
                         + [_DISPLAY.get(name, name.capitalize()) for name in field_names])
    data_list = [[timestamp] + [values.get(name, '') for name in field_names]
                 for timestamp, values in records]

    return data_headers, data_list, context.get_relative_path(source_path)

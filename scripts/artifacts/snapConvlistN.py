__artifacts_v2__ = {
    "snapConvlistN": {
        "name": "Snapchat - Conversation List",
        "description": "Conversation metadata (participants, creation and last activity timestamps, "
                       "retention policy, storage region) for one-to-one and group conversations, "
                       "parsed from a Snapchat law enforcement return (conversation_list.csv).",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-07-09",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Snapchat Returns",
        "notes": "",
        "paths": ('*/conversation_list.csv',),
        "output_types": "standard",
        "artifact_icon": "list",
    }
}

import csv
import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor

_DATETIME_COLUMNS = ('creation_time', 'last_event_timestamp')


def _snap_ts(value):
    # Return format: "2026-04-09 08:46:45 UTC". Non-UTC values are kept as plain text.
    value = (value or '').strip()
    if value.endswith(' UTC'):
        try:
            return datetime.strptime(value[:-4], '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    return value


def _read_sections(file_path):
    # The file holds one or more sections (e.g. 1:1 conversations, then group
    # conversations), each made of a quoted multi-line legend, a row of '='
    # characters, a header row, then data rows. Legend rows parse as a single
    # cell, so rows with fewer than two cells are not data.
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
def snapConvlistN(context):
    # Columns are mapped by header name, never by position, so sections with
    # different layouts (and fields added in future return versions) cannot
    # misalign the output.
    field_names = []
    records = []
    source_path = ''
    parsed = set()
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).startswith('conversation_list.csv'):
            continue
        real_path = os.path.realpath(file_found)
        if real_path in parsed:
            continue
        parsed.add(real_path)
        source_path = file_found
        for header, rows in _read_sections(file_found):
            header = [h.strip().lower() for h in header]
            for name in header:
                if name not in _DATETIME_COLUMNS and name not in field_names:
                    field_names.append(name)
            for raw in rows:
                if not any(cell.strip() for cell in raw):
                    continue
                values = dict(zip(header, raw))
                timestamps = [_snap_ts(values.pop(name, '')) for name in _DATETIME_COLUMNS]
                records.append((timestamps, values))

    data_headers = tuple([('Creation_time', 'datetime'), ('Last_event_timestamp', 'datetime')]
                         + [name.capitalize() for name in field_names])
    data_list = [timestamps + [values.get(name, '') for name in field_names]
                 for timestamps, values in records]

    return data_headers, data_list, context.get_relative_path(source_path)

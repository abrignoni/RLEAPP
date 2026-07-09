__artifacts_v2__ = {
    "snapCalllogsN": {
        "name": "Snapchat - Call Logs",
        "description": "Audio and video call records (creator, participant count, start and end "
                       "timestamps, duration, network and connection result), parsed from a "
                       "Snapchat law enforcement return (call_logs.csv).",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-07-09",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Snapchat Returns",
        "notes": "",
        "paths": ('*/call_logs.csv',),
        "output_types": "standard",
        "artifact_icon": "phone",
    }
}

import csv
import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor

_DATETIME_COLUMNS = ('call_start', 'call_end')


def _snap_ts(value):
    # Return format: "Apr 06 2026 03:48:31 UTC" (some return sections use
    # "2026-04-06 03:48:31 UTC"). Non-UTC values are kept as plain text.
    value = (value or '').strip()
    if value.endswith(' UTC'):
        for fmt in ('%b %d %Y %H:%M:%S', '%Y-%m-%d %H:%M:%S'):
            try:
                return datetime.strptime(value[:-4], fmt).replace(tzinfo=timezone.utc)
            except ValueError:
                pass
    return value


def _read_sections(file_path):
    # Each call is its own block: a row of '=' characters, the call header
    # row, then data rows. A row of '-' characters starts the per-call
    # participant sub-section (label, sub-header, participant rows), which is
    # not part of this artifact, so it ends data collection until the next
    # '=' row. Legend and label rows parse as a single cell, so rows with
    # fewer than two cells are not data.
    sections = []
    rows = None
    pending_header = False
    with open(file_path, 'r', newline='', encoding='utf-8') as f:
        for row in csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL):
            if any(cell and set(cell) == {'='} for cell in row):
                pending_header = True
                rows = None
            elif any(cell and set(cell) == {'-'} for cell in row):
                rows = None
            elif pending_header and row:
                rows = []
                sections.append((row, rows))
                pending_header = False
            elif rows is not None and len(row) >= 2:
                rows.append(row)
    return sections


@artifact_processor
def snapCalllogsN(context):
    # Columns are mapped by header name, never by position, so fields added in
    # future return versions cannot misalign the output.
    field_names = []
    records = []
    source_path = ''
    parsed = set()
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).startswith('call_logs.csv'):
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

    data_headers = tuple([('Call_start', 'datetime'), ('Call_end', 'datetime')]
                         + [name.capitalize() for name in field_names])
    data_list = [timestamps + [values.get(name, '') for name in field_names]
                 for timestamps, values in records]

    return data_headers, data_list, context.get_relative_path(source_path)

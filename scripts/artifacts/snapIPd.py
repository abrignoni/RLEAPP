__artifacts_v2__ = {
    "snapIPd": {
        "name": "Snapchat - IP Data",
        "description": "IP data parsed from a Snapchat law enforcement return (ip_data.csv).",
        "author": "@AlexisBrignoni",
        "creation_date": "2024-06-13",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Snapchat Returns",
        "notes": "",
        "paths": ('*/ip_data.csv',),
        "output_types": "standard",
        "artifact_icon": "globe",
    }
}

import csv
import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor

_MONTHS = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
           'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

# Older returns use headers like "first seen time"; newer ones "first_seen_time".
_DISPLAY = {'ip': 'IP', 'asn': 'ASN', 'url': 'URL',
            'first seen time': 'First Seen Time', 'last seen time': 'Last Seen Time',
            'first_seen_time': 'First Seen Time', 'last_seen_time': 'Last Seen Time'}


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


def _is_time_field(name):
    return name.endswith('time') or name.endswith('timestamp')


def _column(name):
    display = _DISPLAY.get(name, name.capitalize())
    return (display, 'datetime') if _is_time_field(name) else display


@artifact_processor
def snapIPd(context):
    # Columns are mapped by header name, never by position: newer returns replaced the
    # separate per-source sections with one consolidated table of 20+ columns, and the
    # layout keeps changing. Every section in the file is parsed into the union of the
    # columns seen; fields Snapchat adds later are appended as they appear.
    field_names = ['ip', 'timestamp', 'first_seen_time', 'last_seen_time']
    records = []
    source_path = ''
    parsed = set()
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).startswith('ip_data.csv'):
            continue
        real_path = os.path.realpath(file_found)
        if real_path in parsed:
            continue
        parsed.add(real_path)
        source_path = file_found
        for header, rows in _read_sections(file_found):
            header = [h.strip().lower() for h in header]
            for name in header:
                if name not in field_names:
                    field_names.append(name)
            for raw in rows:
                if not any(cell.strip() for cell in raw):
                    continue
                values = dict(zip(header, raw))
                for name in header:
                    if _is_time_field(name) and values.get(name):
                        values[name] = _snap_ts(values[name])
                records.append(values)

    data_headers = tuple(_column(name) for name in field_names)
    data_list = [[values.get(name, '') for name in field_names] for values in records]

    return data_headers, data_list, context.get_relative_path(source_path)

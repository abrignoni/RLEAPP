__artifacts_v2__ = {
    "snapMemN": {
        "name": "Snapchat - Memories",
        "description": "Memories parsed from a Snapchat law enforcement return (memories.csv).",
        "author": "@AlexisBrignoni",
        "creation_date": "2024-06-13",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Snapchat Returns",
        "notes": "",
        "paths": ('*/memories.csv', '*/*.*'),
        "output_types": ['html', 'tsv', 'timeline', 'lava', 'kml'],
        "artifact_icon": "image",
    }
}

import csv
import os
import re
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, check_in_media

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


@artifact_processor
def snapMemN(context):
    files_found = [str(f) for f in context.get_files_found()]

    # Media files in the return are named by media_id (with or without an extension).
    media_lookup = {}
    for path in files_found:
        name = os.path.basename(path)
        if name.lower().endswith('.csv'):
            continue
        media_lookup.setdefault(name, path)
        media_lookup.setdefault(os.path.splitext(name)[0], path)
        # Newer returns name media "<type>~media_v4~...~b~<id>~v4.<ext>" and the
        # CSV media_id column holds only the "b~<id>" token; key by it too.
        token = re.search(r'~(b~[^~]+)~v4', name)
        if token:
            media_lookup.setdefault(token.group(1), path)

    checked_in = {}

    def _media_refs(media_field):
        refs = []
        for token in (t.strip() for t in (media_field or '').split(';')):
            path = media_lookup.get(token)
            if not token or not path:
                continue
            if path not in checked_in:
                checked_in[path] = check_in_media(path, os.path.basename(path))
            if checked_in[path]:
                refs.append(checked_in[path])
        return refs

    # Columns are mapped by header name, never by position (the layout changes across
    # return versions). Known fields are pre-seeded so the Latitude/Longitude columns
    # the kml output needs stay present even when a return holds no data; any new
    # fields Snapchat adds are appended as they appear.
    field_names = ['id', 'media_id', 'encrypted', 'source_type', 'latitude', 'longitude',
                   'duration']
    records = []
    source_path = ''
    parsed = set()
    for file_found in files_found:
        if not os.path.basename(file_found).startswith('memories.csv'):
            continue
        real_path = os.path.realpath(file_found)
        if real_path in parsed:  # the same file can match more than one search pattern
            continue
        parsed.add(real_path)
        source_path = file_found
        for header, rows in _read_sections(file_found):
            header = [h.strip().lower() for h in header]
            for name in header:
                if name != 'timestamp' and name not in field_names:
                    field_names.append(name)
            for raw in rows:
                if not any(cell.strip() for cell in raw):
                    continue
                values = dict(zip(header, raw))
                timestamp = _snap_ts(values.pop('timestamp', ''))
                records.append((timestamp, values, _media_refs(values.get('media_id', ''))))

    # Media is placed right after Timestamp for readability.
    data_headers = tuple([('Timestamp', 'datetime'), ('Media', 'media')]
                         + [name.capitalize() for name in field_names])
    # A single media reference is emitted as a bare id (what the LAVA viewer
    # resolves); a list is kept only when a record links more than one file.
    data_list = [[timestamp, (refs[0] if len(refs) == 1 else refs) if refs else '']
                 + [values.get(name, '') for name in field_names]
                 for timestamp, values, refs in records]

    return data_headers, data_list, context.get_relative_path(source_path)

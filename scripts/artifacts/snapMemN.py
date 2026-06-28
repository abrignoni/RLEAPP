__artifacts_v2__ = {
    "snapMemN": {
        "name": "Snapchat - Memories",
        "description": "Memories parsed from a Snapchat law enforcement return (memories.csv).",
        "author": "@AlexisBrignoni",
        "creation_date": "2024-06-13",
        "last_update_date": "2026-06-27",
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
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, check_in_media

_MONTHS = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
           'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}


def _snap_ts(value):
    # Snapchat return format: "Wed Aug 19 12:00:00 UTC 2021" (the tz field is assumed UTC).
    parts = (value or '').split(' ')
    try:
        return datetime(int(parts[5]), _MONTHS[parts[1]], int(parts[2]),
                        *(int(x) for x in parts[3].split(':')), tzinfo=timezone.utc)
    except (IndexError, KeyError, ValueError):
        return value


def _read_multiline_csv(file_path):
    rows = []
    start = False
    with open(file_path, 'r', newline='', encoding='utf-8') as f:
        for row in csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL):
            if start:
                rows.append(row)
            elif '===========================' in row:
                start = True
    return rows


@artifact_processor
def snapMemN(context):
    ts_idx, media_idx = 7, 2
    data_headers = (('Timestamp', 'datetime'), 'Id', 'Media_id', 'Encrypted', 'Source_type',
                    'Latitude', 'Longitude', 'Duration', ('Media', 'media'))
    non_media = len(data_headers) - 1

    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).startswith('memories.csv'):
            continue
        source_path = file_found
        rows = _read_multiline_csv(file_found)
        for raw in rows[1:]:
            if len(raw) <= ts_idx:
                continue
            entry = list(raw)
            entry.insert(0, _snap_ts(entry[ts_idx]))
            del entry[ts_idx + 1]
            media_raw = entry[media_idx] if len(entry) > media_idx else ''
            refs = [r for r in (check_in_media(m.strip(), m.strip())
                                for m in media_raw.split(';') if m.strip()) if r]
            entry = (entry + [''] * non_media)[:non_media]
            entry.append(refs)
            data_list.append(entry)

    return data_headers, data_list, context.get_relative_path(source_path)

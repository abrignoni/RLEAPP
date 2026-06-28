__artifacts_v2__ = {
    "snapGeolocation": {
        "name": "Snapchat - Geolocation",
        "description": "Geolocation (latitude,longitude,timestamp format) from a Snapchat law enforcement return (geo_locations.csv).",
        "author": "@AlexisBrignoni",
        "creation_date": "2024-06-13",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Snapchat Returns",
        "notes": "Update by Shawn Ramsey 2024-08-05.",
        "paths": ('*/geo_locations.csv',),
        "output_types": ['html', 'tsv', 'timeline', 'lava', 'kml'],
        "artifact_icon": "map-pin",
    },
    "snapGeoAdditional": {
        "name": "Snapchat - Additional Geolocation",
        "description": "Geolocation (latitude,longitude,accuracy,timestamp,is_live_location format) from a Snapchat law enforcement return (geo_locations.csv).",
        "author": "@AlexisBrignoni",
        "creation_date": "2024-06-13",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Snapchat Returns",
        "notes": "Update by Shawn Ramsey 2024-08-05.",
        "paths": ('*/geo_locations.csv',),
        "output_types": ['html', 'tsv', 'timeline', 'lava', 'kml'],
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
def snapGeolocation(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).startswith('geo_locations.csv'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            for section in _clean_and_group(f.read()):
                if not section[0].startswith('latitude,longitude,timestamp'):
                    continue
                for line in section[1:]:
                    item = line.strip().split(',')
                    if len(item) < 3:
                        continue
                    lat_parts = item[0].split(' ')
                    lat = lat_parts[0]
                    accuracy = lat_parts[2] + ' meters' if len(lat_parts) > 2 else ''
                    lon = item[1].split(' ')[0]
                    data_list.append((_snap_ts(item[2]), lat, lon, accuracy))

    data_headers = (('Timestamp', 'datetime'), 'Latitude', 'Longitude', 'Accuracy')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def snapGeoAdditional(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).startswith('geo_locations.csv'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            for section in _clean_and_group(f.read()):
                if not section[0].startswith('latitude,longitude,accuracy,timestamp,is_live_location'):
                    continue
                for line in section[1:]:
                    item = line.strip().split(',')
                    if len(item) < 5:
                        continue
                    data_list.append((_snap_ts(item[3]), item[0], item[1], item[2], item[4]))

    data_headers = (('Timestamp', 'datetime'), 'Latitude', 'Longitude', 'Accuracy',
                    'Is Live Location')
    return data_headers, data_list, context.get_relative_path(source_path)

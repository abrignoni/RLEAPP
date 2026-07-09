__artifacts_v2__ = {
    "snapGeolocation": {
        "name": "Snapchat - Geolocation",
        "description": "Geolocation (latitude,longitude,timestamp format) from a Snapchat law enforcement return (geo_locations.csv).",
        "author": "@AlexisBrignoni",
        "creation_date": "2024-06-13",
        "last_update_date": "2026-07-09",
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
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Snapchat Returns",
        "notes": "Update by Shawn Ramsey 2024-08-05.",
        "paths": ('*/geo_locations.csv',),
        "output_types": ['html', 'tsv', 'timeline', 'lava', 'kml'],
        "artifact_icon": "map-pin",
    },
    "snapGeoCity": {
        "name": "Snapchat - Geolocation City",
        "description": "Country, region, and city derived from device GPS (country,region,city,timestamp format) from a Snapchat law enforcement return (geo_locations.csv).",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-07-09",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Snapchat Returns",
        "notes": "",
        "paths": ('*/geo_locations.csv',),
        "output_types": "standard",
        "artifact_icon": "map",
    }
}

import csv
import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor

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


def _matching_sections(context, required_fields, excluded_fields=()):
    # Sections are identified by the column names in their header, never by position
    # or by order in the file (the layout changes across return versions).
    source_path = ''
    matches = []
    parsed = set()
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).startswith('geo_locations.csv'):
            continue
        real_path = os.path.realpath(file_found)
        if real_path in parsed:
            continue
        parsed.add(real_path)
        source_path = file_found
        for header, rows in _read_sections(file_found):
            header = [h.strip().lower() for h in header]
            if not set(required_fields).issubset(header):
                continue
            if any(name in header for name in excluded_fields):
                continue
            for raw in rows:
                if any(cell.strip() for cell in raw):
                    matches.append(dict(zip(header, raw)))
    return source_path, matches


@artifact_processor
def snapGeolocation(context):
    source_path, rows = _matching_sections(context, ('latitude', 'longitude', 'timestamp'),
                                           excluded_fields=('accuracy', 'is_live_location',
                                                            'country', 'city'))
    data_list = []
    for values in rows:
        # Coordinates come as "34.47359 ± 39.66 meters"; the accuracy is embedded.
        lat_parts = values.get('latitude', '').split(' ')
        lat = lat_parts[0]
        accuracy = lat_parts[2] + ' meters' if len(lat_parts) > 2 else ''
        lon = values.get('longitude', '').split(' ')[0]
        data_list.append((_snap_ts(values.get('timestamp', '')), lat, lon, accuracy))

    data_headers = (('Timestamp', 'datetime'), 'Latitude', 'Longitude', 'Accuracy')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def snapGeoAdditional(context):
    source_path, rows = _matching_sections(
        context, ('latitude', 'longitude', 'accuracy', 'timestamp', 'is_live_location'))
    data_list = [(_snap_ts(values.get('timestamp', '')), values.get('latitude', ''),
                  values.get('longitude', ''), values.get('accuracy', ''),
                  values.get('is_live_location', ''))
                 for values in rows]

    data_headers = (('Timestamp', 'datetime'), 'Latitude', 'Longitude', 'Accuracy',
                    'Is Live Location')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def snapGeoCity(context):
    source_path, rows = _matching_sections(context, ('country', 'region', 'city', 'timestamp'))
    data_list = [(_snap_ts(values.get('timestamp', '')), values.get('country', ''),
                  values.get('region', ''), values.get('city', ''))
                 for values in rows]

    data_headers = (('Timestamp', 'datetime'), 'Country', 'Region', 'City')
    return data_headers, data_list, context.get_relative_path(source_path)

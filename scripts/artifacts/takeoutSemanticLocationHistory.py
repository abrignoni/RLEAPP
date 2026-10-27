__artifacts_v2__ = {
    "takeoutSemanticPlaceVisits": {
        "name": "Google Semantic Location History - Place Visits",
        "description": "Parses placeVisit entries from Google Takeout Semantic Location History JSON files",
        "author": "@AlexisBrignoni, Codex",
        "creation_date": "2022-09-15",
        "last_update_date": "2026-10-07",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "Latitude and Longitude report location.latitudeE7 and location.longitudeE7 divided by "
                 "1e7 when the respective key is present. A missing coordinate key yields a native None "
                 "value (blank in HTML/TSV and NULL in the report database), not 0.0; an actual stored "
                 "zero remains 0.0. A missing whole place location is treated as an empty mapping. "
                 "Present JSON null or unsupported coordinate types remain unsupported. Original "
                 "artifact contribution: @KevinPagano3.",
        "paths": ('*/Semantic Location History/*/*.json',),
        "output_types": ['html', 'tsv', 'timeline', 'lava', 'kml'],
        "artifact_icon": "map-pin",
    },
    "takeoutSemanticActivitySegments": {
        "name": "Google Semantic Location History - Activity Segments",
        "description": "Parses activitySegment entries from Google Takeout Semantic Location History JSON files",
        "author": "@AlexisBrignoni, Codex",
        "creation_date": "2022-09-15",
        "last_update_date": "2026-10-07",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "Start/End coordinates are separate columns; no KML file is written for this artifact. "
                 "An absent whole start or end location retains NOT_SPECIFIED. A present location "
                 "mapping with a missing coordinate key yields a native None value (blank in HTML/TSV "
                 "and NULL in the report database); an actual stored zero remains 0.0. Present JSON "
                 "null or unsupported coordinate types remain unsupported. Original artifact "
                 "contribution: @KevinPagano3.",
        "paths": ('*/Semantic Location History/*/*.json',),
        "output_types": "standard",
        "artifact_icon": "navigation",
    }
}

import json
import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


def _iso_to_utc(value):
    if not value:
        return value
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(timezone.utc)
    except (ValueError, AttributeError):
        return value


def _duration_ts(duration, base):
    # Old archives use '<base>TimestampMs' (ms epoch); new ones use '<base>Timestamp' (ISO).
    ms_value = duration.get(f'{base}TimestampMs')
    if ms_value:
        return convert_unix_ts_to_utc(ms_value)
    return _iso_to_utc(duration.get(f'{base}Timestamp', ''))


@artifact_processor
def takeoutSemanticPlaceVisits(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('.json'):
            continue
        source_path = file_found
        file_name = os.path.basename(file_found)
        with open(file_found, encoding='utf-8-sig') as f:
            data = json.load(f)

        for element in data.get('timelineObjects', []):
            if 'placeVisit' not in element:
                continue
            pv = element['placeVisit']
            location = pv.get('location', {})
            lat = location['latitudeE7'] / 1e7 if 'latitudeE7' in location.keys() else None
            lon = location['longitudeE7'] / 1e7 if 'longitudeE7' in location.keys() else None
            duration = pv.get('duration', {})
            data_list.append((_duration_ts(duration, 'start'), _duration_ts(duration, 'end'),
                              location.get('name', ''), location.get('address', ''), lat, lon,
                              location.get('placeId', ''), file_name))

    data_headers = (('Visit Start Timestamp', 'datetime'), ('Visit End Timestamp', 'datetime'),
                    'Name', 'Address', 'Latitude', 'Longitude', 'PlaceID', 'File Name')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def takeoutSemanticActivitySegments(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('.json'):
            continue
        source_path = file_found
        file_name = os.path.basename(file_found)
        with open(file_found, encoding='utf-8-sig') as f:
            data = json.load(f)

        for element in data.get('timelineObjects', []):
            if 'activitySegment' not in element:
                continue
            seg = element['activitySegment']
            start_lat = start_lon = 'NOT_SPECIFIED'
            if 'startLocation' in seg:
                start_lat = seg['startLocation']['latitudeE7'] / 1e7 if 'latitudeE7' in seg['startLocation'].keys() else None
                start_lon = seg['startLocation']['longitudeE7'] / 1e7 if 'longitudeE7' in seg['startLocation'].keys() else None
            end_lat = end_lon = 'NOT_SPECIFIED'
            if 'endLocation' in seg:
                end_lat = seg['endLocation']['latitudeE7'] / 1e7 if 'latitudeE7' in seg['endLocation'].keys() else None
                end_lon = seg['endLocation']['longitudeE7'] / 1e7 if 'longitudeE7' in seg['endLocation'].keys() else None
            duration = seg.get('duration', {})
            subactivity_str = ''
            for activity in seg.get('activities', []):
                subactivity_str += f"{activity['activityType']} [{activity['probability']}], "
            data_list.append((_duration_ts(duration, 'start'), _duration_ts(duration, 'end'),
                              start_lat, start_lon, end_lat, end_lon, seg.get('activityType', ''),
                              seg.get('distance', ''), seg.get('confidence', ''),
                              subactivity_str[:-2], file_name))

    data_headers = (('Activity Start Timestamp', 'datetime'), ('Activity End Timestamp', 'datetime'),
                    'Start Latitude', 'Start Longitude', 'End Latitude', 'End Longitude',
                    'Activity Type', 'Distance (Meters)', 'Confidence', 'Activities', 'File Name')
    return data_headers, data_list, context.get_relative_path(source_path)

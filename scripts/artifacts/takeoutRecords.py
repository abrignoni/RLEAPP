__artifacts_v2__ = {
    "takeoutRecords": {
        "name": "Google Location History - Records",
        "description": "Parses Google Takeout Records.json location records with detected activity",
        "author": "cheeky4n6monkey@gmail.com",
        "creation_date": "2022-02-27",
        "last_update_date": "2026-06-27",
        "requirements": "ijson",
        "category": "Google Takeout Archive",
        "notes": "Edited from cheeky4n6monkey/4n6-scripts Google_Takeout_Records.",
        "paths": ('*/Location History*/Records.json'),
        "output_types": ['html', 'tsv', 'timeline', 'lava', 'kml'],
        "artifact_icon": "map-pin",
    }
}

import os
from datetime import datetime

import ijson

from scripts.ilapfuncs import artifact_processor


def _iso_to_utc(value):
    # Records timestamps are ISO-8601 strings (often Z-suffixed); leave placeholders untouched.
    if not value or value in ('NOT_SPECIFIED', 'Not found'):
        return value
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00'))
    except (ValueError, AttributeError):
        return value


@artifact_processor
def takeoutRecords(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found) != 'Records.json':
            continue
        source_path = file_found
        with open(file_found, 'rb') as f:
            for element in ijson.items(f, 'locations.item'):
                if 'activity' not in element:
                    continue
                lat = element['latitudeE7'] / 10000000
                lon = element['longitudeE7'] / 10000000
                accuracy = element.get('accuracy', '')
                altitude = float(element['altitude']) if 'altitude' in element else 'NOT_SPECIFIED'
                vertical_accuracy = element.get('verticalAccuracy', 'NOT_SPECIFIED')
                heading = element.get('heading', 'NOT_SPECIFIED')
                velocity = element.get('velocity', 'NOT_SPECIFIED')
                source = element.get('source', '')
                device = str(element.get('deviceTag', ''))
                platform = element.get('platformType', 'NOT_SPECIFIED')
                form_factor = element.get('formFactor', 'NOT_SPECIFIED')
                element_ts = element.get('timestamp', '')
                server_ts = element.get('serverTimestamp', 'NOT_SPECIFIED')
                device_ts = element.get('deviceTimestamp', 'NOT_SPECIFIED')

                for act in element['activity']:
                    activity_ts = act.get('timestamp', 'Not found')
                    count_sub = 0
                    subactivity_str = ''
                    for subact in act.get('activity', []):
                        count_sub += 1
                        subactivity_str += f"{subact['type']} [{subact['confidence']}], "
                    data_list.append((
                        _iso_to_utc(element_ts), source, device, platform, form_factor,
                        _iso_to_utc(server_ts), _iso_to_utc(device_ts), element_ts,
                        lat, lon, altitude, heading, velocity, accuracy, vertical_accuracy,
                        count_sub, _iso_to_utc(activity_ts), subactivity_str[:-2]))

    data_headers = (('Timestamp', 'datetime'), 'Source', 'Device', 'Platform', 'Form Factor',
                    ('Timestamp Server', 'datetime'), ('Timestamp Device', 'datetime'),
                    'Timestamp Element', 'Latitude', 'Longitude', 'Altitude', 'Heading', 'Velocity',
                    'Accuracy', 'Vertical Accuracy', 'Sub-activity Types',
                    ('Timestamp Activity', 'datetime'), 'Detected Activity')
    return data_headers, data_list, context.get_relative_path(source_path)

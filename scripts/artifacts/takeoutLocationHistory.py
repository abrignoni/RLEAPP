__artifacts_v2__ = {
    "takeoutLocationHistory": {
        "name": "Google Location History - Location History",
        "description": "Parses Google Takeout Location History.json (locations with detected activity)",
        "author": "@KevinPagano3 & @Cheeky4n6Monkey",
        "creation_date": "2021-09-21",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "Reworked from cheeky4n6monkey/4n6-scripts Google_Takeout_Location_History.",
        "paths": ('*/Location History/Location History.json', '*/Location History.json'),
        "output_types": ['html', 'tsv', 'timeline', 'lava', 'kml'],
        "artifact_icon": "map-pin",
    }
}

import json
import os

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


@artifact_processor
def takeoutLocationHistory(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found) != 'Location History.json':
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            data = json.load(f)

        for element in data.get('locations', []):
            timestamp = convert_unix_ts_to_utc(element['timestampMs']) if element.get('timestampMs') else ''
            lat = element['latitudeE7'] / 10000000
            lon = element['longitudeE7'] / 10000000
            accuracy = element.get('accuracy', '')
            altitude = float(element['altitude']) if 'altitude' in element else 'NOT_SPECIFIED'
            vertical_accuracy = element.get('verticalAccuracy', 'NOT_SPECIFIED')
            heading = element.get('heading', 'NOT_SPECIFIED')
            velocity = element.get('velocity', 'NOT_SPECIFIED')
            source = element.get('source', 'NOT_SPECIFIED')
            device = str(element['deviceTag']) if 'deviceTag' in element else 'NOT_SPECIFIED'
            platform = element.get('platformType', 'NOT_SPECIFIED')

            for activity in element.get('activity', []):
                activity_ts = convert_unix_ts_to_utc(activity['timestampMs']) if activity.get('timestampMs') else ''
                count_sub = 0
                subactivity_str = ''
                for subact in activity.get('activity', []):
                    count_sub += 1
                    subactivity_str += f"{subact['type']} [{subact['confidence']}], "
                data_list.append((timestamp, source, device, platform, lat, lon, altitude,
                                  heading, velocity, accuracy, vertical_accuracy, count_sub,
                                  activity.get('timestampMs', ''), activity_ts, subactivity_str[:-2]))

    data_headers = (('Timestamp', 'datetime'), 'Source', 'Device Tag', 'Platform', 'Latitude',
                    'Longitude', 'Altitude', 'Heading (Degrees)', 'Velocity', 'Accuracy',
                    'Vertical Accuracy', 'Activity', 'Sub-activity Types',
                    ('Timestamp Activity', 'datetime'), 'Detected Activity')
    return data_headers, data_list, context.get_relative_path(source_path)

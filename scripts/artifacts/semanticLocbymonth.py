__artifacts_v2__ = {
    "semanticLocationsMonthPlaces": {
        "name": "Semantic Locations - Places By Month",
        "description": "Parses placeVisit entries from Google Takeout per-month Semantic Location History JSON files",
        "author": "@AlexisBrignoni",
        "creation_date": "2023-05-28",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": ('*/Location History*/Semantic Location History/*/*_*.json',),
        "output_types": ['html', 'tsv', 'timeline', 'lava', 'kml'],
        "artifact_icon": "map-pin",
    },
    "semanticLocationsMonthActivity": {
        "name": "Semantic Locations - Activity By Month",
        "description": "Parses activitySegment entries from Google Takeout per-month Semantic Location History JSON files",
        "author": "@AlexisBrignoni",
        "creation_date": "2023-05-28",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "Start/End/Parking coordinates are separate columns and waypoint coordinates are aggregated into the Waypoints cell; the original per-segment waypoint-track KML is not auto-emitted.",
        "paths": ('*/Location History*/Semantic Location History/*/*_*.json',),
        "output_types": "standard",
        "html_columns": ["Waypoints"],
        "artifact_icon": "navigation",
    }
}

import json
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor


def _iso_to_utc(value):
    if not value:
        return value
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(timezone.utc)
    except (ValueError, AttributeError):
        return value


@artifact_processor
def semanticLocationsMonthPlaces(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('.json'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            data = json.load(f)

        for record in data.get('timelineObjects', []):
            if 'placeVisit' not in record:
                continue
            pv = record['placeVisit']
            location = pv.get('location', {})
            source_info = location.get('sourceInfo', {})
            devicetag = source_info.get('deviceTag', '') if isinstance(source_info, dict) else ''
            center_lat = pv['centerLatE7'] / 1e7 if 'centerLatE7' in pv else ''
            center_lng = pv['centerLngE7'] / 1e7 if 'centerLngE7' in pv else ''
            duration = pv.get('duration', {})
            data_list.append((
                _iso_to_utc(duration.get('startTimestamp', '')),
                _iso_to_utc(duration.get('endTimestamp', '')), 'placeVisit',
                center_lat, center_lng,
                location.get('latitudeE7', 0) / 1e7, location.get('longitudeE7', 0) / 1e7,
                location.get('placeId', ''), location.get('name', ''), location.get('address', ''),
                devicetag, location.get('locationConfidence', ''),
                location.get('calibratedProbability', ''), pv.get('visitConfidence', ''),
                pv.get('locationConfidence', ''), pv.get('placeVisitType', ''),
                pv.get('placeVisitImportance', '')))

    data_headers = (('Timestamp', 'datetime'), ('End Timestamp', 'datetime'), 'Record',
                    'Latitude', 'Longitude', 'Additional Latitude', 'Additional Longitude',
                    'Place ID', 'Name', 'Address', 'Device Tag', 'Location Confidence',
                    'Calculated Probability', 'Visit Confidence', 'Visit Location Confidence',
                    'Place Visit Type', 'Place Visit Importance')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def semanticLocationsMonthActivity(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('.json'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            data = json.load(f)

        for record in data.get('timelineObjects', []):
            if 'activitySegment' not in record:
                continue
            seg = record['activitySegment']
            start_lat = seg['startLocation']['latitudeE7'] / 1e7 if 'startLocation' in seg else ''
            start_lon = seg['startLocation']['longitudeE7'] / 1e7 if 'startLocation' in seg else ''
            end_lat = seg['endLocation']['latitudeE7'] / 1e7 if 'endLocation' in seg else ''
            end_lon = seg['endLocation']['longitudeE7'] / 1e7 if 'endLocation' in seg else ''
            duration = seg.get('duration', {})
            activities = seg.get('activities', [])
            high_prob_type = activities[0]['activityType'] if activities else ''
            high_prob_num = activities[0]['probability'] if activities else ''

            waypoint_path = seg.get('waypointPath', {})
            waypoints = waypoint_path.get('waypoints', []) if isinstance(waypoint_path, dict) else []
            agg_parts = []
            if waypoints:
                agg_parts.append(f'{start_lat},{start_lon}')
                agg_parts.append(f'{end_lat},{end_lon}')
                for pt in waypoints:
                    agg_parts.append(f"{pt['latE7'] / 1e7},{pt['lngE7'] / 1e7}")
            agg = '<br>'.join(agg_parts)

            parking = seg.get('parkingEvent', {})
            if parking:
                ploc = parking.get('location', {})
                parking_lat = ploc.get('latitudeE7', 0) / 1e7
                parking_lon = ploc.get('longitudeE7', 0) / 1e7
                parking_acc = ploc.get('accuracyMetres', '')
                parking_time = _iso_to_utc(parking.get('timestamp', ''))
            else:
                parking_lat = parking_lon = parking_acc = parking_time = ''

            data_list.append((
                _iso_to_utc(duration.get('startTimestamp', '')),
                _iso_to_utc(duration.get('endTimestamp', '')), 'activitySegment',
                start_lat, start_lon, end_lat, end_lon, seg.get('distance', ''),
                seg.get('activityType', ''), seg.get('confidence', ''), high_prob_type,
                high_prob_num, agg, parking_time, parking_lat, parking_lon, parking_acc))

    data_headers = (('Timestamp', 'datetime'), ('End Timestamp', 'datetime'), 'Record',
                    'Start Latitude', 'Start Longitude', 'End Latitude', 'End Longitude',
                    'Distance', 'Activity Type', 'Confidence', 'Highest Activity Type Probability',
                    'Activity High Probability Percentage', 'Waypoints',
                    ('Parking Location Time', 'datetime'), 'Parking Location Latitude',
                    'Parking Location Longitude', 'Parking Accuracy in Meters')
    return data_headers, data_list, context.get_relative_path(source_path)

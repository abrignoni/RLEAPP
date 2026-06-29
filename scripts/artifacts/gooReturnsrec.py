__artifacts_v2__ = {
    "gooReturnsrec": {
        "name": "Google Returns - Location History Records",
        "description": "Location History activity records (Records.json) from a Google return.",
        "author": "cheeky4n6monkey@gmail.com",
        "creation_date": "2022-05-29",
        "last_update_date": "2026-06-28",
        "requirements": "ijson",
        "category": "Google Returns",
        "notes": "Parses the same source as the Takeout 'Google Location History - Records' "
                 "artifact. Latitude/Longitude are exposed for KML; timestamps normalized to UTC "
                 "(unspecified values are kept verbatim, e.g. NOT_SPECIFIED / Not found).",
        "paths": ('*/Location History*/Records.json',),
        "output_types": ['html', 'tsv', 'timeline', 'lava', 'kml'],
        "artifact_icon": "map-pin",
    }
}

import os
from datetime import datetime, timezone

import ijson

from scripts.ilapfuncs import artifact_processor


def _ts(value):
    text = str(value or '').strip()
    if not text or text in ('NOT_SPECIFIED', 'Not found'):
        return value
    cleaned = text.replace('T', ' ').replace('Z', '')
    try:
        dt = datetime.fromisoformat(cleaned)
        return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)
    except ValueError:
        return value


@artifact_processor
def gooReturnsrec(context):
    data_list, source_path = [], ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found) != 'Records.json':
            continue
        source_path = file_found
        folder_dict = {}
        with open(file_found, encoding='utf-8') as f:
            document = f.read()

        for element in ijson.items(document, 'locations.item'):
            if 'activity' not in element:
                continue
            element_lat = float(element["latitudeE7"] / 10000000)
            element_llg = float(element["longitudeE7"] / 10000000)
            element_accuracy = str(element["accuracy"])
            element_alt = str(float(element["altitude"])) if "altitude" in element else "NOT_SPECIFIED"
            element_vacc = str(element["verticalAccuracy"]) if "verticalAccuracy" in element else "NOT_SPECIFIED"
            element_heading = str(element["heading"]) if "heading" in element else "NOT_SPECIFIED"
            element_velocity = str(element["velocity"]) if "velocity" in element else "NOT_SPECIFIED"
            element_source = element["source"]
            element_device = str(element["deviceTag"])
            element_platform = element["platformType"] if "platformType" in element else "NOT_SPECIFIED"
            element_form = element["formFactor"] if "formFactor" in element else "NOT_SPECIFIED"
            element_ts = element["timestamp"]
            server_ts = element["serverTimestamp"] if "serverTimestamp" in element else "NOT_SPECIFIED"
            device_ts = element["deviceTimestamp"] if "deviceTimestamp" in element else "NOT_SPECIFIED"

            for act in element["activity"]:
                activity_ts = act["timestamp"] if "timestamp" in act else "Not found"
                subactivity = ''
                for subact in act["activity"]:
                    subactivity += f'{subact["type"]} [{subact["confidence"]}], '
                folderid = element_ts.split("T")[0]
                element_ts_clean = element_ts.replace('T', ' ').replace('Z', '')
                row = (_ts(element_ts_clean), element_source, element_device, element_platform,
                       element_form, _ts(server_ts), _ts(device_ts), _ts(element_ts), element_lat,
                       element_llg, element_alt, element_heading, element_velocity,
                       element_accuracy, element_vacc, len(act["activity"]), _ts(activity_ts),
                       subactivity[:-2])
                folder_dict.setdefault(folderid, []).append(row)

        for rows in folder_dict.values():
            data_list.extend(rows)

    data_headers = (('Timestamp', 'datetime'), 'Source', 'Device', 'Platform', 'Form Factor',
                    ('Timestamp Server', 'datetime'), ('Timestamp Device', 'datetime'),
                    ('Timestamp Element', 'datetime'), 'Latitude', 'Longitude', 'Altitude',
                    'Heading', 'Velocity', 'Accuracy', 'Vertical Accuracy', 'Sub-activity Count',
                    ('Timestamp Activity', 'datetime'), 'Detected Activity')
    return data_headers, data_list, context.get_relative_path(source_path)

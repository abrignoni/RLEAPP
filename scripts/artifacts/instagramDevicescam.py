__artifacts_v2__ = {
    "instagramDevicescam": {
        "name": "Instagram Archive - Camera Info",
        "description": "Parses camera device information from an Instagram data archive (camera_information.json)",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-21",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Instagram Archive",
        "notes": "",
        "paths": ('*/device_information/camera_information.json'),
        "output_types": "standard",
        "artifact_icon": "brand-instagram",
    }
}

import os
import json

from scripts.ilapfuncs import artifact_processor


@artifact_processor
def instagramDevicescam(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found).startswith('camera_information.json'):
            source_path = file_found
            with open(file_found, 'r', encoding='utf-8') as fp:
                deserialized = json.load(fp)

            for x in deserialized['devices_camera']:
                smd = x['string_map_data']
                deviceid = smd['Device ID'].get('value', '')
                compression = smd['Compression'].get('value', '')
                ftversion = smd['Face Tracker Version'].get('value', '')
                sdksup = smd['Supported SDK Versions'].get('value', '')
                data_list.append((deviceid, compression, ftversion, sdksup))

    data_headers = ('Device ID', 'Compression', 'Face Tracker Version', 'Supported SDK Versions')
    return data_headers, data_list, context.get_relative_path(source_path)

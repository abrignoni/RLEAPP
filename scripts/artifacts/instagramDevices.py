__artifacts_v2__ = {
    "instagramDevices": {  # This should match the function name exactly
        "name": "Instagram Archive - Devices",
        "description": "Parses device information the Instagram account was used on",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-30",
        "last_update_date": "2025-07-03",
        "requirements": "none",
        "category": "Instagram Archive",
        "notes": "",
        "paths": ('*/device_information/devices.json'),
        "output_types": "standard",  # or ["html", "tsv", "timeline", "lava"]
        "artifact_icon": "instagram",
    }
}

import os
import datetime
import json
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import artifact_processor

@artifact_processor
def instagramDevices(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
    
        if filename.startswith('devices.json'):
            data_list =[]
            with open(file_found, "rb") as fp:
                deserialized = json.load(fp)
            
            devices = (deserialized['devices_devices'])
            for x in devices:
                if 'Device ID' in x['string_map_data']:
                    deviceid = (x['string_map_data']['Device ID'].get('value', ''))
                else:
                    deviceid = ''
                timestamp = (x['string_map_data']['Last Login'].get('timestamp', ''))
                if timestamp > 0:
                    timestamp = (datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
                useragent = (x['string_map_data']['User Agent'].get('value', ''))
                    
                data_list.append((timestamp, deviceid, useragent))
    
    data_headers = ('Last Login Timestamp', 'Device ID', 'User Agent')
    return data_headers, data_list, file_found
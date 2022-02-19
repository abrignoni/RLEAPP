import os
import datetime
import json
import magic
import shutil
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows

def get_instagramDevices(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
    
        if filename.startswith('devices.json'):
            data_list =[]
            with open(file_found, "rb") as fp:
                deserialized = json.load(fp)
                
            devices = (deserialized['devices_devices'])
            for x in devices:
                deviceid = (x['string_map_data']['Device ID'].get('value', ''))
                timestamp = (x['string_map_data']['Last Login'].get('timestamp', ''))
                if timestamp > 0:
                    timestamp = (datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
                useragent = (x['string_map_data']['User Agent'].get('value', ''))
                    
                data_list.append((timestamp, deviceid, useragent))
                    
                
            if data_list:
                report = ArtifactHtmlReport('Instagram Archive - Devices')
                report.start_artifact_report(report_folder, 'Instagram Archive - Devices')
                report.add_script()
                data_headers = ('Last Login Timestamp', 'Device ID', 'User Agent')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Instagram Archive - Devices'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                tlactivity = f'Instagram Archive - Devices'
                timeline(report_folder, tlactivity, data_list, data_headers)
                
            else:
                logfunc('No Instagram Archive - Devices data available')
                
        
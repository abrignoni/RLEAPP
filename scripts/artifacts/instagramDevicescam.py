import os
import datetime
import json
import magic
import shutil
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows

def get_instagramDevicescam(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
    
        if filename.startswith('camera_information.json'):
            data_list =[]
            with open(file_found, "rb") as fp:
                deserialized = json.load(fp)
                
            devices = (deserialized['devices_camera'])
            for x in devices:
                
                deviceid = (x['string_map_data']['Device ID'].get('value', ''))
                compression = (x['string_map_data']['Compression'].get('value', ''))
                ftversion = (x['string_map_data']['Face Tracker Version'].get('value', ''))
                sdksup = (x['string_map_data']['Supported SDK Versions'].get('value', ''))
                
                    
                data_list.append((deviceid, compression, ftversion, sdksup))
                
                
            if data_list:
                report = ArtifactHtmlReport('Instagram Archive - Camera Info')
                report.start_artifact_report(report_folder, 'Instagram Archive - Camera Info')
                report.add_script()
                data_headers = ('Device ID', 'Compression', 'Face Tracker Version', 'Supported SDK Versions')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Instagram Archive - Camera Info'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                tlactivity = f'Instagram Archive - Camera Info'
                timeline(report_folder, tlactivity, data_list, data_headers)
                
            else:
                logfunc('No Instagram Archive - Camera Info data available')
                
        
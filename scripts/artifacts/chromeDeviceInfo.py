# Module Description: Parses Google Chrome synced device information from Takeout
# Author: @KevinPagano3
# Date: 2023-08-24
# Artifact version: 0.0.1
# Requirements: none

import datetime
import json
import os
import textwrap

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_chromeDeviceInfo(files_found, report_folder, seeker, wrap_text, time_offset):

    for file_found in files_found:
        file_found = str(file_found)

        with open(file_found, encoding = 'utf-8', mode = 'r') as f:
            data = json.loads(f.read())
        data_list = []
        
        if 'Device Info' in data:
            for device in data['Device Info']:
                last_updated_timestamp = device.get('last_updated_timestamp','')
                last_updated_timestamp = datetime.datetime.utcfromtimestamp((int(last_updated_timestamp)/1000)).strftime('%Y-%m-%d %H:%M:%S')
                
                manufacturer = device.get('manufacturer','')
                model = device.get('model','')
                client_name = device.get('client_name','')
                os_type = device.get('os_type','')[8:]
                device_type = device.get('device_type','')[5:]
                chrome_version = device.get('chrome_version','')
                sync_user_agent = device.get('sync_user_agent','')
                signin_scoped_device_id = device.get('signin_scoped_device_id','')
                
                data_list.append((last_updated_timestamp,manufacturer,model,client_name,os_type,device_type,chrome_version,sync_user_agent,textwrap.fill(signin_scoped_device_id,width=100)))

        num_entries = len(data_list)
        if num_entries > 0:
            report = ArtifactHtmlReport('Chrome Device Info')
            report.start_artifact_report(report_folder, 'Chrome Device Info')
            report.add_script()
            data_headers = ('Last Updated Timestamp','Manufacturer','Model','Client Name','OS Type','Device Type','Chrome Version','User Agent','Device ID')

            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()

            tsvname = f'Chrome Device Info'
            tsv(report_folder, data_headers, data_list, tsvname)

            tlactivity = f'Chrome Device Info'
            timeline(report_folder, tlactivity, data_list, data_headers)
        else:
            logfunc('No Chrome Device Info data available')

__artifacts__ = {
        "chromeDeviceInfo": (
            "Google Takeout Archive",
            ('*/Chrome/Device Information.json'),
            get_chromeDeviceInfo)
}
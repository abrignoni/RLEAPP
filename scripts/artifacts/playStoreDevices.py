# Module Description: Parses Google Play Store devices from Takeout
# Author: @KevinPagano3
# Date: 2021-08-22
# Artifact version: 0.0.1
# Requirements: none

import datetime
import json
import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_playStoreDevices(files_found, report_folder, seeker, wrap_text, time_offset):
    
    for file_found in files_found:
        file_found = str(file_found)
        if not os.path.basename(file_found) == 'Devices.json': # skip -journal and other files
            continue

        with open(file_found, encoding = 'utf-8', mode = 'r') as f:
            data = json.loads(f.read())
        data_list = []

        for x in range(0, len(data)):
            carrierName = data[x]['device']['mostRecentData']['carrierName']
            manufacturer = data[x]['device']['mostRecentData']['manufacturer']
            modelName = data[x]['device']['mostRecentData']['modelName']
            deviceName = data[x]['device']['mostRecentData']['deviceName']
            totalMemoryBytes = str(round(int(data[x]['device']['mostRecentData']['totalMemoryBytes'])/1000000000,2))
            deviceIpCountry = data[x]['device']['mostRecentData']['deviceIpCountry']
            androidSdkVersion = data[x]['device']['mostRecentData']['androidSdkVersion']
            deviceRegistrationTime = data[x]['device']['deviceRegistrationTime']
            deviceRegistrationTime = deviceRegistrationTime.replace('T', ' ').replace('Z', '')
            userAddedOnDeviceTime = data[x]['device']['userAddedOnDeviceTime']
            userAddedOnDeviceTime = userAddedOnDeviceTime.replace('T', ' ').replace('Z', '')
            lastTimeDeviceActive = data[x]['device']['lastTimeDeviceActive']
            lastTimeDeviceActive = lastTimeDeviceActive.replace('T', ' ').replace('Z', '')
                   
            data_list.append((deviceRegistrationTime, userAddedOnDeviceTime, lastTimeDeviceActive, manufacturer, modelName, totalMemoryBytes, carrierName, deviceIpCountry, deviceName, androidSdkVersion))
        
        num_entries = len(data_list)
        if num_entries > 0:
            description = 'Metadata about your devices that have accessed the Google Play Store.'
            report = ArtifactHtmlReport('Google Play Store Devices')
            report.start_artifact_report(report_folder, 'Google Play Store Devices',description)
            report.add_script()
            data_headers = ('Device Registration Timestamp','User Added Timestamp','Last Device Active Timestamp','Device Manufacturer','Device Model','Device RAM (GBs)','Carrier','Device IP Country','Device Name','SDK Version  ')

            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()
            
            tsvname = f'Google Play Store Devices'
            tsv(report_folder, data_headers, data_list, tsvname)
            
            tlactivity = f'Google Play Store Devices'
            timeline(report_folder, tlactivity, data_list, data_headers)
        else:
            logfunc('No Google Play Store Devices data available')

__artifacts__ = {
        "playStoreDevices": (
            "Google Takeout Archive",
            ('*/Google Play Store/Devices.json'),
            get_playStoreDevices)
}
# Module Description: Parses Google Play Store application installations from Takeout
# Author: @KevinPagano3
# Date: 2021-08-22
# Artifact version: 0.0.1
# Requirements: none

import datetime
import json
import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_playStoreInstalls(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        if not os.path.basename(file_found) == 'Installs.json': # skip -journal and other files
            continue

        with open(file_found, encoding = 'utf-8', mode = 'r') as f:
            data = json.loads(f.read())
        data_list = []

        for x in data:
            docType = x['install']['doc'].get('documentType','')
            title = x['install']['doc'].get('title','')
            firstInstallationTime = x['install'].get('firstInstallationTime','')
            firstInstallationTime = firstInstallationTime.replace('T', ' ').replace('Z', '')
            lastUpdateTime = x['install'].get('lastUpdateTime','')
            lastUpdateTime = lastUpdateTime.replace('T', ' ').replace('Z', '')
            model = x['install']['deviceAttribute'].get('model','')
            carrier  = x['install']['deviceAttribute'].get('carrier','')
            manufacturer = x['install']['deviceAttribute'].get('manufacturer','')
            deviceDisplayName = x['install']['deviceAttribute'].get('deviceDisplayName','')
            
            data_list.append((firstInstallationTime, lastUpdateTime, title, docType, manufacturer, model, carrier, deviceDisplayName))
    
        num_entries = len(data_list)
        if num_entries > 0:
            description = 'List of your Google Play app installs.'
            report = ArtifactHtmlReport('Google Play Store Installs')
            report.start_artifact_report(report_folder, 'Google Play Store Installs',description)
            report.add_script()
            data_headers = ('First Install Timestamp','Last Update Timestamp','Title','Type','Device Manufacturer','Device Model','Carrier','Device Display Name')

            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()
            
            tsvname = f'Google Play Store Installs'
            tsv(report_folder, data_headers, data_list, tsvname)
            
            tlactivity = f'Google Play Store Installs'
            timeline(report_folder, tlactivity, data_list, data_headers)
        else:
            logfunc('No Google Play Store Installs data available')

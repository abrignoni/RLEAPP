# Module Description: Parses Google Play Store subscriptions from Takeout
# Author: @KevinPagano3
# Date: 2021-08-22
# Artifact version: 0.0.1
# Requirements: none

import datetime
import json
import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_playStoreSubscriptions(files_found, report_folder, seeker, wrap_text, time_offset):
    
    for file_found in files_found:
        file_found = str(file_found)
        if not os.path.basename(file_found) == 'Subscriptions.json': # skip -journal and other files
            continue

        with open(file_found, encoding = 'utf-8', mode = 'r') as f:
            data = json.loads(f.read())
        data_list = []

        for x in data:
            price = x['subscription'].get('price','')
            docType = x['subscription']['doc'].get('documentType','')
            title = x['subscription']['doc'].get('title','')
            renewalDate = x['subscription'].get('renewalDate','')
            renewalDate = renewalDate.replace('T', ' ').replace('Z', '')
            renewalPrice = x['subscription']['pricing'][0].get('price','')
            renewalUnit = x['subscription']['pricing'][0]['period'].get('unit','')
            renewalCount = x['subscription']['pricing'][0]['period'].get('count','')
            renewalPeriod = str(renewalCount) + ' / ' + renewalUnit
            state = x['subscription'].get('state','')
            
            data_list.append((renewalDate, title, renewalPrice, renewalPeriod, state))
    
        num_entries = len(data_list)
        if num_entries > 0:
            description = 'List of your Google Play subscriptions.'
            report = ArtifactHtmlReport('Google Play Store Subscriptions')
            report.start_artifact_report(report_folder, 'Google Play Store Subscriptions', description)
            report.add_script()
            data_headers = ('Renewal Timestamp','Subscription','Renewal Price','Renewal Period','Status')

            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()
            
            tsvname = f'Google Play Store Subscriptions'
            tsv(report_folder, data_headers, data_list, tsvname)
            
            tlactivity = f'Google Play Store Subscriptions'
            timeline(report_folder, tlactivity, data_list, data_headers)
        else:
            logfunc('No Google Play Store Subscriptions data available')

__artifacts__ = {
        "playStoreSubscriptions": (
            "Google Takeout Archive",
            ('*/Google Play Store/Subscriptions.json'),
            get_playStoreSubscriptions)
}
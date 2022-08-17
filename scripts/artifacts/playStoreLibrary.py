# Module Description: Parses Google Play Store library of music, movies and apps from Takeout
# Author: @KevinPagano3
# Date: 2021-08-22
# Artifact version: 0.0.1
# Requirements: none

import datetime
import json
import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_playStoreLibrary(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        if not os.path.basename(file_found) == 'Library.json': # skip -journal and other files
            continue

        with open(file_found, encoding = 'utf-8', mode = 'r') as f:
            data = json.loads(f.read())
        data_list = []

        for x in data:
            docType = x['libraryDoc']['doc'].get('documentType','')
            title = x['libraryDoc']['doc'].get('title','')
            acquisitionTime = x['libraryDoc'].get('acquisitionTime','')
            acquisitionTime = acquisitionTime.replace('T', ' ').replace('Z', '')
    
            data_list.append((acquisitionTime, title, docType))

        num_entries = len(data_list)
        if num_entries > 0:
            description = 'List of your Google Play downloads including music, movies and apps.'
            report = ArtifactHtmlReport('Google Play Store Library')
            report.start_artifact_report(report_folder, 'Google Play Store Library', description)
            report.add_script()
            data_headers = ('Added Timestamp','Title','Type')

            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()
            
            tsvname = f'Google Play Store Library'
            tsv(report_folder, data_headers, data_list, tsvname)
            
            tlactivity = f'Google Play Store Library'
            timeline(report_folder, tlactivity, data_list, data_headers)
        else:
            logfunc('No Google Play Store Library data available')

__artifacts__ = {
        "playStoreLibrary": (
            "Google Takeout Archive",
            ('*/Google Play Store/Library.json'),
            get_playStoreLibrary)
}
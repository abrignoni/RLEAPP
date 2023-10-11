# Module Description: Parses Google Play Store reviews from Takeout
# Author: @KevinPagano3
# Date: 2021-08-23
# Artifact version: 0.0.1
# Requirements: none

import datetime
import json
import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_playStoreReviews(files_found, report_folder, seeker, wrap_text, time_offset):
    
    for file_found in files_found:
        file_found = str(file_found)
        if not os.path.basename(file_found) == 'Reviews.json': # skip -journal and other files
            continue

        with open(file_found, encoding = 'utf-8', mode = 'r') as f:
            data = json.loads(f.read())
        data_list = []

        for x in data:
            creationTime = x['review'].get('creationTime','')
            creationTime = creationTime.replace('T', ' ').replace('Z', '')
            title = x['review']['document'].get('title','')
            comment = x['review'].get('comment','')
            reviewTitle = x['review'].get('title','')
            starRating = x['review'].get('starRating','')
            docType = x['review']['document'].get('documentType','')

            data_list.append((creationTime, title, comment, reviewTitle, starRating, docType))
    
        num_entries = len(data_list)
        if num_entries > 0:
            description = 'Details about your Google Play reviews.'
            report = ArtifactHtmlReport('Google Play Store Reviews')
            report.start_artifact_report(report_folder, 'Google Play Store Reviews', description)
            report.add_script()
            data_headers = ('Creation Timestamp','Title','Comment','Review Title','Star Rating','Type')

            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()
            
            tsvname = f'Google Play Store Reviews'
            tsv(report_folder, data_headers, data_list, tsvname)
            
            tlactivity = f'Google Play Store Reviews'
            timeline(report_folder, tlactivity, data_list, data_headers)
        else:
            logfunc('No Google Play Store Reviews data available')

__artifacts__ = {
        "playStoreReviews": (
            "Google Takeout Archive",
            ('*/Google Play Store/Reviews.json'),
            get_playStoreReviews)
}
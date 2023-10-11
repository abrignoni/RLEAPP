# Module Description: Parses Google data from a search warrant
# Author: @Alexis Brignoni
# Date: 2023-05-16
# Artifact version: 0.0.1
# Requirements: none

import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html

def get_googleMyactisearch(files_found, report_folder, seeker, wrap_text, time_offset):
    
    data_list = []
    reportcount = 0
    
    for file_found in files_found:
        file_found = str(file_found)
        
        reportname = file_found.split('/')
        reportname = reportname[-3]
        
        with open(file_found, encoding = 'utf-8', mode = 'r') as f:
            data = f.read()

        data_list.append((data,))

        num_entries = len(data_list)
        if num_entries > 0:
            report = ArtifactHtmlReport(f'{reportname}')
            report.start_artifact_report(report_folder, f'Act. Image Search Report {reportcount}')
            report.add_script()
            data_headers = ('HTML File',)
    
            report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['HTML File'])
            report.end_artifact_report()
            
            reportcount = reportcount + 1
            data_list = []
    
        else:
            logfunc(f'No Google data for {reportname}')
 
__artifacts__ = {
        "googleMyactisearch": (
            "Google Returns My Activity Image Search",
            (('*/*MyActivity.MyActivity_*/My Activity/Image Search/MyActivity.html')),
            get_googleMyactisearch)
}

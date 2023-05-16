# Module Description: Parses Google data from a search warrant
# Author: @Alexis Brignoni
# Date: 2023-05-16
# Artifact version: 0.0.1
# Requirements: none

import os
import csv

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html

def get_googlelinkedbycookies(files_found, report_folder, seeker, wrap_text):
    
    data_list = []
    reportcount = 0
    
    for file_found in files_found:
        file_found = str(file_found)
        
        reportname = file_found.split('/')
        reportname = reportname[-3]
        
        with open(file_found, 'r') as f:
            delimited = csv.reader(f, delimiter=',')
            firsrowindicator = 0
            
            for item in delimited:
                if firsrowindicator == 0:
                    data_headers = item
                    firsrowindicator = 1
                elif item == []:
                    pass
                else:
                    data_list.append((item))

        num_entries = len(data_list)
        if num_entries > 0:
            report = ArtifactHtmlReport(f'{reportname}')
            report.start_artifact_report(report_folder, f'Report {reportcount}')
            report.add_script()
            #data_headers = ('HTML File',)
    
            report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['HTML File'])
            report.end_artifact_report()
            
            reportcount = reportcount + 1
            data_list = []
    
        else:
            logfunc(f'No Google data for {reportname}')
 
__artifacts__ = {
        "googlelinkedbycookies": (
            "Google Returns Account Target Assoc. Cookies",
            (('*/*GoogleAccountTargetAssociation.LinkedByCookies_*/Google Account Target Association/*.LinkedByCookies.csv')),
            get_googlelinkedbycookies)
}

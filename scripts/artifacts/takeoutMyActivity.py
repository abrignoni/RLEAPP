# Module Description: Parses Google Takeout My Activity HTML files
# Author: Gemini
# Artifact version: 1.0
# Requirements: none

import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html

def get_takeoutMyActivityHtml(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        
        # Extract service name from path: .../My Activity/Service Name/MyActivity.html
        path_parts = os.path.normpath(file_found).split(os.sep)
        try:
            my_activity_index = path_parts.index('My Activity')
            service_name = path_parts[my_activity_index + 1]
        except (ValueError, IndexError):
            service_name = "Unknown"
        
        with open(file_found, encoding = 'utf-8', mode = 'r') as f:
            data = f.read()
        
        data_list = [(data,)]
        
        if data_list:
            report = ArtifactHtmlReport(f'Google Takeout - My Activity - {service_name}')
            description = f'MyActivity.html file for the {service_name} service.'
            report.start_artifact_report(report_folder, f'My Activity - {service_name}', description)
            report.add_script()
            data_headers = ('HTML File',)
    
            report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['HTML File'])
            report.end_artifact_report()

        else:
            logfunc(f'No Google data for {service_name}')

__artifacts_v2__ = {
    "takeoutMyActivity": {
        "name": "Google Takeout My Activity",
        "description": "Parses and displays MyActivity.html files from Google Takeout for various services (e.g., Ads, Chrome, YouTube).",
        "author": "Gemini",
        "version": "1.2",
        "date": "2025-07-21",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "This artifact embeds the original HTML file from the Takeout into the report, allowing for manual review. It creates a separate report for each service's MyActivity.html file found.",
        "paths": ('*/My Activity/*/MyActivity.html',),
        "function": "get_takeoutMyActivityHtml"
    }
}
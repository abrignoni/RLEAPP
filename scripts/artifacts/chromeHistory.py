import datetime
import json
import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_chromeHistory(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        if not os.path.basename(file_found) == 'BrowserHistory.json': # skip -journal and other files
            continue

        with open(file_found, "r") as f:
            data = json.loads(f.read())
        data_list = []
        url = ''
        title = ''
        timestamp = ''
        page_transition = ''

        for site in data['Browser History']:
            
            url = site['url']
            title = site['title']
            timestamp = datetime.datetime.fromtimestamp(int(site['time_usec'])/1000000).strftime('%Y-%m-%d %H:%M:%S.%f')
            page_transition = site['page_transition']

            data_list.append((timestamp, title, url, page_transition))

        num_entries = len(data_list)
        if num_entries > 0:
            report = ArtifactHtmlReport('Chrome Web History')
            report.start_artifact_report(report_folder, 'Chrome Web History')
            report.add_script()
            data_headers = ('Timestamp','Webpage Title','URL','Page Transition') 

            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()
            
            tsvname = f'Chrome Web History'
            tsv(report_folder, data_headers, data_list, tsvname)
            
            tlactivity = f'Chrome Web History'
            timeline(report_folder, tlactivity, data_list, data_headers)
        else:
            logfunc('No Chrome Web History data available')

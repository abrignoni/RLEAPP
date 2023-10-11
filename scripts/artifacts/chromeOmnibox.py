# Module Description: Parses Google Chrome Omnibox / typed URL value information from Takeout
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

def get_chromeOmnibox(files_found, report_folder, seeker, wrap_text, time_offset):

    for file_found in files_found:
        file_found = str(file_found)
        if not os.path.basename(file_found) == 'Omnibox.json': 
            continue

        with open(file_found, encoding = 'utf-8', mode = 'r') as f:
            data = json.loads(f.read())
        data_list = []
        
        if 'Typed Url' in data:
            for site in data['Typed Url']:
                visit_ts = site['visits']
                hidden = site['hidden']
                title = site['title']
                url = site['url']
                #count = len(visit_ts)

                for stamp in visit_ts:
                    timestamp = datetime.datetime.utcfromtimestamp((int(stamp)/1000000)-11644473600).strftime('%Y-%m-%d %H:%M:%S')

                    data_list.append((timestamp, title, textwrap.fill(url, width=100), hidden))

        num_entries = len(data_list)
        if num_entries > 0:
            report = ArtifactHtmlReport('Chrome Omnibox')
            report.start_artifact_report(report_folder, 'Chrome Omnibox')
            report.add_script()
            data_headers = ('Visit Timestamp','Title','URL','Hidden')

            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()

            tsvname = f'Chrome Omnibox'
            tsv(report_folder, data_headers, data_list, tsvname)

            tlactivity = f'Chrome Omnibox'
            timeline(report_folder, tlactivity, data_list, data_headers)
        else:
            logfunc('No Chrome Omnibox data available')

__artifacts__ = {
        "chromeOmnibox": (
            "Google Takeout Archive",
            ('*/Chrome/Omnibox.json'),
            get_chromeOmnibox)
}
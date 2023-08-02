# Module Description: Parses Google Chrome Autofill (not autofill profile) information from Takeout
# Author: @upintheairsheep
# Date: 2023-08-01
# Artifact version: 0
# Requirements: none

import datetime
import json
import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_chromeAutofillInfo(files_found, report_folder, seeker, wrap_text):

    for file_found in files_found:
        file_found = str(file_found)
        if not os.path.basename(file_found) == 'Autofill.json': 
            continue

        with open(file_found, encoding = 'utf-8', mode = 'r') as f:
            data = json.loads(f.read())
        data_list = []

        chromeautofill_name = ''
        chromeautofill_value = ''




        for site in data['Autofill']:

            chromeautofill_name = site['name']
            chromeautofill_value = site['value']

            data_list.append((name, value))

        num_entries = len(data_list)
        if num_entries > 0:
            report = ArtifactHtmlReport('Chrome Autofill')
            report.start_artifact_report(report_folder, 'Chrome Autofill')
            report.add_script()
            data_headers = ('Field type', 'Typed value')

            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()

            tsvname = f'Chrome Autofill'
            tsv(report_folder, data_headers, data_list, tsvname)

            tlactivity = f'Chrome Autofill'
            timeline(report_folder, tlactivity, data_list, data_headers)
        else:
            logfunc('No Chrome Autofill data available')
          '''
          Todo: support Timestamps:
          
                      "usage_timestamp": [
                        13288051329000000,
                        13319092566000000
            ],

            "usage_timestamp": [13328516295000000],
            
          '''

__artifacts__ = {
        "chromeAutofill": (
            "Google Takeout Archive",
            ('*/Chrome/Autofill.json'),
            get_chromeAutofillInfo)
}

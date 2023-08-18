# Module Description: Parses Google Chrome Autofill value information from Takeout
# Author: @upintheairsheep & @KevinPagano3
# Date: 2023-08-18
# Artifact version: 0.0.1
# Requirements: none

import datetime
import json
import os
import textwrap

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_chromeAutofill(files_found, report_folder, seeker, wrap_text):

    for file_found in files_found:
        file_found = str(file_found)
        if not os.path.basename(file_found) == 'Autofill.json': 
            continue

        with open(file_found, encoding = 'utf-8', mode = 'r') as f:
            data = json.loads(f.read())
        data_list = []

        if 'Autofill' in data:
            for site in data['Autofill']:
                chromeautofill_name = site['name']
                chromeautofill_value = site['value']
                chromeautofill_usage = site['usage_timestamp']
                count = len(chromeautofill_usage)

                for stamp in chromeautofill_usage:
                    timestamp = datetime.datetime.fromtimestamp((int(stamp)/1000000)-11644473600).strftime('%Y-%m-%d %H:%M:%S')
                    data_list.append((timestamp, chromeautofill_name, textwrap.fill(chromeautofill_value, width=100)))

        num_entries = len(data_list)
        if num_entries > 0:
            report = ArtifactHtmlReport('Chrome Autofill')
            report.start_artifact_report(report_folder, 'Chrome Autofill')
            report.add_script()
            data_headers = ('Usage Timestamp','Field Type', 'Typed Value')

            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()

            tsvname = f'Chrome Autofill'
            tsv(report_folder, data_headers, data_list, tsvname)

            tlactivity = f'Chrome Autofill'
            timeline(report_folder, tlactivity, data_list, data_headers)
        else:
            logfunc('No Chrome Autofill data available')

__artifacts__ = {
        "chromeAutofill": (
            "Google Takeout Archive",
            ('*/Chrome/Autofill.json'),
            get_chromeAutofill)
}
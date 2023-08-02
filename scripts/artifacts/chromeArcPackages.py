# Module Description: Parses Google ChromeOS ARCVM ARC information from Takeout's OS Settings
# Author: @upintheairsheep
# Date: 2023-07-14
# Artifact version: 0
# Requirements: none

import datetime
import json
import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_chromeArcPackageInfo(files_found, report_folder, seeker, wrap_text):

    for file_found in files_found:
        file_found = str(file_found)
        if not os.path.basename(file_found) == 'OS Settings.json': # skip -journal and other files
            continue

        with open(file_found, encoding = 'utf-8', mode = 'r') as f:
            data = json.loads(f.read())
        data_list = []

        chromeARC_ver = ''
        chromeARC_lastBack = ''
        chromeARC_name = ''
        chromeARC_bkID = ''





        for site in data['Arc Package']:

            chromeARC_ver = site['package_version']
            chromeARC_lastBack = site['last_backup_time']
            chromeARC_name = site['package_name']
            chromeARC_bkID = site['last_backup_android_id']

            data_list.append((chromeARC_name, chromeARC_ver, chromeARC_lastBack, chromeARC_bkID))

        num_entries = len(data_list)
        if num_entries > 0:
            report = ArtifactHtmlReport('Chrome ARC Packages')
            report.start_artifact_report(report_folder, 'Chrome ARC Packages')
            report.add_script()
            data_headers = ('Package Name','Package Version','Last Time Backed Up','Last Backup Android ID')

            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()

            tsvname = f'Chrome ARC Packages'
            tsv(report_folder, data_headers, data_list, tsvname)

            tlactivity = f'Chrome ARC Packages'
            timeline(report_folder, tlactivity, data_list, data_headers)
        else:
            logfunc('No Chrome ARC Packages data available')

__artifacts__ = {
        "chromeArcPackageInfo": (
            "Google Takeout Archive",
            ('*/Chrome/OS Settings.json'),
            get_chromeArcPackageInfo)
}

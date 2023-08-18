# Module Description: Parses OS Settings from Google Takeout
# Author: @upintheairsheep & @KevinPagano3
# Date: 2023-08-18
# Artifact version: 0.0.1
# Requirements: none

import datetime
import json
import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_chromeOSSettings(files_found, report_folder, seeker, wrap_text):

    for file_found in files_found:
        file_found = str(file_found)
        if not os.path.basename(file_found) == 'OS Settings.json': # skip -journal and other files
            continue

        with open(file_found, encoding = 'utf-8', mode = 'r') as f:
            data = json.loads(f.read())
        data_list = []
        data_list2 = []

        for package in data['Arc Package']:
            chromeARC_lastBack = package['last_backup_time']
            if chromeARC_lastBack == 0:
                chromeARC_lastBack = ''
            else:
                chromeARC_lastBack = datetime.datetime.fromtimestamp(int(chromeARC_lastBack)/1000000).strftime('%Y-%m-%d %H:%M:%S.%f')
            chromeARC_name = package.get('package_name','')
            chromeARC_ver = package.get('package_version','')
            chromeARC_bkID = package.get('last_backup_android_id','')

            data_list.append((chromeARC_lastBack, chromeARC_name, chromeARC_ver, chromeARC_bkID))

        num_entries = len(data_list)
        if num_entries > 0:
            report = ArtifactHtmlReport('Chrome ARC Packages')
            report.start_artifact_report(report_folder, 'Chrome ARC Packages')
            report.add_script()
            data_headers = ('Last Time Backed Up','Package Name','Package Version','Last Backup Android ID')

            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()

            tsvname = f'Chrome ARC Packages'
            tsv(report_folder, data_headers, data_list, tsvname)

            tlactivity = f'Chrome ARC Packages'
            timeline(report_folder, tlactivity, data_list, data_headers)
        else:
            logfunc('No Chrome ARC Packages data available')

        for pref in data['OS Priority Preference']:
            pref_name = pref['preference']['name']
            pref_value = pref['preference']['value']
            preference_value = json.loads(pref_value)
            gender = preference_value['gender']
            if gender == 0:
                gender = 'Female'
            elif gender == 1:
                gender = 'Male'
            elif gender == 2:
                gender = 'Rather not say'
            else:
                gender = 'Other'
            birth_year = preference_value['birth_year']

            data_list2.append((pref_name,gender,birth_year))
            
        num_entries = len(data_list2)
        if num_entries > 0:
            report = ArtifactHtmlReport('Chrome OS Settings')
            report.start_artifact_report(report_folder, 'Chrome OS Settings')
            report.add_script()
            data_headers = ('Preference Name','User Gender','User Birth Year')

            report.write_artifact_data_table(data_headers, data_list2, file_found)
            report.end_artifact_report()

            tsvname = f'Chrome OS Settings'
            tsv(report_folder, data_headers, data_list2, tsvname)

        else:
            logfunc('No Chrome OS Settings data available')

__artifacts__ = {
        "chromeOSSettings": (
            "Google Takeout Archive",
            ('*/Chrome/OS Settings.json'),
            get_chromeOSSettings)
}
# Module Description: Parses Google Chrome Extensions from Takeout
# Author: @KevinPagano3
# Date: 2021-08-20
# Artifact version: 0.0.1
# Requirements: none

import datetime
import json
import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_chromeExtensions(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        if not os.path.basename(file_found) == 'Extensions.json': # skip -journal and other files
            continue

        with open(file_found, encoding = 'utf-8', mode = 'r') as f:
            data = json.loads(f.read())
        data_list = []
        
        ext_name = ''
        ext_version = ''
        ext_ID = ''
        ext_enabled = ''
        incoginito_enabled = ''
        remote_install = ''

        for site in data['Extensions']:
            
            ext_name = site['name']
            ext_version = site['version']
            ext_ID = site['id']
            ext_enabled = site['enabled']
            incoginito_enabled = site['incognito_enabled']
            remote_install = site['remote_install']
               
            data_list.append((ext_name, ext_version, ext_ID, ext_enabled, incoginito_enabled, remote_install))

        num_entries = len(data_list)
        if num_entries > 0:
            report = ArtifactHtmlReport('Chrome Extensions')
            report.start_artifact_report(report_folder, 'Chrome Extensions')
            report.add_script()
            data_headers = ('Name','Version','ID','Enabled','Incognito Enabled','Remote Install')

            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()
            
            tsvname = f'Chrome Extensions'
            tsv(report_folder, data_headers, data_list, tsvname)
            
            tlactivity = f'Chrome Extensions'
            timeline(report_folder, tlactivity, data_list, data_headers)
        else:
            logfunc('No Chrome Extensions data available')

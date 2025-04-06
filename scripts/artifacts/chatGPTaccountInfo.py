# Module Description: Parses ChatGPT user info from a data export from ChatGPT.
# Author: @upintheairsheep
# Date: 2023-07-13
# Artifact version: 1
# Requirements: none

import datetime
import json
import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_chatGPTuser(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        if not os.path.basename(file_found) == 'user.json': # skip -journal and other files
            continue

        with open(file_found, encoding = 'utf-8', mode = 'r') as f:
            data = json.loads(f.read())
        data_list = []
        
        cGPTu_id = ''
        cGPTu_email = ''
        cGPTu_plus = ''
        cGPTu_phoneN = ''

        for site in data:
            cGPTu_id = site['id']
            cGPTu_email = site['email']
            cGPTu_plus = site['chatgpt_plus_user']
            cGPTu_phoneN = site['phone_number']
               
            data_list.append((cGPTu_id, cGPTu_email, cGPTu_plus, cGPTu_phoneN))

        num_entries = len(data_list)
        if num_entries > 0:
            report = ArtifactHtmlReport('ChatGPT User Information')
            report.start_artifact_report(report_folder, 'ChatGPT User Information')
            report.add_script()
            data_headers = ('User ID','User Email Adress','Does this user use ChatGPT Plus?','User Phone Number')

            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()
            
            tsvname = f'ChatGPT User Information'
            tsv(report_folder, data_headers, data_list, tsvname)
            
            tlactivity = f'ChatGPT User Information'
            timeline(report_folder, tlactivity, data_list, data_headers)
        else:
            logfunc('No ChatGPT User information availble')

__artifacts__ = {
        "chatGPTuser": (
            "ChatGPT Data Export Archive",
            ('*/user.json'),
            get_chatGPTuser)
}

# Module Description: Parses Google profile information from Takeout
# Author: @KevinPagano3
# Date: 2021-08-23
# Artifact version: 0.0.2
# Requirements: none

import datetime
import json
import os
import shutil

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html

def get_googleProfile(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        if not os.path.basename(file_found) == 'Profile.json': # skip -journal and other files
            continue

        with open(file_found, encoding = 'utf-8', mode = 'r') as f:
            data = json.loads(f.read())
        data_list = []
        emails = []
        addresses = ''
        gender=''
        formattedName = data['name'].get('formattedName','')
        displayName = data.get('displayName')
        birthday = data.get('birthday')
        _gender = data.get('gender')
        if (_gender):
            gender = _gender.get('type','')

        if (len(emails)>0):
            for x in data['emails']:
                emails.append((x['value']))

            for y in emails:
                addresses += str(y) + "; "
            addresses = addresses[:-2]
        
    thumb = ''
    ProfilePhoto = 'ProfilePhoto.jpg'
            
    for match in files_found:
        if ProfilePhoto in match:
            shutil.copy2(match, report_folder)
            thumb = media_to_html(match, files_found, report_folder)
            #thumb = f'<img src="{report_folder}/{ProfilePhoto}" width="300"></img>'
    
    data_list.append((formattedName, displayName, addresses, birthday, gender, thumb))

    num_entries = len(data_list)
    if num_entries > 0:
        report = ArtifactHtmlReport('Google Profile')
        report.start_artifact_report(report_folder, 'Google Profile')
        report.add_script()
        data_headers = ('Name','Display Name','Email Address(s)','Birthday','Gender','Profile Pic')

        report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Profile Pic'])
        report.end_artifact_report()
        
        tsvname = f'Google Profile'
        tsv(report_folder, data_headers, data_list, tsvname)
        
        tlactivity = f'Google Profile'
        timeline(report_folder, tlactivity, data_list, data_headers)
    else:
        logfunc('No Google Profile data available')
 
__artifacts__ = {
        "googleProfile": (
            "Google Takeout Archive",
            (('*/Profile/Profile.json','*/Profile/ProfilePhoto.jpg')),
            get_googleProfile)
}

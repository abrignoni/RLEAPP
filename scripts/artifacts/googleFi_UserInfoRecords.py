# Module Description: Parses Google Fi user info records from Takeout
# Author: @KevinPagano3
# Date: 2022-02-28
# Artifact version: 0.0.1
# Requirements: none

import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_googleFi_UserInfoRecords(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        if not os.path.basename(file_found) == 'GoogleFi.UserInfo.Records.txt': # skip -journal and other files
            continue

        with open(file_found, encoding = 'utf-8', mode = 'r') as f:
            data = f.readlines()[1:]
            
        data_list = []
        
        for line in data:
            entry = line.split('\t')
            
            user_phone = entry[0]
            usage_type = entry[1].replace('USAGE_TYPE_','').title()
            start_ts = entry[2].replace(' UTC','')
            end_ts = entry[3].replace(' UTC','')
            direction = entry[4].replace('DIRECTION_','').title()
            duration = entry[5].replace('Duration:','')
            user_country = entry[6]
            remote_country = entry[7]
            remote_phone = entry[8]
            equipment_id = entry[9]
            carrier = entry[10]
            network_carrier = entry[11]
            network_carrier_start_ts = entry[12].replace(' UTC','')
            is_wifi = entry[13].title()
            is_hosted_voice = entry[14].title()
            is_hangouts = entry[15].title()
            is_voicemail = entry[16].strip().title()

            data_list.append((start_ts,end_ts,user_phone,usage_type,direction,duration,remote_phone,equipment_id,carrier,network_carrier,network_carrier_start_ts,is_wifi,is_hosted_voice,is_hangouts,is_voicemail))

        num_entries = len(data_list)
        if num_entries > 0:
            report = ArtifactHtmlReport('Google Fi - User Info Records')
            report.start_artifact_report(report_folder, 'Google Fi - User Info Records')
            report.add_script()
            data_headers = ('Start Timestamp','End Timestamp','User Phone Number','Usage Type','Direction','Duration (Minutes)','Remote Phone Number','Equipment ID','Carrier','Network Carrier','Network Carrier Start Timestamp','Is Wifi?','Is Hosted Voice?','Is Hangouts?','Is Voicemail?')

            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()
            
            tsvname = f'Google Fi - User Info Records'
            tsv(report_folder, data_headers, data_list, tsvname)
            
            tlactivity = f'Google Fi - User Info Records'
            timeline(report_folder, tlactivity, data_list, data_headers)
        else:
            logfunc('No Google Fi - User Info Records data available')

__artifacts__ = {
        "googleFi_UserInfoRecords": (
            "Google Takeout Archive",
            ('*/Google Fi/User Info*/GoogleFi.UserInfo.Records.txt'),
            get_googleFi_UserInfoRecords)
}
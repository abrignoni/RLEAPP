# Module Description: Parses Fitbit details from Google Takeout
# Author: @KevinPagano3
# Date: 2023-09-08
# Artifact version: 0.0.1
# Requirements: none

import os
import datetime
import csv

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, ipgen

def get_fitbit(files_found, report_folder, seeker, wrap_text):

    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        #SLEEP PROFILE
        if filename.startswith('Sleep Profile.csv'):
            data_list = []
            
            description = 'Sleep profiles for a Fitbit account'
            report = ArtifactHtmlReport('Fitbit Sleep Profile')
            report.start_artifact_report(report_folder, 'Fitbit Sleep Profile', description)
            html_report = report.get_report_file_path()
            report.add_script()
            has_header = True
            
            with open(file_found, 'r', encoding='utf-8') as f:
                delimited = csv.reader(f, delimiter=',')
                next(delimited)
                for item in delimited:
                    if len(item) > 2:
                        create_date = item[0]
                        sleep_type = item[1]
                        deep_sleep = item[2]
                        rem_sleep = item[3]
                        sleep_duration = item[4]
                        sleep_start = item[5]
                        schedule_var = item[6]
                        restore_sleep = item[7]
                        time_before_sound_sleep = item[8]
                        sleep_stability = item[9]
                        long_awakening = item[10]
                        naps = item[11]
                    
                        data_list.append((create_date,sleep_type,deep_sleep,rem_sleep,sleep_duration,sleep_start,schedule_var,restore_sleep,time_before_sound_sleep,sleep_stability,long_awakening,naps))
                        
                    else:
                        create_date = item[0]
                        sleep_type = item[1]
                        
                        data_list.append((create_date,sleep_type,'','','','','','','','','',''))
                
            if len(data_list) > 0:
                data_headers = ('Created Date','Sleep Type','Deep Sleep (Minutes)','REM Sleep (%)','Sleep Duration (Hours)','Sleep Start Time ()','Schedule Variability (Minutes)','Restorative Sleep (%)','Time Before Sound Sleep (Minutes)','Sleep Stability (Events/Hr)','Nights w/ Long Awakenings (%)','Days w/ Naps')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Fitbit Sleep Profile'
                tsv(report_folder, data_headers, data_list, tsvname)

                tlactivity = f'Fitbit Sleep Profile'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Fitbit Sleep Profile data available')
                
        #SLEEP SCORES      
        if filename.startswith('sleep_score.csv'):
            data_list = []
            
            description = 'Sleep scores for a Fitbit account'
            report = ArtifactHtmlReport('Fitbit Sleep Scores')
            report.start_artifact_report(report_folder, 'Fitbit Sleep Scores', description)
            html_report = report.get_report_file_path()
            report.add_script()
            has_header = True
            
            with open(file_found, 'r', encoding='utf-8') as f:
                delimited = csv.reader(f, delimiter=',')
                next(delimited)
                for item in delimited:
                    entry_id = item[0]
                    timestamp = item[1]
                    timestamp = timestamp.replace('T',' ').replace('Z','')
                    overall_score = item[2]
                    composition_score = item[3]
                    revitalization_score = item[4]
                    duration_score = item[5]
                    deep_sleep = item[6]
                    resting_hr = item[7]
                    restlessness = round(float(item[8])*100,2)

                    data_list.append((timestamp,entry_id,overall_score,composition_score,revitalization_score,duration_score,deep_sleep,resting_hr,restlessness))

            if len(data_list) > 0:
                data_headers = ('End Timestamp','Entry ID','Overall Score','Deep & REM Score','Restoration Score','Time Asleep Score','Deep Sleep (Minutes)','Resting Heart Rate','Restlessness (%)')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Fitbit Sleep Scores'
                tsv(report_folder, data_headers, data_list, tsvname)

                tlactivity = f'Fitbit Sleep Scores'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Fitbit Sleep Scores data available')
        
        #STRESS SCORES
        if filename.startswith('Stress Score.csv'):
            data_list = []
            
            description = 'Stress scores for a Fitbit account'
            report = ArtifactHtmlReport('Fitbit Stress Scores')
            report.start_artifact_report(report_folder, 'Fitbit Stress Scores', description)
            html_report = report.get_report_file_path()
            report.add_script()
            has_header = True
            
            with open(file_found, 'r', encoding='utf-8') as f:
                delimited = csv.reader(f, delimiter=',')
                next(delimited)
                for item in delimited:
                    date_created = item[0].replace('T',' ')
                    date_updated = item[1].replace('T',' ')
                    stress_score = item[2]
                    sleep_points = item[3]
                    max_sleep_points = item[4]
                    responsiveness_points = item[5]
                    max_responsiveness_points = item[6]
                    exertion_points = item[7]
                    max_exertion_points = item[8]
                    status = item[9]
                    calculation_failed = item[10]

                    data_list.append((date_created,date_updated,stress_score,sleep_points,responsiveness_points,exertion_points,status,calculation_failed))

            if len(data_list) > 0:
                data_headers = ('Created Timestamp','Updated Timestamp','Stress Score','Sleep Points (n/30)','Responsiveness Points (n/30)','Exertion Points (n/40)','Status','Calculation Failed')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Fitbit Stress Scores'
                tsv(report_folder, data_headers, data_list, tsvname)

                tlactivity = f'Fitbit Stress Scores'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Fitbit Stress Scores data available')
                
        #FITBIT PROFILE
        if filename.startswith('Profile.csv'):
            data_list = []
            
            description = 'Profile details for a Fitbit account'
            report = ArtifactHtmlReport('Fitbit Account Profile')
            report.start_artifact_report(report_folder, 'Fitbit Account Profile', description)
            html_report = report.get_report_file_path()
            report.add_script()
            has_header = True
            
            with open(file_found, 'r', encoding='utf-8') as f:
                delimited = csv.reader(f, delimiter=',')
                next(delimited)
                for item in delimited:
                    user_id = item[0]
                    full_name = item[1]
                    first_name = item[2]
                    last_name = item[3]
                    display_name = item[5]
                    username = item[6]
                    email_address = item[7]
                    date_of_birth = item[8]
                    child = item[9]
                    country = item[10]
                    state = item[11]
                    city = item[12]
                    timezone = item[13]
                    member_since = item[15]
                    about_me = item[16]
                    gender = item[20]
                    height = item[21]
                    weight = item[22]
                    stride_length_walking = item[23]
                    stride_length_running = item[24]

                    data_list.append((user_id,full_name,display_name,username,email_address,date_of_birth,child,country,state,city,timezone,member_since,about_me,gender,height,weight,stride_length_walking,stride_length_running))

            if len(data_list) > 0:
                data_headers = ('User ID','Full Name','Display Name','Username','Email Address','Date of Birth','Is Child','Country','State','City','Timezone','Member Since','About Me','Gender','Height (cm)','Weight (kg)','Strike Length (Walking)','Stride Length (Running)')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Fitbit Account Profile'
                tsv(report_folder, data_headers, data_list, tsvname)

            else:
                logfunc('No Fitbit Account Profile data available')
                
        
        #FITBIT TRACKERS
        if filename.startswith('Trackers.csv'):
            data_list = []
            
            description = 'Trackers for a Fitbit account'
            report = ArtifactHtmlReport('Fitbit Trackers')
            report.start_artifact_report(report_folder, 'Fitbit Trackers', description)
            html_report = report.get_report_file_path()
            report.add_script()
            has_header = True
            
            with open(file_found, 'r', encoding='utf-8') as f:
                delimited = csv.reader(f, delimiter=',')
                next(delimited)
                for item in delimited:
                    tracker_id = item[0]
                    date_added = item[1]
                    last_sync = item[2].replace('T',' ').replace('Z','')
                    battery_level = item[3]
                    tracker_name = item[12]
                    device_name = item[13]
                    dominant_hand = item[14]
                    alarm_update = item[20].replace('T',' ').replace('Z','')
                    heart_rate_update = item[23].replace('T',' ').replace('Z','')

                    data_list.append((last_sync,device_name,tracker_name,tracker_id,battery_level,heart_rate_update,alarm_update,dominant_hand))

            if len(data_list) > 0:
                data_headers = ('Last Synced Timestamp','Device Name','Tracker Name','Tracker ID','Battery Level','Heart Rate Update Timestamp','Alarm Update Timestamp','On Dominant Hand')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Fitbit Trackers'
                tsv(report_folder, data_headers, data_list, tsvname)

                tlactivity = f'Fitbit Trackers'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Fitbit Trackers data available')
                
        #FITBIT OXYGEN SATURATION
        if filename.startswith('Daily Sp02 - '):
            data_list = []
            
            description = 'Trackers for a Fitbit account'
            report = ArtifactHtmlReport('Fitbit Trackers')
            report.start_artifact_report(report_folder, 'Fitbit Trackers', description)
            html_report = report.get_report_file_path()
            report.add_script()
            has_header = True
            
            with open(file_found, 'r', encoding='utf-8') as f:
                delimited = csv.reader(f, delimiter=',')
                next(delimited)
                for item in delimited:
                    tracker_id = item[0]
                    date_added = item[1]
                    last_sync = item[2].replace('T',' ').replace('Z','')
                    battery_level = item[3]
                    tracker_name = item[12]
                    device_name = item[13]
                    dominant_hand = item[14]
                    alarm_update = item[20].replace('T',' ').replace('Z','')
                    heart_rate_update = item[23].replace('T',' ').replace('Z','')

                    data_list.append((last_sync,device_name,tracker_name,tracker_id,battery_level,heart_rate_update,alarm_update,dominant_hand))

            if len(data_list) > 0:
                data_headers = ('Last Synced Timestamp','Device Name','Tracker Name','Tracker ID','Battery Level','Heart Rate Update Timestamp','Alarm Update Timestamp','On Dominant Hand')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Fitbit Trackers'
                tsv(report_folder, data_headers, data_list, tsvname)

                tlactivity = f'Fitbit Trackers'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Fitbit Trackers data available')

__artifacts__ = {
        "fitbit": (
            "Google Takeout Archive",
            ('*/Fitbit/Sleep/Sleep Profile.csv','*/Fitbit/Sleep Score/sleep_score.csv','*/Fitbit/Stress Score/Stress Score.csv','*/Fitbit/Your Profile/Profile.csv','*/Fitbit/Paired Devices/Trackers.csv','*/Fitbit/Oxygen Saturation (SpO2)/Daily Sp02 - *.csv'),
            get_fitbit)
}
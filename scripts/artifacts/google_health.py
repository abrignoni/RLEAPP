__artifacts_v2__ = {
    "fitbit_sleep_profile": {
        "name": "Google Health (Fitbit) - Sleep Profile",
        "description": "Sleep profiles for a Fitbit account",
        "author": "@stark4n6",
        "creation_date": "2023-09-14",
        "last_update_date": "2026-06-19",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": "*/Sleep/Sleep Profile.csv",
        "output_types": "standard",
        "artifact_icon": "moon",
    },
    "fitbit_sleep_score": {
        "name": "Google Health (Fitbit) - Sleep Scores",
        "description": "Sleep scores for a Fitbit account",
        "author": "@stark4n6",
        "creation_date": "2023-09-14",
        "last_update_date": "2026-06-19",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": "*/Sleep Score/sleep_score.csv",
        "output_types": "standard",
        "artifact_icon": "moon",
    },
    "fitbit_stress_score": {
        "name": "Google Health (Fitbit) - Stress Scores",
        "description": "Stress scores for a Fitbit account",
        "author": "@stark4n6",
        "creation_date": "2023-09-14",
        "last_update_date": "2026-06-19",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": "*/Stress Score/Stress Score.csv",
        "output_types": "standard",
        "artifact_icon": "meh",
    },
    "fitbit_profile": {
        "name": "Google Health (Fitbit) - Account Profile",
        "description": "Profile details for a Fitbit account",
        "author": "@stark4n6",
        "creation_date": "2023-09-14",
        "last_update_date": "2026-06-19",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": "*/Your Profile/Profile.csv",
        "output_types": ["html","tsv","lava"],
        "artifact_icon": "user",
    },
    "fitbit_trackers": {
        "name": "Google Health (Fitbit) - Trackers",
        "description": "Trackers for a Fitbit account",
        "author": "@stark4n6",
        "creation_date": "2023-09-14",
        "last_update_date": "2026-06-19",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": "*/Paired Devices/Trackers.csv",
        "output_types": "standard",
        "artifact_icon": "watch",
    },
    "fitbit_goals": {
        "name": "Google Health (Fitbit) - Activity Goals",
        "description": "Activity goals for a Fitbit account",
        "author": "@stark4n6",
        "creation_date": "2023-09-14",
        "last_update_date": "2026-06-19",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": "*/Activity Goals/Activity Goals.csv",
        "output_types": "standard",
        "artifact_icon": "award",
    },
    "fitbit_oxygen": {
        "name": "Google Health (Fitbit) - Oxygen Saturation (SpO2)",
        "description": "Parses oxygen saturation from a Fitbit account",
        "author": "@stark4n6",
        "creation_date": "2023-09-14",
        "last_update_date": "2026-06-19",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": "*/Oxygen Saturation (SpO2)/Daily SpO2 - *.csv",
        "output_types": "standard",
        "artifact_icon": "wind",
    },
    "fitbit_comp_temp": {
        "name": "Google Health (Fitbit) - Computed Temperature",
        "description": "Parses computed temperatures for a Fitbit account",
        "author": "@stark4n6",
        "creation_date": "2023-09-14",
        "last_update_date": "2026-06-19",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": "*/Temperature/Computed Temperature - *.csv",
        "output_types": "standard",
        "artifact_icon": "thermometer",
    },
}

import csv
import os
from scripts.ilapfuncs import artifact_processor, get_file_path

@artifact_processor
def fitbit_sleep_profile(files_found, report_folder, seeker, wrap_text):
    data_list = []
    file_found = get_file_path(files_found, 'Sleep Profile.csv')

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
                
    data_headers = ('Created Date','Sleep Type','Deep Sleep (Minutes)','REM Sleep (%)','Sleep Duration (Hours)','Sleep Start Time ()','Schedule Variability (Minutes)','Restorative Sleep (%)','Time Before Sound Sleep (Minutes)','Sleep Stability (Events/Hr)','Nights w/ Long Awakenings (%)','Days w/ Naps')
    
    return data_headers, data_list, file_found

@artifact_processor
def fitbit_sleep_score(files_found, report_folder, seeker, wrap_text):             
    data_list = []
    file_found = get_file_path(files_found, 'sleep_score.csv') 
        
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
    
    data_headers = ('End Timestamp','Entry ID','Overall Score','Deep & REM Score','Restoration Score','Time Asleep Score','Deep Sleep (Minutes)','Resting Heart Rate','Restlessness (%)')
        
    return data_headers, data_list, file_found
    
@artifact_processor
def fitbit_stress_score(files_found, report_folder, seeker, wrap_text):             
    data_list = []
    file_found = get_file_path(files_found, 'Stress Score.csv')    

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

    data_headers = (('Created Timestamp','datetime'),('Updated Timestamp','datetime'),'Stress Score','Sleep Points (n/30)','Responsiveness Points (n/30)','Exertion Points (n/40)','Status','Calculation Failed')
    
    return data_headers, data_list, file_found

@artifact_processor
def fitbit_profile(files_found, report_folder, seeker, wrap_text):             
    data_list = []
    file_found = get_file_path(files_found, 'Profile.csv')    

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

    data_headers = ('User ID','Full Name','Display Name','Username','Email Address','Date of Birth','Is Child','Country','State','City','Timezone','Member Since','About Me','Gender','Height (cm)','Weight (kg)','Strike Length (Walking)','Stride Length (Running)')
    
    return data_headers, data_list, file_found
    
@artifact_processor
def fitbit_trackers(files_found, report_folder, seeker, wrap_text):             
    data_list = []
    file_found = get_file_path(files_found, 'Trackers.csv')
    
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
            dominant_hand = str(item[14]).title()
            alarm_update = item[20].replace('T',' ').replace('Z','')
            heart_rate_update = item[23].replace('T',' ').replace('Z','')

            data_list.append((last_sync,device_name,tracker_name,tracker_id,battery_level,heart_rate_update,alarm_update,dominant_hand))

    data_headers = (('Last Synced Timestamp','datetime'),'Device Name','Tracker Name','Tracker ID','Battery Level',('Heart Rate Update Timestamp','datetime'),('Alarm Update Timestamp','datetime'),'On Dominant Hand')
    
    return data_headers, data_list, file_found
    
@artifact_processor
def fitbit_goals(files_found, report_folder, seeker, wrap_text):             
    data_list = []
    file_found = get_file_path(files_found, 'Activity Goals.csv')
    
    has_header = True
    
    with open(file_found, 'r', encoding='utf-8') as f:
        delimited = csv.reader(f, delimiter=',')
        next(delimited)
        for item in delimited:
            goal_type = item[0]
            goal_frequency = item[1]
            goal_target = item[2]
            goal_result = item[3]
            goal_status = item[4]
            goal_primary = item[5]
            goal_start = item[6]
            goal_end = item[7]
            goal_created = item[8].replace('T',' ')
            goal_edited = item[9]

            data_list.append((goal_created,goal_start,goal_end,goal_type,goal_frequency,goal_target,goal_result,goal_status,goal_primary))
    
    data_headers = (('Created Timestamp','datetime'),'Start Date','End Date','Type','Frequency','Target','Result','Status','Is Primary')
        
    return data_headers, data_list, file_found
    
@artifact_processor
def fitbit_oxygen(files_found, report_folder, seeker, wrap_text):             
    data_list = []
    
    for file_found in files_found:
        file_found = str(file_found)
        filename = os.path.basename(file_found)
        source_file = os.path.dirname(file_found) + '\\Daily SpO2 - *.csv'
            
        has_header = True
        
        with open(file_found, 'r', encoding='utf-8') as f:
            delimited = csv.reader(f, delimiter=',')
            next(delimited)
            for item in delimited:
                timestamp = item[0].replace('T',' ').replace('Z','')
                average_value = item[1]
                lower_bound = item[2]
                upper_bound = item[3]
                
                data_list.append((timestamp,average_value,lower_bound,upper_bound,filename))
                
    data_headers = (('Timestamp','datetime'),'Average Value','Lower Bound','Upper Bound','Source File')
    return data_headers, data_list, "See source file column"
    
@artifact_processor
def fitbit_comp_temp(files_found, report_folder, seeker, wrap_text):             
    data_list = []
    
    for file_found in files_found:
        file_found = str(file_found)
        filename = os.path.basename(file_found)
        source_file = os.path.dirname(file_found) + '\\Computed Temperature - *.csv'
        
        with open(file_found, 'r', encoding='utf-8') as f:
            delimited = csv.reader(f, delimiter=',')
            next(delimited)
            for item in delimited:
                comp_type = item[0]
                sleep_start = item[1].replace('T',' ')
                sleep_end = item[2].replace('T',' ')
                temp_samples = item[3]
                nightly_temp = item[4]
                base_rel_sample_sum = item[5]
                base_rel_sample_sum_square = item[6]
                base_rel_nightly_stand_dev = item[7]
                base_rel_sample_stand_dev = item[8]
                
                data_list.append((sleep_start,sleep_end,comp_type,temp_samples,nightly_temp,base_rel_sample_sum,base_rel_sample_sum_square,base_rel_nightly_stand_dev,base_rel_sample_stand_dev,filename))
                
    data_headers = (('Sleep Start Timestamp','datetime'),('Sleep End Timestamp','datetime'),'Type','Temperature Sample Count','Nightly Temperature (C)','Baseline Relative Sample Sum','Baseline Relative Sample (Sum of Squares)','Baseline Relative Nightly Standard Deviation','Baseline Relative Sample Standard Deviation','Source File')
    return data_headers, data_list, "See source file column"
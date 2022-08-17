# Module Description: Parses Google Takeout Location History.json file
# Author: @KevinPagano3 & @Cheeky4n6Monkey
# Date: 2021-09-21
# Artifact version: 0.0.2
# Requirements: none
# Updated: 2022-02-28
# Code completely reworked from https://github.com/cheeky4n6monkey/4n6-scripts/blob/master/Google_Takeout_Location_History/%23%20gLocationHistoryActivity.py
# License: https://www.gnu.org/licenses/gpl-3.0.en.html

import datetime
import json
import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, kmlgen

def get_takeoutLocationHistory(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        if not os.path.basename(file_found) == 'Location History.json': # skip -journal and other files
            continue

        data_list = []
        count_element = 0
        count_element_activity = 0
        count_sub_total = 0
        count_multiple_activitys = 0
        folder_dict = {}

        with open(file_found, 'r') as f:
            data = json.loads(f.read())

        for element in data["locations"]:
            count_element += 1
            #print(element["timestampMs"]) # parent element timestamp
            element_timestamp = element["timestampMs"]
            element_timestamp_str = datetime.datetime.utcfromtimestamp(int(element_timestamp)/1000).isoformat()
            element_lat = float(element["latitudeE7"]/10000000)
            element_llg = float(element["longitudeE7"]/10000000)
            element_accuracy = element["accuracy"]

            element_alt = "NOT_SPECIFIED"
            if "altitude" in element: # altitude not always specified
                element_alt = float(element["altitude"])

            element_verticalaccuracy = "NOT_SPECIFIED"
            if "verticalAccuracy" in element: # verticalAccuracy not always specified
                element_verticalaccuracy = element["verticalAccuracy"]

            element_heading = "NOT_SPECIFIED"
            if "heading" in element: # heading not always specified
                element_heading = element["heading"]

            element_velocity = "NOT_SPECIFIED"
            if "velocity" in element: # velocity not always specified
                element_velocity = element["velocity"]

            element_source = element["source"]
            element_device = str(element["deviceTag"])

            element_platform = "NOT_SPECIFIED"
            if "platformType" in element: # platformType not always specified
                element_platform = element["platformType"]

            if "activity" in element: # parent activity list
                count_element_activity += 1

                if (len(element["activity"]) > 1):
                    count_multiple_activitys += 1 

                # Each element activity has at least one child activity which is represented as a list of type/confidence dicts
                count_child = 0
                for activity in element["activity"]:
                    count_child += 1

                    activity_timestamp = activity["timestampMs"]
                    activity_timestamp_str = datetime.datetime.utcfromtimestamp(int(activity_timestamp)/1000).isoformat()

                    # Each (sub)activity can have multiple types:
                    # IN_VEHICLE	The device is in a vehicle, such as a car.
                    # ON_BICYCLE	The device is on a bicycle.
                    # ON_FOOT	The device is on a user who is walking or running.
                    # RUNNING	The device is on a user who is running.
                    # STILL	The device is still (not moving).
                    # TILTING	The device angle relative to gravity changed significantly.
                    # UNKNOWN	Unable to detect the current activity.
                    # WALKING	The device is on a user who is walking.
                    #
                    # confidence    value from 0 to 100 indicating how likely it is that the user is performing this activity.
                    #
                    # Source: https://developers.google.com/android/reference/com/google/android/gms/location/DetectedActivity
                    count_sub = 0
                    subactivity_str = ""
                    for subact in activity["activity"]:
                        count_sub += 1
                        subactivity_str += str(subact["type"] + " [" + str(subact["confidence"]) + "], ")

                    # Store each activity & its subactivitys    
                    folderid = element_timestamp_str.split("T")[0] # eg 2022-02-04T09:56:36.253Z
                    element_timestamp_c = element_timestamp_str.replace('T', ' ')
                    element_timestamp_c = element_timestamp_c.replace('Z', '')
                    
                    if folderid not in folder_dict.keys(): # add entry 1 if key has not been created before
                        folder_dict[folderid] = [(element_timestamp_c, element_source, element_device, element_platform,  element_lat, element_llg, element_alt, element_heading, element_velocity, element_accuracy, element_verticalaccuracy, count_sub, activity_timestamp, activity_timestamp_str, subactivity_str[:-2])]
                    else:
                        # add n-th entry to existing folder
                        folder_dict[folderid].append((element_timestamp_c, element_source, element_device, element_platform, element_lat, element_llg, element_alt, element_heading, element_velocity, element_accuracy, element_verticalaccuracy, count_sub, activity_timestamp, activity_timestamp_str, subactivity_str[:-2]))
                count_sub_total += count_sub
                     
        for x, y in folder_dict.items():
            for a in y:
                data_list.append(a)                           

    num_entries = len(data_list)
    if num_entries > 0:
        report = ArtifactHtmlReport('Google Location History - Location History')
        report.start_artifact_report(report_folder, 'Google Location History - Location History')
        report.add_script()
        data_headers = ('Timestamp','Source','Device Tag','Platform','Latitude','Longitude','Altitude','Heading (Degrees)','Velocity','Accuracy','Vertical Accuracy','Activity','Sub-activity Types', 'Timestamp Activity', 'Detected Activity')

        report.write_artifact_data_table(data_headers, data_list, file_found)
        report.end_artifact_report()
        
        tsvname = f'Google Location History - Location History'
        tsv(report_folder, data_headers, data_list, tsvname)
        
        tlactivity = f'Google Location History - Location History'
        timeline(report_folder, tlactivity, data_list, data_headers)
        
        kmlactivity = 'Google Location History - Location History'
        kmlgen(report_folder, kmlactivity, data_list, data_headers)            
        
    else:
        logfunc('No Google Location History - Location History data available')

__artifacts__ = {
        "takeoutLocationHistory": (
            "Google Takeout Archive",
            ('*/Location History/Location History.json'),
            get_takeoutLocationHistory)
}
# Code edited from https://github.com/cheeky4n6monkey/4n6-scripts/blob/master/Google_Takeout_Records/gRecordsActivity_ijson_date.py
#
# Author: cheeky4n6monkey@gmail.com
# License: https://www.gnu.org/licenses/gpl-3.0.en.html


import datetime
import ijson
import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, kmlgen

def get_gooReturnsrec(files_found, report_folder, seeker, wrap_text, time_offset):
    
    for file_found in files_found:
        file_found = str(file_found)
        if not os.path.basename(file_found) == 'Records.json': # skip -journal and other files
            continue

        data_list = []
        count_element = 0
        count_element_activity = 0
        count_multiple_activitys = 0
        folder_dict = {} 
    
        with open(file_found, 'r') as f:
            document = f.read()
            
        element_items = ijson.items(document, 'locations.item')
    
        for element in element_items: # each element
            #print("\n" + str(element))
            count_element += 1
    
            if 'activity' in element: # each element which has an activty
                count_element_activity += 1
    
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
                if "platformType" in element: # altitude not always specified
                    element_platform = element["platformType"]
    
                element_formFactor = "NOT_SPECIFIED"
                if "formFactor" in element: # formFactor not always specified
                    element_formFactor = element["formFactor"]
    
                element_timestamp_str = element["timestamp"]
    
                element_serverTimestamp_str = "NOT_SPECIFIED"
                if "serverTimestamp" in element: # serverTimestamp not always specified
                    element_serverTimestamp_str = element["serverTimestamp"]      
    
                element_deviceTimestamp_str = "NOT_SPECIFIED"
                if "deviceTimestamp" in element: # deviceTimestamp not always specified 
                    element_deviceTimestamp_str = element["deviceTimestamp"]

                if (len(element["activity"]) > 1):
                    count_multiple_activitys += 1
                    
                count_activity = 0
                for act in element["activity"]: # for each activity in element. multiple (sub)activitys can be in 1 element.
                    count_activity += 1                    
                    activity_timestamp_str = "Not found"
                    if "timestamp" in act: # search for Activity Timestamp
                        activity_timestamp_str = act["timestamp"]
    
                    # For each sub-activity listed, there can be multiple type/confidence pairs
                    # (sub)activity type can be:
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
                    for subact in act["activity"]:
                        count_sub += 1
                        #print("subactivity no. = " + str(count_sub))
                        #print("type: " + subact["type"])
                        #print("conf: " + str(subact["confidence"]))
                        subactivity_str += str(subact["type"] + " [" + str(subact["confidence"]) + "], ")
                    
    
                    # Store each activity & its subactivitys    
                    folderid = element_timestamp_str.split("T")[0] # eg 2022-02-04T09:56:36.253Z
                    element_timestamp_c = element_timestamp_str.replace('T', ' ')
                    element_timestamp_c = element_timestamp_c.replace('Z', '')
                    
                    if folderid not in folder_dict.keys(): # add entry 1 if key has not been created before
                        folder_dict[folderid] = [(element_timestamp_c, element_source, element_device, element_platform, element_formFactor, element_serverTimestamp_str, element_deviceTimestamp_str, element_timestamp_str, element_lat, element_llg, element_alt, element_heading, element_velocity, element_accuracy, element_verticalaccuracy, count_sub, activity_timestamp_str, subactivity_str[:-2])]
                    else:
                        # add n-th entry to existing folder
                        folder_dict[folderid].append((element_timestamp_c, element_source, element_device, element_platform, element_formFactor, element_serverTimestamp_str, element_deviceTimestamp_str, element_timestamp_str, element_lat, element_llg, element_alt, element_heading, element_velocity, element_accuracy, element_verticalaccuracy, count_sub, activity_timestamp_str, subactivity_str[:-2]))
                        
                # end for activity in element loop
        # ends for element loop
    
        for x, y in folder_dict.items():
            for a in y:
                data_list.append(a)
                
        
    num_entries = len(data_list)
    if num_entries > 0:
        report = ArtifactHtmlReport('Google Location History - Records')
        report.start_artifact_report(report_folder, 'Google Location History - Records')
        report.add_script()
        data_headers = ('Timestamp', 'Source', 'Device', 'Platform', 'Form Factor', 'Timestamp Server', 'Timestamp Device', 'Timestamp Element', 'Latitude', 'Longitude', 'Altitude', 'Heading', 'Velocity', 'Accuracy', 'Vertical Accuracy', 'Sub-activity Types', 'Timestamp Activity', 'Detected Activity')

        report.write_artifact_data_table(data_headers, data_list, file_found)
        report.end_artifact_report()
        
        tsvname = f'Google Location History - Records'
        tsv(report_folder, data_headers, data_list, tsvname)
        
        tlactivity = f'Google Location History - Records'
        timeline(report_folder, tlactivity, data_list, data_headers)
        
        kmlactivity = 'Google Location History - Records'
        kmlgen(report_folder, kmlactivity, data_list, data_headers)
        
    else:
        logfunc('No Google Location History - Records data available')
            
__artifacts__ = {
        "gooReturnsrec": (
            "Google Returns",
            ('*/Location History/Records.json'),
            get_gooReturnsrec)
}
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

        #with open(file_found, encoding = 'utf-8', mode = 'r') as f:
        with open(file_found, "r") as f:
            data = json.loads(f.read())
        data_list = []

        for x in data['locations']:
    
            timestampMs = x.get('timestampMs','')
            timestamp_formatted = datetime.datetime.utcfromtimestamp(int(timestampMs)/1000).strftime('%Y-%m-%d %H:%M:%S')
            latitude = int(x.get('latitudeE7',''))/10000000
            longitude = int(x.get('longitudeE7',''))/10000000
            accuracy = x.get('accuracy','')
            velocity = x.get('velocity','')
            heading = x.get('heading','')
            altitude = x.get('altitude','')
            verticalAccuracy = x.get('verticalAccuracy','')        
            source = x.get('source','')
            deviceTag = x.get('deviceTag','')
            activity = x.get('activity','')
        
            data_list.append((timestamp_formatted,latitude,longitude,accuracy,velocity,heading,altitude,verticalAccuracy,source,deviceTag,activity))

        num_entries = len(data_list)
        if num_entries > 0:
            report = ArtifactHtmlReport('Google Takeout Location History')
            report.start_artifact_report(report_folder, 'Google Takeout Location History')
            report.add_script()
            data_headers = ('Timestamp','Latitude','Longitude','Accuracy','Velocity','Heading (Degrees)','Altitude','Vertical Accuracy','Source','Device Tag','Activity')

            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()
            
            tsvname = f'Google Takeout Location History'
            tsv(report_folder, data_headers, data_list, tsvname)
            
            tlactivity = f'Google Takeout Location History'
            timeline(report_folder, tlactivity, data_list, data_headers)
            
            kmlactivity = 'Google Takeout Location History'
            kmlgen(report_folder, kmlactivity, data_list, data_headers)            
            
        else:
            logfunc('No Google Takeout Location History data available')

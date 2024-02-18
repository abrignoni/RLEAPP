# Module Description: Parses Google Takeout Semantic Location History .json files
# Author: @KevinPagano3
# Date: 2022-09-15
# Artifact version: 0.0.1

import datetime
import json
import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, kmlgen

def get_takeoutSemanticLocationHistory(files_found, report_folder, seeker, wrap_text, time_offset):
    
    data_list_visits = []
    data_list_segments = []
    data_list_segments_kml = []
    timestamp_hit = 'T'
    count_activity = 0
    count_multiple_activitys = 0
    
    for file_found in files_found:
        file_found = str(file_found)
        file_name = os.path.basename(file_found)
        
        if file_name.endswith('.json'):
            with open(file_found, 'r', encoding='utf-8-sig') as f:
                data = json.loads(f.read())

            for element in data['timelineObjects']:
                if 'placeVisit' in element:
                    visit_lat = float(element['placeVisit']['location'].get('latitudeE7','0')/10000000)
                    visit_long = float(element['placeVisit']['location'].get('longitudeE7','0')/10000000)
                    visit_placeID = element['placeVisit']['location'].get('placeId','')
                    visit_address = element['placeVisit']['location'].get('address','')
                    visit_name = element['placeVisit']['location'].get('name','')
                    visit_locationConfidence = element['placeVisit']['location'].get('locationConfidence','')
                    
                    #Check placeVisit start timestamps for old format
                    if 'startTimestampMs' in element['placeVisit']['duration']:
                        visit_start_TS = element['placeVisit']['duration'].get('startTimestampMs','')
                        if visit_start_TS != '':
                            if timestamp_hit in visit_start_TS:
                                continue
                            else:
                                visit_start_TS = datetime.datetime.utcfromtimestamp(int(visit_start_TS)/1000).strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            visit_start_TS = ''
                    
                    #Check placeVisit start timestamp for new format
                    elif 'startTimestamp' in element['placeVisit']['duration']:
                        visit_start_TS = element['placeVisit']['duration'].get('startTimestamp','')
                        visit_start_TS = visit_start_TS.replace('T', ' ').replace('Z', '')
                    
                    #Check placeVisit end timestamp for old format
                    if 'endTimestampMs' in element['placeVisit']['duration']:
                        visit_end_TS = element['placeVisit']['duration'].get('endTimestampMs','')
                        if visit_end_TS != '':
                            if timestamp_hit in visit_end_TS:
                                continue
                            else:
                                visit_end_TS = datetime.datetime.utcfromtimestamp(int(visit_end_TS)/1000).strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            visit_end_TS = ''
                    
                    #Check placeVisit end timestamp for new format
                    elif 'endTimestamp' in element['placeVisit']['duration']:
                        visit_end_TS = element['placeVisit']['duration'].get('endTimestamp','')
                        visit_end_TS = visit_end_TS.replace('T', ' ').replace('Z', '')
                    
                    data_list_visits.append((visit_start_TS,visit_end_TS,visit_name,visit_address,visit_lat,visit_long,visit_placeID,file_name))
                    
                if 'activitySegment' in element:
                    segment_start_lat = 'NOT_SPECIFIED'
                    segment_start_long = 'NOT_SPECIFIED'
                    
                    if 'startLocation' in element['activitySegment']:
                        segment_start_lat = float(element['activitySegment']['startLocation'].get('latitudeE7','0'))/10000000
                        segment_start_long = float(element['activitySegment']['startLocation'].get('longitudeE7','0'))/10000000
                        
                    segment_end_lat = 'NOT_SPECIFIED'
                    segment_end_long = 'NOT_SPECIFIED'
                    if 'endLocation' in element['activitySegment']:
                        segment_end_lat = float(element['activitySegment']['endLocation'].get('latitudeE7','0'))/10000000
                        segment_end_long = float(element['activitySegment']['endLocation'].get('longitudeE7','0'))/10000000
                    
                    #Check activitySegment start timestamp for old format
                    if 'startTimestampMs' in element['activitySegment']['duration']:
                        segment_start_TS = element['activitySegment']['duration'].get('startTimestampMs','')
                        if segment_start_TS != '':
                            if timestamp_hit in segment_start_TS:
                                continue
                            else:
                                segment_start_TS = datetime.datetime.utcfromtimestamp(int(segment_start_TS)/1000).strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            segment_start_TS = ''
                    
                    #Check activitySegment start timestamp for new format
                    elif 'startTimestamp' in element['activitySegment']['duration']:
                        segment_start_TS = element['activitySegment']['duration'].get('startTimestamp','')
                        segment_start_TS = segment_start_TS.replace('T', ' ').replace('Z', '')
                    
                    #Check activitySegment end timestamp for old format
                    if 'endTimestampMs' in element['activitySegment']['duration']:
                        segment_end_TS = element['activitySegment']['duration'].get('endTimestampMs','')
                        if segment_end_TS != '':
                            if timestamp_hit in segment_end_TS:
                                continue
                            else:
                                segment_end_TS = datetime.datetime.utcfromtimestamp(int(segment_end_TS)/1000).strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            segment_end_TS = ''
                    
                    #Check activitySegment end timestamp for new format
                    elif 'endTimestamp' in element['activitySegment']['duration']:
                        segment_end_TS = element['activitySegment']['duration'].get('endTimestamp','')
                        segment_end_TS = segment_end_TS.replace('T', ' ').replace('Z', '')
                        
                    segment_activity_type = element['activitySegment'].get('activityType')
                    segment_confidence = element['activitySegment'].get('confidence')
                    
                    if "activities" in element['activitySegment']: # parent activity list
                        count_activity += 1

                        if (len(element['activitySegment']["activities"]) > 1):
                            count_multiple_activitys += 1 

                        count_child = 0
                        subactivity_str = ''
                        for activity in element['activitySegment']['activities']:
                            count_child += 1
                            subactivity_str += str(activity["activityType"] + " [" + str(activity["probability"]) + "], ")
                    
                    data_list_segments_kml.append((segment_start_TS,segment_start_lat,segment_start_long))
                    data_list_segments_kml.append((segment_end_TS,segment_end_lat,segment_end_long))
                    
                    data_list_segments.append((segment_start_TS,segment_end_TS,segment_start_lat,segment_start_long,segment_end_lat,segment_end_long,segment_activity_type,segment_confidence,subactivity_str[:-2],file_name))

        num_entries = len(data_list_visits)
        if num_entries > 0:
            report = ArtifactHtmlReport('Google Semantic Location History - Place Visits')
            report.start_artifact_report(report_folder, 'Google Semantic Location History - Place Visits')
            report.add_script()
            data_headers = ('Visit Start Timestamp','Visit End Timestamp','Name','Address','Latitude','Longitude','PlaceID','File Name')

            report.write_artifact_data_table(data_headers, data_list_visits, file_found)
            report.end_artifact_report()
            
            tsvname = f'Google Semantic Location History - Place Visits'
            tsv(report_folder, data_headers, data_list_visits, tsvname)
            
            tlactivity = f'Google Semantic Location History - Place Visits'
            timeline(report_folder, tlactivity, data_list_visits, data_headers)
            
            data_headers_kml = ('Timestamp','Visit End Timestamp','Name','Address','Latitude','Longitude','PlaceID','File Name')
            kmlactivity = 'Google Semantic Location History - Place Visits'
            kmlgen(report_folder, kmlactivity, data_list_visits, data_headers_kml)            
            
        else:
            logfunc('No Google Location History - Place Visits data available')
            
        num_entries = len(data_list_segments)
        if num_entries > 0:
            report = ArtifactHtmlReport('Google Semantic Location History - Activity Segments')
            report.start_artifact_report(report_folder, 'Google Semantic Location History - Activity Segments')
            report.add_script()
            data_headers = ('Activity Start Timestamp','Activity End Timestamp','Start Latitude','Start Longitude','End Latitude','End Longitude','Activity Type','Confidence','Activities','File Name')

            report.write_artifact_data_table(data_headers, data_list_segments, file_found)
            report.end_artifact_report()
            
            tsvname = f'Google Semantic Location History - Activity Segments'
            tsv(report_folder, data_headers, data_list_segments, tsvname)
            
            tlactivity = f'Google Semantic Location History - Activity Segments'
            timeline(report_folder, tlactivity, data_list_segments, data_headers)
            
            data_headers_segments_kml = ('Timestamp','Latitude','Longitude')
            kmlactivity = 'Google Location History - Activity Segments'
            kmlgen(report_folder, kmlactivity, data_list_segments_kml, data_headers_segments_kml)            
            
        else:
            logfunc('No Google Semantic Location History - Activity Segments data available')

__artifacts__ = {
        'takeoutSemanticLocationHistory': (
            'Google Takeout Archive',
            ('*/Location History*/Semantic Location History/*/*.json'),
            get_takeoutSemanticLocationHistory)
}

# Module Description: Semantic Location by Month
# Author: @AlexisBrignoni
# Date: 2023-05-28
# Artifact version: 0.0.1
# Requirements: none

import json
import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, kmlgen

def get_semanticLocbymonth(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)

        data_list = []
        data_list_wayp =[]
        waypointrecord = 0
        agg = ''
        
        with open(file_found, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for record in data['timelineObjects']:
            for datakey, datavalue in record.items():
                if datakey == 'placeVisit':
                    for key, values in datavalue.items():
                        #print(key, values)
                        if key == 'location':
                            latitudel = values['latitudeE7']/1e7
                            longitudel = values['longitudeE7']/1e7
                            placeid = values['placeId']
                            address = values['address']
                            name = values.get('name','')
                            devicetag = values.get('sourceInfo',' ')
                            if devicetag != ' ':
                                devicetag = values['sourceInfo']['deviceTag']
                            locconfidence = values.get('locationConfidence','')
                            calculatedprob = values.get('calibratedProbability','')
                        elif key == 'otherCandidateLocations':
                            pass
                        elif key == 'duration':
                            starttimestamp = values['startTimestamp'].replace('T',' ').replace('Z','')
                            endtimestamp = values['endTimestamp'].replace('T',' ').replace('Z','')
                        elif key == 'centerLatE7':
                            centerLatE7 = values/1e7
                        elif key == 'centerLngE7':
                            centerLngE7 = values/1e7
                        elif key == 'visitConfidence':
                            visitconfidence = values
                        elif key == 'locationConfidence':
                            locationconfidence = values
                        elif key == 'placeVisitType':
                            placevisittype = values
                        elif key == 'placeVisitImportance':
                            placeVisitImportance = values
                    data_list.append((starttimestamp,endtimestamp,datakey,centerLatE7,centerLngE7,latitudel,longitudel,placeid,name,address,devicetag,locconfidence,calculatedprob,visitconfidence,locationconfidence,placevisittype,placeVisitImportance))
                    
                    starttimestamp = endtimestamp = datakey = centerLatE7 = centerLatE7 = latitudel = longitudel = placeid = name = address = devicetag = placeid = locconfidence = calculatedprob = visitconfidence = locationconfidence = placevisittype = placeVisitImportance = ''
                    
                elif datakey == 'activitySegment':
                    for key, values in datavalue.items():
                        #print(key, values)
                        if key == 'startLocation':
                            startlatitude = values['latitudeE7']/1e7
                            startlongitude = values['longitudeE7']/1e7
                        elif key == 'endLocation':
                            endlatitude = values['latitudeE7']/1e7
                            endlongitude = values['longitudeE7']/1e7
                        elif key == 'duration':
                            starttimestamp = values['startTimestamp'].replace('T',' ').replace('Z','')
                            endtimestamp = values['endTimestamp'].replace('T',' ').replace('Z','')
                        elif key == 'distance':
                            distance = values
                        elif key == 'activityType':
                            activitytype = values
                        elif key == 'confidence':
                            confidence = values
                        elif key == 'activities':
                            activitytypehighprob = values[0]['activityType']
                            activitytypehighprobnumber = values[0]['probability']
                        elif key == 'waypointPath':
                            listofpoints = (values['waypoints'])
                            
                            #for KML 
                            waypointlist = []
                            waypoint_headers = ('Timestamp','Latitude','Longitude')
                            waypointrecord = waypointrecord + 1
                            waypointskmlactivity = f'Waypoint Record: {waypointrecord}'
                            waypointlist.append((starttimestamp,startlatitude,startlongitude))
                            waypointlist.append((endtimestamp,endlatitude,endlongitude))
                            
                            #for HTML
                            agg = agg + f'{startlatitude},{startlongitude}<br>'
                            agg = agg + f'{endlatitude},{endlongitude}<br>'
                            
                            for points in listofpoints:
                                waylat = points['latE7']/1e7
                                waylong = points['lngE7']/1e7
                                waypointlist.append(('',waylat,waylong))
                                
                                #for html
                                agg = agg + f'{waylat},{waylong}<br>'
                            
                            data_headers = ('Timestamp','Latitude','Longitude')
                            kmlactivity = f'{filename} - Waypoint Track - {waypointrecord}'
                            kmlgen(report_folder, kmlactivity, waypointlist, data_headers)
                            waypointlist = []
                            
                        elif key == 'parkingEvent':
                            parkingloclat = values['location']['latitudeE7']/1e7
                            parkingloclong = values['location']['longitudeE7']/1e7
                            parkingaccuracy = values['location']['accuracyMetres']
                            parkinglocationtime = values['timestamp'].replace('T',' ').replace('Z','')
                            
                            
                    data_list_wayp.append((starttimestamp,endtimestamp,datakey,startlatitude,startlongitude,endlatitude,endlongitude,distance,activitytype,confidence,activitytypehighprob,activitytypehighprobnumber,agg,waypointrecord,parkinglocationtime,parkingloclat,parkingloclong,parkingaccuracy))
                    
                    starttimestamp = endtimestamp = datakey = startlatitude = startlongitude = endlatitude = endlongitude = distance = activitytype = confidence = activitytypehighprob = activitytypehighprobnumber = agg = parkinglocationtime = parkingloclat = parkingloclong = parkingaccuracy = ''
        
        
        num_entries = len(data_list_wayp)
        if num_entries > 0:
            description = 'Semantic Locations - Activity by Month'
            report = ArtifactHtmlReport('Semantic Locations - Activity By Month')
            report.start_artifact_report(report_folder, f'{filename} - Activity', description)
            report.add_script()
            data_headers = ('Timestamp','End Timestamp','Record','Start Latitude','Start Longitude','End Latitude','End Longitude','Distance','Activity Type','Confidence','Highest Activity Type Probability','Activity High Probability Percentage','Waypoints','Waypoint Record Number for KML','Parking Location Time','Parking Location Latitude','Parking Location Longitude','Parking Accuracy in Meters')

            report.write_artifact_data_table(data_headers, data_list_wayp, file_found, html_no_escape=['Waypoints'])
            report.end_artifact_report()
            
            tsvname = f'{filename} - Activity'
            tsv(report_folder, data_headers, data_list_wayp, tsvname)
            
            tlactivity = f'{filename} - Activity'
            timeline(report_folder, tlactivity, data_list_wayp, data_headers)
            
        else:
            logfunc('No Semantic Locations Activity by Month data available')
        
        num_entries = len(data_list)
        if num_entries > 0:
            description = 'Semantic Locations - Places visited by Month'
            report = ArtifactHtmlReport('Semantic Locations - Places By Month')
            report.start_artifact_report(report_folder, f'{filename} - Places', description)
            report.add_script()
            data_headers = ('Timestamp','End Timestamp','Record','Latitude','Longitude','Additional Latitude','Additional Longitude','Place ID','Name','Address','Device Tag','Location Confidence','Calculated Probability','Visit Confidence','Location Confidence','Place Visit Type','Place Visit Importance')
            
            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()
            
            tsvname = f'{filename} - Places'
            tsv(report_folder, data_headers, data_list, tsvname)
            
            tlactivity = f'{filename} - Places'
            timeline(report_folder, tlactivity, data_list, data_headers)
            
            kmlactivity = f'{filename} - Places'
            kmlgen(report_folder, kmlactivity, data_list, data_headers)
        else:
            logfunc('No Semantic Locations Places by Month available')

__artifacts__ = {
        "semanticLocationsMonth": (
            "Google Returns Semantic Locations by Month",
            ('*/Location History/Semantic Location History/*/*_*.json'),
            get_semanticLocbymonth)
}

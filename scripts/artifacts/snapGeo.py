import os
import datetime

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html, kmlgen

def monthletter(month):
    monthdict = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    return monthdict[month]

def clean_and_group_data(input_data):
    # Split the input data into lines
    lines = input_data.split('\n')
    
    # Initialize variables to track whether we are in a section to exclude
    exclude = False
    grouped_data = []
    current_section = []
    
    for line in lines:
        # Check if the line contains dashes or equal signs
        if line.startswith('---') or line.startswith('==='):
            exclude = not exclude
            if not exclude:
                # End of an excluded section, start a new section
                if current_section:
                    grouped_data.append(current_section)
                    current_section = []
            continue
        
        # Add the line to current_section if we are not in an excluded section
        if not exclude and line.strip():
            current_section.append(line.strip())
            
    # Add the last section to the grouped data if it exists
    if current_section:
        grouped_data.append(current_section)
        
    return grouped_data

def get_snapGeo(files_found, report_folder, seeker, wrap_text, time_offset):

    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        one = (os.path.split(file_found))
        username = (os.path.basename(one[0]))
        
        data_list2 = []
        
        if filename.startswith('geo_locations.csv'):
            with open(file_found) as f:
                input_data = f.read() 
                
            # Run the cleaning and grouping function
            grouped_data = clean_and_group_data(input_data)
            
            for x in grouped_data:
                data_list = []
                header = x[0]
            
                for y in x[1:]:
                    item = y.strip().split(',')
                    data_list.append(item)
            
                    
                if header.startswith('latitude,longitude,accuracy,timestamp,is_live_location'):
                    header = header.strip().split(',')
                    header2 = header
                    header2[0]='Timestamp'
                    header2[1]='Latitude'
                    header2[2]='Longitude'
                    header2[3]='Accuracy'
                    header2[4]='Is Live Location'
                    data_list2 = data_list
                    
                    for x in data_list2:
                        timestamp = x[3].split(' ')
                        year = timestamp[5]
                        day = timestamp[2]
                        time = timestamp[3]
                        month = monthletter(timestamp[1])
                        timestampfinal = (f'{year}-{month}-{day} {time}')
                        lat = x[0]
                        lon = x[1]
                        acc = x[2]
                        x[0] = timestampfinal
                        x[1] = lat
                        x[2] = lon
                        x[3] = acc
                        
                    
        if len(data_list2) > 0:
            report = ArtifactHtmlReport(f'Snapchat - Geolocation')
            report.start_artifact_report(report_folder, f'Snapchat - Geolocation - {username}')
            report.add_script()
            #data_headers = ('Timestamp','Username','Name','Registration IP','Country','Phone Number','Carrier')
            report.write_artifact_data_table(header2, data_list2, file_found, html_no_escape=['Media'])
            report.end_artifact_report()
            
            tsvname = f'Snapchat - Geolocation - {username}'
            tsv(report_folder, header2, data_list2, tsvname)
            
            tlactivity = f'Snapchat - Geolocation - {username}'
            timeline(report_folder, tlactivity, data_list2, header2)
            
            kmlactivity = f'Snapchat - Geolocation - {username}'
            kmlgen(report_folder, kmlactivity, data_list2, header2) 
            
        else:
            logfunc(f'No Snapchat - Geolocation - {username}')
        
        data_list2 = []
    
__artifacts__ = {
        "snapGeo": (
            "Snapchat Returns",
            ('*/geo_locations.csv'),
            get_snapGeo)
}
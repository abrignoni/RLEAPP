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

def get_snapFriendsN(files_found, report_folder, seeker, wrap_text, time_offset):

    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        one = (os.path.split(file_found))
        username = (os.path.basename(one[0]))
        
        if filename.startswith('friends_list.csv'):
            with open(file_found) as f:
                input_data = f.read() 
                
            # Run the cleaning and grouping function
            grouped_data = clean_and_group_data(input_data)
            
            for x in grouped_data:
                data_list = []
                header = x[0]
            
                for y in x[1:]:
                    item = y #.strip().split(',')
                    data_list.append((item,))
            
            data_list.append((header,))
                
                
                        
                    
        if len(data_list) > 0:
            report = ArtifactHtmlReport(f'Snapchat - Friends')
            report.start_artifact_report(report_folder, f'Snapchat - Friends - {username}')
            report.add_script()
            data_headers = ('Friends',)
            report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Media'])
            report.end_artifact_report()
            
            tsvname = f'Snapchat - Friends - {username}'
            tsv(report_folder, data_headers, data_list, tsvname)
            
            tlactivity = f'Snapchat - Friends- {username}'
            timeline(report_folder, tlactivity, data_list, data_headers)
            
        else:
            logfunc(f'No Snapchat - Friends - {username}')
    
__artifacts__ = {
        "snapFriendsN": (
            "Snapchat Returns",
            ('*/friends_list.csv'),
            get_snapFriendsN)
}
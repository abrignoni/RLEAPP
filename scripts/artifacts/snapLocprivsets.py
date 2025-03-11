import os
import datetime

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html

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

def get_snapLocprivsets(files_found, report_folder, seeker, wrap_text):

    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        one = (os.path.split(file_found))
        username = (os.path.basename(one[0]))
        
        data_list2 = []
        
        if filename.startswith('loc_priv_sets.csv'):
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
                    
                    
                if header.startswith('timestamp,audience,allowlist,blocklist,ghost_mode,ghost_mode_expiration,live_session_ids,live_session_expirations'):
                    header = header.strip().split(',')
                    header2 = header
                    header2[0]='Timestamp'
                    header2[1]='Audience'
                    header2[2]='Allow List'
                    header2[3]='Block List'
                    header2[4]='Ghost Mode'
                    header2[5]='Ghost Mode Expiration'
                    header2[6]='Live Session IDS'
                    header2[7]='Live Session Expirations'
                    data_list2 = data_list
                    for x in data_list2:
                        timestamp = x[0].split(' ')
                        year = timestamp[5]
                        day = timestamp[2]
                        time = timestamp[3]
                        month = monthletter(timestamp[1])
                        timestampfinal = (f'{year}-{month}-{day} {time}')
                        x[0] = timestampfinal
                        
                    
        if len(data_list2):
            report = ArtifactHtmlReport(f'Snapchat - Location Privacy Settings')
            report.start_artifact_report(report_folder, f'Snapchat - Location Privacy Settings - {username}')
            report.add_script()
            #data_headers = ('Timestamp','Username','Name','Registration IP','Country','Phone Number','Carrier')
            report.write_artifact_data_table(header2, data_list2, file_found, html_no_escape=['Media'])
            report.end_artifact_report()
            
            tsvname = f'Snapchat - Location Privacy Settings - {username}'
            tsv(report_folder, header2, data_list2, tsvname)
            
            tlactivity = f'Snapchat - Location Privacy Settings - {username}'
            timeline(report_folder, tlactivity, data_list2, header2)
            
        else:
            logfunc(f'No Snapchat - Location Privacy Settings - {username}')
            
        data_list2 = []
    
__artifacts__ = {
        "snapLocprivsets": (
            "Snapchat Returns",
            ('*/loc_priv_sets.csv'),
            get_snapLocprivsets)
}
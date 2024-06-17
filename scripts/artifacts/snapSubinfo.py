import os
import datetime
import csv
import codecs
import shutil

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

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
    

def get_snapSubinfo(files_found, report_folder, seeker, wrap_text, time_offset):
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        one = (os.path.split(file_found))
        username = (os.path.basename(one[0]))
        
        data_list2 = []
        data_list3 = []
        data_list4 = []
        data_list5 = []
        data_list6 = []
        data_list7 = []

        if filename.startswith('subscriber_info.csv'):
            with open(file_found) as f:
                input_data = f.read() 
                
            # Run the cleaning and grouping function
            grouped_data = clean_and_group_data(input_data)
            
            """
            # Print the grouped data
            for i, section in enumerate(grouped_data):
                print(f"Section {i+1}:")
                for line in section:
                    print(line)
                print()
                
            # If you want to see the list of lists directly
            print(grouped_data)
            """
            
            
            
            for x in grouped_data:
                data_list = []
                header = x[0]
                
                for y in x[1:]:
                    item = y.strip().split(',')
                    data_list.append(item)
                    
                    
                if header.startswith('"Target username "'):
                    header1 = list((header,''))
                    data_list1 = data_list
                    
                elif header.startswith('username,user_id,verified_email_address'):
                    header = header.strip().split(',')
                    header2 = header
                    header2[0]='Timestamp'
                    header2[1]='User ID'
                    header2[2]='Verified Email Address'
                    header2[3]='Email status'
                    header2[4]='Pending Email Address'
                    header2[5]='Username'
                    header2[6]='Creation IP'
                    header2[7]='Verified Phone Number'
                    header2[8]='Phone Status'
                    header2[9]='Pending Phone Number'
                    header2[10]='Display Name'
                    header2[11]='Status'
                    data_list2 = data_list
                    for x in data_list2:
                        if x[5] == '':
                            username = x[0]
                            x[0] = x[5]
                            x[5] = username
                        else:
                            timestamp = x[5].split(' ')
                            year = timestamp[5]
                            day = timestamp[2]
                            time = timestamp[3]
                            month = monthletter(timestamp[1])
                            timestampfinal = (f'{year}-{month}-{day} {time}')
                            x[5] = timestampfinal
                            username = x[0]
                            x[0] = x[5]
                            x[5] = username
                    
                elif header.startswith('date,action,old_value,new_value,reason'): #Done
                    header = header.strip().split(',')
                    header3 = header
                    header3[0]='Timestamp'
                    header3[1]='Action'
                    header3[2]='Old Value'
                    header3[3]='New Value'
                    header3[4]='Reason'
                    data_list3 = data_list
                    for x in data_list3:
                        timestamp = x[0].split(' ')
                        year = timestamp[5]
                        day = timestamp[2]
                        time = timestamp[3]
                        month = monthletter(timestamp[1])
                        timestampfinal = (f'{year}-{month}-{day} {time}')
                        x[0] = timestampfinal
            
                elif header.startswith('old_value,new_value,timestamp'):
                    header = header.strip().split(',')
                    header4 = header
                    header4[0]='Timestamp'
                    header4[1]='Old Value'
                    header4[2]='New Value'
                    data_list4 = data_list
                    for x in data_list4:
                        timestamp = x[2].split(' ')
                        year = timestamp[5]
                        day = timestamp[2]
                        time = timestamp[3]
                        month = monthletter(timestamp[1])
                        timestampfinal = (f'{year}-{month}-{day} {time}')
                        oldval = x[0]
                        newval = x[1] 
                        x[0] = timestampfinal
                        x[1] = oldval
                        x[2] = newval
                        
                elif header.startswith('email_verified_timestamp,phone_verified_timestamp,birthdate,last_active,follower_count,app_version,2FA_status'):
                    header = header.strip().split(',')
                    header5 = header
                    header5[0]='Email Verified Timestamp'
                    header5[1]='Phone Verified Timestamp'
                    header5[2]='Birthdate'
                    header5[3]='Last Active'
                    header5[4]='Follower Count'
                    header5[5]='App Version'
                    header5[6]='2FA Status'
                    data_list5 = data_list
                
                elif header.startswith('snap_privacy,story_privacy'):
                    header = header.strip().split(',')
                    header6 = header
                    header6[0]='Snap Privacy'
                    header6[1]='Story Privacy'
                    data_list6 = data_list
                
                elif header.startswith('is_bitmoji_user,bitmoji_gender'):
                    header = header.strip().split(',')
                    header7 = header
                    header7[0]='Is Bitmoji User'
                    header7[1]='Bitmoji Gender'
                    data_list7 = data_list
                       
        if len(data_list2) > 0:
            report = ArtifactHtmlReport(f'Snapchat - Account Information')
            report.start_artifact_report(report_folder, f'Snapchat - Account Information - {username}')
            report.add_script()
            report.write_artifact_data_table(header2, data_list2, file_found)
            report.end_artifact_report()
            
            tsvname = f'Snapchat - Account Information - {username}'
            tsv(report_folder, header2, data_list2, tsvname)
            
            tlactivity = f'Snapchat - Account Information - {username}'
            timeline(report_folder, tlactivity, data_list2, header2)
        else:
            logfunc(f'Snapchat - Account Information - {username}')    
            
        data_list2 = []
        
        if len(data_list3) > 0:
            report = ArtifactHtmlReport(f'Snapchat - Account Change History')
            report.start_artifact_report(report_folder, f'Snapchat - Account Change History - {username}')
            report.add_script()
            report.write_artifact_data_table(header3, data_list3, file_found)
            report.end_artifact_report()
            
            tsvname = f'Snapchat - Account Change History - {username}'
            tsv(report_folder, header3, data_list3, tsvname)
            
            tlactivity = f'Snapchat - Account Change History - {username}'
            timeline(report_folder, tlactivity, data_list3, header3)
        else:
            logfunc(f'Snapchat - Account Change History - {username}')
        
        data_list3 = []
            
        if len(data_list4) > 0:
            report = ArtifactHtmlReport(f'Snapchat - Username History')
            report.start_artifact_report(report_folder, f'Snapchat - Account Username History - {username}')
            report.add_script()
            report.write_artifact_data_table(header4, data_list4, file_found)
            report.end_artifact_report()
            
            tsvname = f'Snapchat - Account Username History - {username}'
            tsv(report_folder, header4, data_list4, tsvname)
            
            tlactivity = f'Snapchat - Account Username History - {username}'
            timeline(report_folder, tlactivity, data_list4, header4)
        else:
            logfunc(f'Snapchat - Account Username History - {username}')
        
        data_list4 = []
        
        if len(data_list5) > 0:
            report = ArtifactHtmlReport(f'Snapchat - Account Data')
            report.start_artifact_report(report_folder, f'Snapchat - Account Data - {username}')
            report.add_script()
            report.write_artifact_data_table(header5, data_list5, file_found)
            report.end_artifact_report()
            
            tsvname = f'Snapchat - Account Data - {username}'
            tsv(report_folder, header5, data_list5, tsvname)
            
            tlactivity = f'Snapchat - Account Data - {username}'
            timeline(report_folder, tlactivity, data_list5, header5)
        else:
            logfunc(f'Snapchat - Account Data - {username}')
        
        data_list5 = []
        
        if len(data_list6) > 0:
            report = ArtifactHtmlReport(f'Snapchat - Privacy')
            report.start_artifact_report(report_folder, f'Snapchat - Privacy - {username}')
            report.add_script()
            report.write_artifact_data_table(header6, data_list6, file_found)
            report.end_artifact_report()
            
            tsvname = f'Snapchat - Privacy - {username}'
            tsv(report_folder, header6, data_list6, tsvname)
            
            tlactivity = f'Snapchat - Privacy - {username}'
            timeline(report_folder, tlactivity, data_list6, header6)
        else:
            logfunc(f'Snapchat - Privacy - {username}')
        
        data_list6 = []
        
        if len(data_list7) > 0:
            report = ArtifactHtmlReport(f'Snapchat - Bitmoji')
            report.start_artifact_report(report_folder, f'Snapchat - Bitmoji - {username}')
            report.add_script()
            report.write_artifact_data_table(header7, data_list7, file_found)
            report.end_artifact_report()
            
            tsvname = f'Snapchat - Bitmoji - {username}'
            tsv(report_folder, header7, data_list7, tsvname)
            
            tlactivity = f'Snapchat - Bitmoji - {username}'
            timeline(report_folder, tlactivity, data_list7, header7)
        else:
            logfunc(f'Snapchat - Bitmoji - {username}')
        
        data_list7 = []
                
__artifacts__ = {
        "ssnapSubinfo": (
            "Snapchat Returns",
            ('*/subscriber_info.csv'),
            get_snapSubinfo)
}
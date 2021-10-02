import os
import datetime
import csv
import codecs
import shutil
import magic

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def monthletter(month):
    monthdict = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    return monthdict[month]

def get_snapChatsubsinfo(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        one = (os.path.split(file_found))
        username = (os.path.basename(one[0]).split('-')[0])

        if filename.startswith('subscriber_information.csv'):
            data_list_subs =[]
            data_list_change =[]
            with open(file_found, 'r') as f:
                delimited = csv.reader(f, delimiter=',')
                for iteration, item in enumerate(delimited):
                    if iteration not in [0,1,2,3,5,6,7,8]:
                        if iteration == 4:
                            #subscriber info
                            fecha = item[2]
                            timestamp = fecha.split(' ')
                            year = timestamp[5]
                            day = timestamp[2]
                            time = timestamp[3]
                            month = monthletter(timestamp[1])
                            timestampfinal = (f'{year}-{month}-{day} {time}')
                            data_list_subs.append((timestampfinal, item[0], item[1], item[3], item[4], item[5], item[6]))
                            
                        else:
                            #subscriber info
                            fecha = item[0]
                            timestamp = fecha.split(' ')
                            year = timestamp[5]
                            day = timestamp[2]
                            time = timestamp[3]
                            month = monthletter(timestamp[1])
                            timestampfinal = (f'{year}-{month}-{day} {time}')
                            data_list_change.append((timestampfinal, item[1], item[2], item[3], item[4]))
                            
        if data_list_subs:
            report = ArtifactHtmlReport(f'Snapchat - Subscriber Info')
            report.start_artifact_report(report_folder, f'Snapchat - Subscriber Info - {username}')
            report.add_script()
            data_headers_sub = ('Timestamp UTC', 'Username', 'Email', 'Creation IP', 'Phone Number', 'Display Name', 'Status')
            report.write_artifact_data_table(data_headers_sub, data_list_subs, file_found)
            report.end_artifact_report()
            
            tsvname = f'Snapchat - Subscriber Info - {username}'
            tsv(report_folder, data_headers_sub, data_list_subs, tsvname)
            
            tlactivity = f'Snapchat - Subscriber Info - {username}'
            timeline(report_folder, tlactivity, data_list_subs, data_headers_sub)
        else:
            logfunc(f'Snapchat - Subscriber Info - {username}')
            
        if data_list_change:
            report = ArtifactHtmlReport(f'Snapchat - Account Change History')
            report.start_artifact_report(report_folder, f'Snapchat - Account Change History - {username}')
            report.add_script()
            data_headers = ('Timestamp', 'Action', 'Old Value', 'New Value', 'Reason')
            report.write_artifact_data_table(data_headers, data_list_change, file_found)
            report.end_artifact_report()
            
            tsvname = f'Snapchat - Account Change History - {username}'
            tsv(report_folder, data_headers, data_list_change, tsvname)
            
            tlactivity = f'Snapchat - Account Change History - {username}'
            timeline(report_folder, tlactivity, data_list_change, data_headers)
        else:
            logfunc(f'Snapchat - Account Change History - {username}')
                
        
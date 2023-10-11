import os
import datetime
import csv
import codecs
import shutil
import magic

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html, kmlgen

def monthletter(month):
    monthdict = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    return monthdict[month]

def get_snapChatmemo(files_found, report_folder, seeker, wrap_text, time_offset):
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        one = (os.path.split(file_found))
        username = (os.path.basename(one[0]))
        
        data_list = [] 
        
        if filename.startswith('memories.csv'):
            pathforreport = file_found
            
            with open(file_found, 'r') as f:
                for index, line in enumerate(f):
                    #print(f'linea: {line}')
                    if '==' in line:
                        limit = index + 1
                        break
                    
                   
            with open(file_found, 'r') as f:
                for index, line in enumerate(f):
                    #print(f'linea: {line}')
                    if index > limit:
                        memories = line.strip().split(',')
                        id = memories[0]
                        media = memories[1]
                        thumb = media_to_html(media, files_found, report_folder)
                        encrypted = memories[2]
                        sourcet = memories[3]
                        latitude = memories[4]
                        longitude = memories[5]
                        duration = memories[6]
                        fecha = memories[7]
                        timestamp = fecha.split(' ')
                        year = timestamp[5]
                        day = timestamp[2]
                        time = timestamp[3]
                        month = monthletter(timestamp[1])
                        timestampfinal = (f'{year}-{month}-{day} {time}')
                        
                        data_list.append((timestampfinal, memories[0], memories[1], thumb, memories[2], memories[3], memories[4], memories[5], memories[6]))
                        
        if len(data_list) > 0 :
            report = ArtifactHtmlReport(f'Snapchat - Memories Metadata')
            report.start_artifact_report(report_folder, f'Snapchat - Memories Metadata - {username}')
            report.add_script()
            data_headers = ('Timestamp', 'ID', 'Media ID','Media','Encrypted', 'Source', 'Latitude', 'Longitude', 'Duration')
            report.write_artifact_data_table(data_headers, data_list, pathforreport, html_no_escape=['Media'])
            report.end_artifact_report()
            
            tsvname = f'Snapchat - Memories Metadata - {username}'
            tsv(report_folder, data_headers, data_list, tsvname)
            
            tlactivity = f'Snapchat - Memories Metadata- {username}'
            timeline(report_folder, tlactivity, data_list, data_headers)
            
            kmlactivity = f'Snapchat - Memories Metadata  - {username}'
            kmlgen(report_folder, kmlactivity, data_list, data_headers)
            
    if len(data_list) < 1:
        logfunc(f'No Snapchat - Memories Metadata - {username}')
            
__artifacts__ = {
        "snapChatmemo": (
            "Snapchat Returns",
            ('*/memories.csv','*/memories*.jpg','*/memories*.mp4'),
            get_snapChatmemo)
}     
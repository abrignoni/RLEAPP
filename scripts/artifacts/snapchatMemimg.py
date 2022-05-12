import os
import datetime
import csv
import calendar

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html, kmlgen

def monthletter(month):
    monthdict = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    return monthdict[month]

def get_snapchatMemimg(files_found, report_folder, seeker, wrap_text):

    userlist = []
    start_terms = ('memories','custom_sticker')
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        one = (os.path.split(file_found))
        username = (os.path.basename(one[0]).split('-')[0])
        if username not in userlist:
            userlist.append(username)
            print(userlist)
            
    for name in userlist:
        data_list_media = []
        for file_found in files_found:
            file_found = str(file_found)
            filename = os.path.basename(file_found)
            
            if filename.startswith(start_terms):
                metadata = filename.split('~')
                if name == metadata[3]:
                    typeoffile = metadata[0]
                    timestamp = metadata[2]
                    timestamp = timestamp.split('-')
                    org_string = timestamp[5]
                    mod_string = org_string[:-3]
                    timestamp = f'{timestamp[0]}-{timestamp[1]}-{timestamp[2]} {timestamp[3]}:{timestamp[4]}:{mod_string}'
                    usernamefile = metadata[3]
                    media = media_to_html(file_found, files_found, report_folder)
                    file_found_dir = os.path.dirname(file_found)
                    data_list_media.append((timestamp,media,filename,usernamefile,typeoffile,))
                    
        if data_list_media:
            report = ArtifactHtmlReport(f'Snapchat - Memories')
            report.start_artifact_report(report_folder, f'Snapchat - Memories - {name}')
            report.add_script()
            data_headers = ('Timestamp','Media','Filename','User','File Type')
            report.write_artifact_data_table(data_headers, data_list_media, file_found_dir, html_no_escape=['Media'])
            report.end_artifact_report()
            
            tsvname = f'Snapchat - Memories - {name}'
            tsv(report_folder, data_headers, data_list_media, tsvname)
            
            tlactivity = f'Snapchat - Memories- {name}'
            timeline(report_folder, tlactivity, data_list_media, data_headers)
        else:
            logfunc(f'No Snapchat - Memories - {name}')
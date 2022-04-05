import os
import json

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html

def get_snapChathistory(files_found, report_folder, seeker, wrap_text):

    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        one = (os.path.split(file_found))
        username = (os.path.basename(one[0]))
        
        if filename.startswith('chat_history.json'):
            data_list =[]
            with open(file_found, 'r') as fp:
                deserialized = json.load(fp)
            
            for x, y in deserialized.items():
                for mess in y:
                    typeline = x
                    #print(itemsdict)
                    if mess.get('From'):
                        directionality = mess['From']
                        directionality = 'From: ' + directionality
                    elif mess.get('To'):
                        directionality = mess['To']
                        directionality = 'To: ' + directionality
                        
                    mediatype = mess['Media Type']
                    created = mess['Created']
                    textm = mess['Text']
                    
                    data_list.append((created, directionality, textm, mediatype, typeline ))
                    
            if data_list:
                report = ArtifactHtmlReport(f'Snapchat - Chat History')
                report.start_artifact_report(report_folder, f'Snapchat - Chat History')
                report.add_script()
                data_headers = ('Timestamp','Directionality','Text','Media Type','Message Type')
                report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Chat History'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                tlactivity = f'Snapchat - Chat History'
                timeline(report_folder, tlactivity, data_list, data_headers)
                
            else:
                logfunc(f'Snapchat - Chat History')
    
    
    
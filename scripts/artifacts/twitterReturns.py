import os
from datetime import datetime
import csv
import codecs
import shutil
import magic

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html

def get_twitterReturns(files_found, report_folder, seeker, wrap_text):
    data_list_dms =[]
    data_list_groupdm = []
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.endswith('-dms.txt'):
            with open(file_found, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            count = 0    
            for line in lines:
                count += 1
                
                if count < 4:
                    pass
                    
                if 'Conversation ID' in line:
                    convoid = line.split('#')[1].replace('*','').strip()
                    
                if '"id" :' in line:
                    idc = line.split(': ')[1].replace(',', '').strip()
                    
                if '"sender_id" :' in line:
                    sid = line.split(': ')[1].replace(',', '').strip()
                    
                if '"text" :' in line:
                    text = line.split(': ')[1].replace(',', '').replace('"','').strip()
                    
                if '"recipient_id" :' in line:
                    rid = line.split(': ')[1].replace(',', '').strip()
                    
                if '"created_at" :' in line:
                    date = (line.split(': ')[1].replace(',', '').replace('"','').strip().split(' '))
                    timetochange = f'{date[1]} {date[2]} {date[3]} {date[5]}'
                    
                    datetime_object = datetime.strptime(timetochange, '%b %d %H:%M:%S %Y')
                    timestamp = (datetime_object)
                    
                    data_list_dms.append((timestamp, convoid, sid, rid, text))	
                    
                
        if filename.endswith('-groupdm.txt'):
            with open(file_found, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            count = 0    
            for line in lines:
                count += 1
                
                if count < 3:
                    pass
                    
                if 'Group Conversation ID' in line:
                    convoid = line.split('#')[1].replace('*','').strip()
                    
                if 'JoinConversation, current participants (user IDs):' in line:
                    timestampj = (line.split(': ')[0].split('+')[0].strip())
                    messagea = (line.split(': ')[1].replace(',', ''))
                    messageb = (line.split(': ')[2])
                    messagefinal = (f'{messagea}: {messageb}')
                    data_list_groupdm.append((timestampj, convoid, '', '', messagefinal))
                    
                if 'ParticipantsJoin (user IDs):' in line:
                    #print(line)
                    timestampk = (line.split(': ')[0].split('+')[0].strip())
                    messagec = (line.split(': ')[1])
                    messaged = (line.split(': ')[2].strip())
                    messagefinala = (f'{messagec}: {messaged}')
                    data_list_groupdm.append((timestampk, convoid, '', '', messagefinala))
                    
                if '"id" :' in line:
                    idc = line.split(': ')[1].replace(',', '').strip()
                    
                if '"text" :' in line:
                    text = line.split(': ')[1].replace(',', '').replace('"','').strip()
                    
                if '"sender_id" :' in line:
                    sid = line.split(': ')[1].replace(',', '').strip()
                    
                if '"recipient_id" :' in line:
                    rid = line.split(': ')[1].replace(',', '').strip()
                    
                if '"created_at" :' in line:
                    date = (line.split(': ')[1].replace(',', '').replace('"','').strip().split(' '))
                    timetochange = f'{date[1]} {date[2]} {date[3]} {date[5]}'
                    
                    datetime_object = datetime.strptime(timetochange, '%b %d %H:%M:%S %Y')
                    timestamp = (datetime_object)
                    
                    data_list_groupdm.append((timestamp, convoid, sid, rid, text))
                            
    if data_list_dms:
        report = ArtifactHtmlReport('Twitter Returns - Direct Messages')
        report.start_artifact_report(report_folder, 'Twitter Returns - Direct Messages')
        report.add_script()
        data_headers = ('Timestamp', 'Conversation ID', 'Sender ID', 'Recipient ID', 'Message')
        report.write_artifact_data_table(data_headers, data_list_dms, file_found)
        report.end_artifact_report()
        
        tsvname = f'Twitter Returns - Direct Messages'
        tsv(report_folder, data_list_dms, data_headers, tsvname)
        
        tlactivity = f'Twitter Returns - Direct Messages'
        timeline(report_folder, tlactivity, data_list_dms, data_headers)
    else:
        logfunc('No Twitter Returns - Direct Messages data available')
        
    if data_list_groupdm:
        report = ArtifactHtmlReport('Twitter Returns - Group Messages')
        report.start_artifact_report(report_folder, 'Twitter Returns - Group Messages')
        report.add_script()
        data_headers = ('Timestamp', 'Conversation ID', 'Sender ID', 'Recipient ID', 'Message')
        report.write_artifact_data_table(data_headers, data_list_groupdm, file_found, html_no_escape=['Content'])
        report.end_artifact_report()
        
        tsvname = f'Twitter Returns - Group Messages'
        tsv(report_folder, data_list_groupdm, data_headers, tsvname)
        
        tlactivity = f'Twitter Returns - Group Messages'
        timeline(report_folder, tlactivity, data_list_groupdm, data_headers)
    else:
        logfunc('No Twitter Returns - Group Messages data available')
        
        
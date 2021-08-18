import os
import datetime
import csv
import codecs
import shutil
import magic

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_kikReturns(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('bind.txt'):
            data_list =[]
            with open(file_found, 'r') as f:
                delimited = csv.reader(f, delimiter='\t')
                for item in delimited:
                    utctimestamp = (datetime.datetime.fromtimestamp(int(item[0])/1000).strftime('%Y-%m-%d %H:%M:%S'))
                    user = item[1]
                    ip = item[2]
                    port = item [3]
                    timestamp = item[4]
                    info = item[5]
                    data_list.append((utctimestamp, timestamp, user, ip, port, info))
                
            if data_list:
                report = ArtifactHtmlReport('Kik - Bind')
                report.start_artifact_report(report_folder, 'Kik - Bind.txt')
                report.add_script()
                data_headers = ('Timestamp UTC', 'Timestamp', 'User', 'IP', 'Port', 'Info')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Kik - bind'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                tlactivity = f'Kik - bind'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Kik - Bind data available')
                
        if filename.startswith('chat_platform_sent_received.txt'):
            data_list =[]
            with open(file_found, 'r') as f:
                delimited = csv.reader(f, delimiter='\t')
                for item in delimited:
                    utctimestamp = (datetime.datetime.fromtimestamp(int(item[0])/1000).strftime('%Y-%m-%d %H:%M:%S'))
                    user = item[1]
                    user_other = item[2]
                    app = item[3]
                    contentID = item[4]
                    info = item[5]
                    timestamp = item[6]
                    thumb = ''
                    for match in files_found:
                        if contentID in match:
                            shutil.copy2(match, report_folder)
                            mimetype = magic.from_file(match, mime = True)
                            
                            if mimetype == 'video/mp4':
                                thumb = f'<video width="320" height="240" controls="controls"><source src="{report_folder}{contentID}" type="video/mp4">Your browser does not support the video tag.</video>'
                            else:
                                thumb = f'<img src="{report_folder}{contentID}" width="300"></img>'
                            
                            data_list.append((utctimestamp, timestamp, user, user_other, app, info, contentID, thumb))
                            break
                            

            if data_list:
                report = ArtifactHtmlReport('Kik - Chat Platform Sent Received')
                report.start_artifact_report(report_folder, 'Kik - Chat Platform Sent Received')
                report.add_script()
                data_headers = ('Timestamp UTC', 'Timestamp', 'User', 'User', 'App', 'Info', 'Content ID', 'Content')
                report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Content'])
                report.end_artifact_report()
                
                tsvname = f'Kik - Chat Platform Sent Received'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                tlactivity = f'Kik - Chat Platform Sent Received'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Kik Chat Platform Sent Received data available')
        
        if filename.startswith('chat_platform_sent.txt'):
            data_list =[]
            with open(file_found, 'r') as f:
                delimited = csv.reader(f, delimiter='\t')
                for item in delimited:
                    utctimestamp = (datetime.datetime.fromtimestamp(int(item[0])/1000).strftime('%Y-%m-%d %H:%M:%S'))
                    user = item[1]
                    user_other = item[2]
                    app = item[3]
                    contentID = item[4]
                    info = item[5]
                    timestamp = item[6]
                    thumb = ''
                    for match in files_found:
                        if contentID in match:
                            shutil.copy2(match, report_folder)
                            mimetype = magic.from_file(match, mime = True)
                            
                            if mimetype == 'video/mp4':
                                thumb = f'<video width="320" height="240" controls="controls"><source src="{report_folder}{contentID}" type="video/mp4">Your browser does not support the video tag.</video>'
                            else:
                                thumb = f'<img src="{report_folder}{contentID}" width="300"></img>'
                                
                            data_list.append((utctimestamp, timestamp, user, user_other, app, info, contentID, thumb))
                            break
                        
                        
            if data_list:
                report = ArtifactHtmlReport('Kik - Chat Platform Sent')
                report.start_artifact_report(report_folder, 'Kik  - Chat Platform Sent')
                report.add_script()
                data_headers = ('Timestamp UTC', 'Timestamp', 'User', 'User', 'App', 'IP', 'Content ID', 'Content')
                report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Content'])
                report.end_artifact_report()
                
                tsvname = f'Kik - Chat Platform Sent'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                tlactivity = f'Kik - Chat Platform Sent'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Kik Chat Platform Sent data available')
        
        if filename.startswith('chat_sent_received.txt'):
            data_list =[]
            with open(file_found, 'r') as f:
                delimited = csv.reader(f, delimiter='\t')
                for item in delimited:
                    utctimestamp = (datetime.datetime.fromtimestamp(int(item[0])/1000).strftime('%Y-%m-%d %H:%M:%S'))
                    user = item[1]
                    user_other = item[2]
                    info_one = item[3]
                    info_two = item[4]
                    timestamp = item[5]
                    thumb = ''
                    
                    data_list.append((utctimestamp, timestamp, user, user_other, info_one, info_two))
                    #info_two says REDACTED in my data set. Might be some data in other returns. Leaving code for content available in case sample data comes up. If so if REDACTED else content.
                    '''
                    for match in files_found:
                        if contentID in match:
                            shutil.copy2(match, report_folder)
                            mimetype = magic.from_file(match, mime = True)
                            
                            if mimetype == 'video/mp4':
                                thumb = f'<video width="320" height="240" controls="controls"><source src="{report_folder}{contentID}" type="video/mp4">Your browser does not support the video tag.</video>'
                            else:
                                thumb = f'<img src="{report_folder}{contentID}" width="300"></img>'
                                
                            data_list.append((utctimestamp, timestamp, user, user_other, app, info, contentID, thumb))
                            break
                    '''    
                        
            if data_list:
                report = ArtifactHtmlReport('Kik - Chat Sent Received')
                report.start_artifact_report(report_folder, 'Kik - Chat Sent Received')
                report.add_script()
                data_headers = ('Timestamp UTC', 'Timestamp', 'User', 'User', 'Info', 'Info')
                report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Content'])
                report.end_artifact_report()
                
                tsvname = f'Kik - Chat Sent Received'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                tlactivity = f'Kik - Chat Sent Received'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Kik Chat Sent Received data available')
                
        if filename.startswith('chat_sent.txt'):
            data_list =[]
            with open(file_found, 'r') as f:
                delimited = csv.reader(f, delimiter='\t')
                for item in delimited:
                    utctimestamp = (datetime.datetime.fromtimestamp(int(item[0])/1000).strftime('%Y-%m-%d %H:%M:%S'))
                    user = item[1]
                    user_other = item[2]
                    info_one = item[3]
                    info_two = item[4]
                    timestamp = item[5]
                    thumb = ''
                    
                    data_list.append((utctimestamp, timestamp, user, user_other, info_one, info_two))
                                        
            if data_list:
                report = ArtifactHtmlReport('Kik - Chat Sent')
                report.start_artifact_report(report_folder, 'Kik - Chat Sent')
                report.add_script()
                data_headers = ('Timestamp UTC', 'Timestamp', 'User', 'User', 'Info', 'IP')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Kik - Chat Sent'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                tlactivity = f'Kik - Chat Sent'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Kik Chat Sent data available')
                
        if filename.endswith('abuse'):
            if filename.startswith('.'):
                break
            else:
                data_list =[]
                aggregator = ''
                with open(file_found, 'r') as f:
                    for line in f:
                        if line.startswith('-------Report'):
                            if aggregator != '':
                                data_list.append((timestamp, reportFrom, aggregator))
                                aggregator = ''
                            line = line.split(' ')
                            reportFrom = line[2]
                            timestamp = line[4].strip('(')
                            timestamp = timestamp + ' ' + line[5]
                        else:
                            aggregator = aggregator  + line + '<br>'
                    data_list.append((timestamp, reportFrom, aggregator))
                if data_list:
                    report = ArtifactHtmlReport('Kik - Abuse Report')
                    report.start_artifact_report(report_folder, 'Kik - Abuse Report')
                    report.add_script()
                    data_headers = ('Timestamp', 'Report From', 'Data')
                    report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Data'])
                    report.end_artifact_report()
                    
                    tsvname = f'Kik - Abuse Report'
                    tsv(report_folder, data_headers, data_list, tsvname)
                    
                    tlactivity = f'Kik - Abuse Report'
                    timeline(report_folder, tlactivity, data_list, data_headers)
                else:
                    logfunc('No Kik Abuse Report data available')
                    
        if filename.startswith('friend_added.txt'):
            data_list =[]
            with open(file_found, 'r') as f:
                delimited = csv.reader(f, delimiter='\t')
                for item in delimited:
                    utctimestamp = (datetime.datetime.fromtimestamp(int(item[0])/1000).strftime('%Y-%m-%d %H:%M:%S'))
                    user = item[1]
                    user_other = item[2]
                    timestamp = item[3]
                    
                    data_list.append((utctimestamp, timestamp, user, user_other))
                    
            if data_list:
                report = ArtifactHtmlReport('Kik - Friend Added')
                report.start_artifact_report(report_folder, 'Kik - Friend Added')
                report.add_script()
                data_headers = ('Timestamp UTC', 'Timestamp', 'User', 'User')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Kik - Friend Added'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                tlactivity = f'Kik - Friend Added'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Kik Friend Added data available')
                
        if filename.startswith('group_receive_msg_platform.txt'):
            data_list =[]
            with open(file_found, 'r') as f:
                delimited = csv.reader(f, delimiter='\t')
                for item in delimited:
                    utctimestamp = (datetime.datetime.fromtimestamp(int(item[0])/1000).strftime('%Y-%m-%d %H:%M:%S'))
                    user = item[1]
                    field = item[2]
                    user_other = item[3]
                    appid = item[4]
                    contentID = item[5]
                    info = item[6]
                    timestamp = item[7]
                    thumb = ''
                    for match in files_found:
                        if contentID in match:
                            shutil.copy2(match, report_folder)
                            mimetype = magic.from_file(match, mime = True)
                            
                            if mimetype == 'video/mp4':
                                thumb = f'<video width="320" height="240" controls="controls"><source src="{report_folder}{contentID}" type="video/mp4">Your browser does not support the video tag.</video>'
                            else:
                                thumb = f'<img src="{report_folder}{contentID}" width="300"></img>'
                                
                            data_list.append((utctimestamp, timestamp, user, field, user_other, appid, info, contentID, thumb))
                            break
            if data_list:
                report = ArtifactHtmlReport('Kik - Group Receive Msg Platform')
                report.start_artifact_report(report_folder, 'Kik  - Group Receive Msg Platform')
                report.add_script()
                data_headers = ('Timestamp UTC', 'Timestamp', 'User', 'Field', 'User', 'App', 'Info', 'Content ID', 'Content')
                report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Content'])
                report.end_artifact_report()
                
                tsvname = f'Kik - Group Receive Msg Platform'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                tlactivity = f'Kik - Group Receive Msg Platform'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Kik Group Receive Msg Platform data available')
                
        if filename.startswith('group_receive_msg.txt'):
            data_list =[]
            with open(file_found, 'r') as f:
                delimited = csv.reader(f, delimiter='\t')
                for item in delimited:
                    utctimestamp = (datetime.datetime.fromtimestamp(int(item[0])/1000).strftime('%Y-%m-%d %H:%M:%S'))
                    user = item[1]
                    value = item[2]
                    user_other = item[3]
                    info_one = item[4]
                    info_two = item[5]
                    timestamp = item[6]
                    thumb = ''
                    
                    data_list.append((utctimestamp, timestamp, user, value, user_other, info_one, info_two))
                    
            if data_list:
                report = ArtifactHtmlReport('Kik - Group Receive Msg')
                report.start_artifact_report(report_folder, 'Kik - Group Receive Msg')
                report.add_script()
                data_headers = ('Timestamp UTC', 'Timestamp', 'User', 'Value', 'User', 'Info', 'Info')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Kik - Group Receive Msg'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                tlactivity = f'Kik - Group Receive Msg'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Kik Group Receive Msg data available')
                
        if filename.startswith('group_send_msg_platform.txt'):
            
            data_list =[]
            with open(file_found, 'r') as f:
                delimited = csv.reader(f, delimiter='\t')
                for item in delimited:
                    utctimestamp = (datetime.datetime.fromtimestamp(int(item[0])/1000).strftime('%Y-%m-%d %H:%M:%S'))
                    user = item[1]
                    field = item[2]
                    user_other = item[3]
                    appid = item[4]
                    contentID = item[5]
                    info = item[6]
                    timestamp = item[7]
                    thumb = ''
                    for match in files_found:
                        if contentID in match:
                            shutil.copy2(match, report_folder)
                            mimetype = magic.from_file(match, mime = True)
                            
                            if mimetype == 'video/mp4':
                                thumb = f'<video width="320" height="240" controls="controls"><source src="{report_folder}{contentID}" type="video/mp4">Your browser does not support the video tag.</video>'
                            else:
                                thumb = f'<img src="{report_folder}{contentID}" width="300"></img>'
                                
                            data_list.append((utctimestamp, timestamp, user, field, user_other, appid, info, contentID, thumb))
                            break
            if data_list:
                report = ArtifactHtmlReport('Kik - Group Send Msg Platform')
                report.start_artifact_report(report_folder, 'Kik - Group Send Msg Platform')
                report.add_script()
                data_headers = ('Timestamp UTC', 'Timestamp', 'User', 'Field', 'User', 'App', 'IP', 'Content ID', 'Content')
                report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Content'])
                report.end_artifact_report()
                
                tsvname = f'Kik - Group Send Msg Platform'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                tlactivity = f'Kik - Group Send Msg Platform'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Kik Group Send Msg Platform data available')
                
        if filename.startswith('group_send_msg.txt'):
            
            data_list =[]
            with open(file_found, 'r') as f:
                delimited = csv.reader(f, delimiter='\t')
                for item in delimited:
                    utctimestamp = (datetime.datetime.fromtimestamp(int(item[0])/1000).strftime('%Y-%m-%d %H:%M:%S'))
                    user = item[1]
                    field = item[2]
                    user_other = item[3]
                    info_one = item[4]
                    ip = item[6]
                    timestamp = item[6]
                    
                    data_list.append((utctimestamp, timestamp, user, field, user_other,info_one, ip))
                            
            if data_list:
                report = ArtifactHtmlReport('Kik - Group Send Msg')
                report.start_artifact_report(report_folder, 'Kik - Group Send Msg')
                report.add_script()
                data_headers = ('Timestamp UTC', 'Timestamp', 'User', 'Field', 'User', 'Field', 'IP')
                report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Content'])
                report.end_artifact_report()
                
                tsvname = f'Kik - Group Send Msg'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                tlactivity = f'Kik - Group Send Msg'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Kik Group Send Msg data available')
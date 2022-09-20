import os
import datetime
import csv
import calendar

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html, kmlgen

def monthletter(month):
    monthdict = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    return monthdict[month]

def get_snapchatConv(files_found, report_folder, seeker, wrap_text):

    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        one = (os.path.split(file_found))
        username = (os.path.basename(one[0]))
        
        if filename.startswith('geo_locations.csv'):
            data_list_geo =[]
            with open(file_found, 'r', errors='backslashreplace') as f:
                for line in f:
                    if '=' in line:
                        break
                for line in f:
                    delimited = csv.reader(f, delimiter=',')
                    for item in delimited:
                        latitude = item[0].split(' ')
                        latitudemeters = latitude[2]
                        latitude = latitude[0]
                        
                        longitude = item[1].split(' ')
                        longitudemeters = longitude[2]
                        longitude = longitude[0]
                        
                        fecha = item[2]
                        timestamp = fecha.split(' ')
                        year = timestamp[5]
                        day = timestamp[2]
                        time = timestamp[3]
                        month = monthletter(timestamp[1])
                        timestampfinal = (f'{year}-{month}-{day} {time}')
                        
                        data_list_geo.append((timestampfinal, latitude, latitudemeters, longitude, longitudemeters))
    
            if data_list_geo:
                report = ArtifactHtmlReport(f'Snapchat - Geolocations')
                report.start_artifact_report(report_folder, f'Snapchat - Geolocations - {username}')
                report.add_script()
                data_headers = ('Timestamp','Latitude','Latitude +- Meters','Longitude','Longitude +- Meters')
                report.write_artifact_data_table(data_headers, data_list_geo, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Geolocations  - {username}'
                tsv(report_folder, data_headers, data_list_geo, tsvname)
                
                tlactivity = f'Snapchat - Geolocations  - {username}'
                timeline(report_folder, tlactivity, data_list_geo, data_headers)
                
                kmlactivity = f'Snapchat - Geolocations  - {username}'
                kmlgen(report_folder, kmlactivity, data_list_geo, data_headers)
            else:
                logfunc(f'No Snapchat - Geolocations  - {username}')
    
    
    for file_found in files_found:
        file_found = str(file_found)
    
        filename = os.path.basename(file_found)
        one = (os.path.split(file_found))
        username = (os.path.basename(one[0]))
                    
        if filename.startswith('conversations.csv'):
            data_list_conversations = []
            with open(file_found, 'r', errors='backslashreplace') as f:
                for line in f:
                    if '=' in line:
                        next(f)
                        break
                delimited = csv.reader(f, delimiter=',')
                for item in delimited:
                    #print(item)
                    content_type = item[0]
                    message_type = item[1]
                    conversation_id = item[2]
                    message_id = item[3]
                    reply_to_message_id = item[4]
                    conversation_title = item[5]
                    sender_username = item[6]
                    sender_user_id = item[7]
                    recipient_username = item[8]
                    recipient_user_id = item[9]
                    text = item[10]
                    media = item[11]
                    if media == '':
                        agregator = ' '
                    else:
                        if ';' in media:
                            media = media.split(';')
                            agregator = '<table>'
                            counter = 0
                            for x in media:
                                if counter == 0:
                                    agregator = agregator + ('<tr>')
                                thumb = media_to_html(x, files_found, report_folder)
                            
                                counter = counter + 1
                                agregator = agregator + f'<td>{thumb}</td>'
                                #hacer uno que no tenga html
                                if counter == 2:
                                    counter = 0
                                    agregator = agregator + ('</tr>')
                            if counter == 1:
                                agregator = agregator + ('</tr>')
                            agregator = agregator + ('</table><br>')
                        else:
                            agregator = media_to_html(media, files_found, report_folder)
                    is_saved = item[12]
                    is_one_on_one = item[13] 
                    timestamp = item[14]
                    timestamp = timestamp.split(' ')
                    year = timestamp[5]
                    day = timestamp[2]
                    time = timestamp[3]
                    month = monthletter(timestamp[1])
                    timestampfinal = (f'{year}-{month}-{day} {time}')
                    data_list_conversations.append((timestampfinal,sender_username,recipient_username,text,is_saved,content_type,message_type,agregator,is_one_on_one,conversation_title,message_id,reply_to_message_id,sender_user_id,recipient_user_id))
                        
        
            if data_list_conversations:
                report = ArtifactHtmlReport(f'Snapchat - Conversations')
                report.start_artifact_report(report_folder, f'Snapchat - Conversations - {username}')
                report.add_script()
                data_headers = ('Timestamp','Sender Username','Recipient Username','Text','Is Saved','Content Type', 'Message Type','Media','Is One on One','Conversation Title','Message ID','Reply to Message ID','Sender User ID','Recipient User ID')
                report.write_artifact_data_table(data_headers, data_list_conversations, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Conversations - {username}'
                tsv(report_folder, data_headers, data_list_conversations, tsvname)
                
                tlactivity = f'Snapchat - Conversations - {username}'
                timeline(report_folder, tlactivity, data_list_conversations, data_headers)
            else:
                logfunc(f'No Snapchat - Conversations - {username}')
                
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        one = (os.path.split(file_found))
        username = (os.path.basename(one[0]))
        
        
        
        if filename.startswith('chat.csv' or 'chats.csv'):
            data_list_chats =[]
            with open(file_found, 'r', errors='backslashreplace') as f:
                #for i in range(1):
                #    next(f)
                for line in f:
                    delimited = csv.reader(f, delimiter=',')
                    for item in delimited:
                        #print(item)
                        #chatsid,from,to,body,href,media_id,saved,timestamp
                        chatsid = item[1]
                        fromc = item[2]
                        to = item[3]
                        body = item[4]
                        href = item[5]
                        media = item[6]
                        saved = item[7]
                        timestamp = item[8]
                        if media == '':
                            agregator = ' '
                        else:
                            if ';' in media:
                                media = media.split(';')
                                agregator = '<table>'
                                counter = 0
                                for x in media:
                                    if counter == 0:
                                        agregator = agregator + ('<tr>')
                                    thumb = media_to_html(x, files_found, report_folder)        
                                    
                                    counter = counter + 1
                                    agregator = agregator + f'<td>{thumb}</td>'
                                    #hacer uno que no tenga html
                                    if counter == 2:
                                        counter = 0
                                        agregator = agregator + ('</tr>')
                                if counter == 1:
                                    agregator = agregator + ('</tr>')
                                agregator = agregator + ('</table><br>')
                            else:
                                agregator = media_to_html(media, files_found, report_folder)
            
                        timestamp = timestamp.split(' ')
                        year = timestamp[5]
                        day = timestamp[2]
                        time = timestamp[3]
                        month = monthletter(timestamp[1])
                        timestampfinal = (f'{year}-{month}-{day} {time}')
                        data_list_chats.append((timestampfinal,fromc,to,body,href,saved,agregator,))
                        
                        
            if data_list_chats:
                report = ArtifactHtmlReport(f'Snapchat - Chats')
                report.start_artifact_report(report_folder, f'Snapchat - Chats - {username}')
                report.add_script()
                data_headers = ('Timestamp','Sender Username','Recipient Username','Body','HREF','Is Saved','Media')
                report.write_artifact_data_table(data_headers, data_list_chats, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Chats - {username}'
                tsv(report_folder, data_headers, data_list_chats, tsvname)
                
                tlactivity = f'Snapchat - Chats - {username}'
                timeline(report_folder, tlactivity, data_list_chats, data_headers)
            else:
                logfunc(f'No Snapchat - Chats - {username}')
            
    
            
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        one = (os.path.split(file_found))
        username = (os.path.basename(one[0]))
        
        if filename.startswith('ip_data.csv'):
            data_list_ip =[]
            with open(file_found, 'r', errors='backslashreplace') as f:
                for line in f:
                    if 'ip,action,timestamp,user_agent,status,verification_method' in line:
                        header = line #f.readline()
                        numberofcolumns = header.count(',')+1
                        break
                delimited = csv.reader(f, delimiter=',')
                if numberofcolumns == 6:
                    for item in delimited:
                        ip = item[0]
                        type = item[1]
                        fecha = item[2]
                        useragent = item[3]
                        status = item[4]
                        vermethod = item[5]
                        timestamp = fecha.split(' ')
                        year = timestamp[5]
                        day = timestamp[2]
                        time = timestamp[3]
                        month = monthletter(timestamp[1])
                        timestampfinal = (f'{year}-{month}-{day} {time}')
                        
                        data_list_ip.append((timestampfinal, ip, type, useragent, status, vermethod))
                else:
                    print(delimited)
                    for item in delimited:
                        print(item)
                        ip = item[0]
                        type = item[1]
                        fecha = item[2]
                        timestamp = fecha.split(' ')
                        year = timestamp[5]
                        day = timestamp[2]
                        time = timestamp[3]
                        month = monthletter(timestamp[1])
                        timestampfinal = (f'{year}-{month}-{day} {time}')
                        
                        data_list_ip.append((timestampfinal, ip, type))
                        
            if data_list_ip:
                report = ArtifactHtmlReport(f'Snapchat - IP Data')
                report.start_artifact_report(report_folder, f'Snapchat - IP Data - {username}')
                report.add_script()
                if numberofcolumns == 6:
                    data_headers = ('Timestamp','IP','Type','User Agent','Status','Verification Method')
                else:
                    data_headers = ('Timestamp','IP','Type')
                report.write_artifact_data_table(data_headers, data_list_ip, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - IP Data  - {username}'
                tsv(report_folder, data_headers, data_list_ip, tsvname)
                
                tlactivity = f'Snapchat - IP Data  - {username}'
                timeline(report_folder, tlactivity, data_list_ip, data_headers)
                
            else:
                logfunc(f'No Snapchat - IP Data  - {username}')

    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        one = (os.path.split(file_found))
        username = (os.path.basename(one[0]))
        
        if filename.startswith('friends.csv'):
            data_list_friendscsv =[]
            with open(file_found, 'r') as f:
                for line in f:
                    if '=' in line:
                        next(f)
                        break
                for line in f:
                    delimited = csv.reader(f, delimiter=',')
                    for item in delimited:
                        idf = item[0]
                        adder = item[1]
                        added = item[2]
                        types = item[3]
                        modat = item[4]
                        created = item[5]
                        
                        timestamp = created.split(' ')
                        year = timestamp[5]
                        day = timestamp[2]
                        time = timestamp[3]
                        month = monthletter(timestamp[1])
                        timestampcreated = (f'{year}-{month}-{day} {time}')
                        
                        timestamp = modat.split(' ')
                        year = timestamp[5]
                        day = timestamp[2]
                        time = timestamp[3]
                        month = monthletter(timestamp[1])
                        timestampmodat = (f'{year}-{month}-{day} {time}')
                        
                        
                        data_list_friendscsv.append((timestampcreated,timestampmodat, adder,added, types, idf))
                        
            if data_list_ip:
                report = ArtifactHtmlReport(f'Snapchat - Friends.csv')
                report.start_artifact_report(report_folder, f'Snapchat - Friends.csv - {username}')
                report.add_script()
                data_headers = ('Timestamp Created','Timestamps Modified At','Adder','Added','Type','ID')
                report.write_artifact_data_table(data_headers, data_list_friendscsv, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Friends.csv - {username}'
                tsv(report_folder, data_headers, data_list_friendscsv, tsvname)
                
                tlactivity = f'Snapchat - Friends.csv  - {username}'
                timeline(report_folder, tlactivity, data_list_friendscsv, data_headers)
                
            else:
                logfunc(f'No Snapchat - Friends.csv  - {username}')
                
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        one = (os.path.split(file_found))
        username = (os.path.basename(one[0]))
        
        if filename.startswith('friends_list.csv'):
            data_list_friendlist =[]
            with open(file_found, 'r') as f:
                for i in range(3):
                    next(f)
                for line in f:
                    delimited = csv.reader(f, delimiter=',')
                    for item in delimited:
                        friend = item[0]
                        
                        
                        data_list_friendlist.append((friend,))
                        
            if data_list_ip:
                report = ArtifactHtmlReport(f'Snapchat - Friends_list.csv')
                report.start_artifact_report(report_folder, f'Snapchat - Friends_list.csv - {username}')
                report.add_script()
                data_headers = ('Friend Username',)
                report.write_artifact_data_table(data_headers, data_list_friendlist , file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Friends_list.csv - {username}'
                tsv(report_folder, data_headers, data_list_friendlist , tsvname)
                
            else:
                logfunc(f'No Snapchat - Friends_list.csv  - {username}')
                
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        one = (os.path.split(file_found))
        username = (os.path.basename(one[0]))
        
        if filename.startswith('group-chat.csv'):
            data_list_groupchats =[]
            with open(file_found, 'r', errors='backslashreplace') as f:
                for i in range(3):
                    next(f)
                for line in f:
                    delimited = csv.reader(f, delimiter=',')
                    for item in delimited:
                        #print(item)
                        #message_type,from,to_group_id,to_group_name,text,href,media_id,timestamp
                        mtype = item[0]
                        fromn = item[1]
                        togroupid = item[2]
                        togroupname = item[3]
                        text = item[4]
                        href = item[5]
                        media = item[6]
                        timestamp = item[7]
                        if media == '':
                            agregator = ' '
                        else:
                            if ';' in media:
                                media = media.split(';')
                                agregator = '<table>'
                                counter = 0
                                for x in media:
                                    if counter == 0:
                                        agregator = agregator + ('<tr>')
                                    thumb = media_to_html(x, files_found, report_folder)        
                                    
                                    counter = counter + 1
                                    agregator = agregator + f'<td>{thumb}</td>'
                                    #hacer uno que no tenga html
                                    if counter == 2:
                                        counter = 0
                                        agregator = agregator + ('</tr>')
                                if counter == 1:
                                    agregator = agregator + ('</tr>')
                                agregator = agregator + ('</table><br>')
                            else:
                                agregator = media_to_html(media, files_found, report_folder)
                                
                        timestamp = timestamp.split(' ')
                        year = timestamp[5]
                        day = timestamp[2]
                        time = timestamp[3]
                        month = monthletter(timestamp[1])
                        timestampfinal = (f'{year}-{month}-{day} {time}')
                        data_list_groupchats.append((timestampfinal,fromn,togroupname,text,href,agregator,togroupid,mtype))
                        
                        
            if data_list_groupchats:
                report = ArtifactHtmlReport(f'Snapchat - Group-chat.csv')
                report.start_artifact_report(report_folder, f'Snapchat - Group-chat.csv - {username}')
                report.add_script()
                data_headers = ('Timestamp','From','To Group Name','Text','HREF','Media','To Group ID','Type')
                report.write_artifact_data_table(data_headers, data_list_groupchats, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Group-chat.csv - {username}'
                tsv(report_folder, data_headers, data_list_groupchats, tsvname)
                
                tlactivity = f'Snapchat - Group-chat.csv - {username}'
                timeline(report_folder, tlactivity, data_list_groupchats, data_headers)
            else:
                logfunc(f'No Snapchat - Group-chat.csv - {username}')

__artifacts__ = {
        "snapchatConv": (
            "Snapchat Returns",
            ('*/conversations.csv', '*/*.*'),
            get_snapchatConv)
}
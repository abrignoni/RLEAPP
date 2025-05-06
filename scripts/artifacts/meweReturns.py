__artifacts_v2__ = {
    "meweContacts": {
        "name": "MeWe Contacts",
        "description": "This parses the Contacts list from a MeWe warrant return.",
        "author": "Troy Schnack (@TheBaldJedi)",
        "version": "1.0.1",
        "date": "2024-05-13",
        "requirements": "",
        "category": "MeWe",
        "paths": (
            '**/mewe-content/contacts.txt'),
        "function": "get_meweContacts"
    },
    "meweDevices": {
        "name": "MeWe Devices",
        "description": "This parses the Device list from a MeWe warrant return.",
        "author": "Troy Schnack (@TheBaldJedi)",
        "version": "1.0.1",
        "date": "2024-05-13",
        "requirements": "",
        "category": "MeWe",
        "paths": (
            '**/mewe-content/devices.txt'),
        "function": "get_meweDevices"
    },
    "meweEmails": {
        "name": "MeWe Email Accounts",
        "description": "This parses the Email account list from a MeWe warrant return.",
        "author": "Troy Schnack (@TheBaldJedi)",
        "version": "1.0.1",
        "date": "2024-05-13",
        "requirements": "",
        "category": "MeWe",
        "paths": (
            '**/mewe-content/emails.txt'),
        "function": "get_meweEmails"
    },
    "meweGroupmemberships": {
        "name": "MeWe Group Memberships",
        "description": "This parses the Group Membership list from a MeWe warrant return.",
        "author": "Troy Schnack (@TheBaldJedi)",
        "version": "1.0.1",
        "date": "2024-05-13",
        "requirements": "",
        "category": "MeWe",
        "paths": (
            '**/mewe-content/group-memberships.txt'),
        "function": "get_meweGroupmemberships"
    },
    "meweProfile": {
        "name": "MeWe Profile",
        "description": "This parses the User Profile from a MeWe warrant return.",
        "author": "Troy Schnack (@TheBaldJedi)",
        "version": "1.1.0",
        "date": "2024-05-15",
        "requirements": "",
        "category": "MeWe",
        "paths": (
            '**/mewe-content/profile.txt','**/mewe-content/photos/*.jpg'),
        "function": "get_meweProfile"
    },
    "meweGroupChat": {
        "name": "MeWe Group Chat",
        "description": "This parses the Group Chat Posts from a MeWe warrant return.",
        "author": "Troy Schnack (@TheBaldJedi)",
        "version": "1.0.1",
        "date": "2024-05-15",
        "requirements": "",
        "category": "MeWe",
        "paths": (
            '**/mewe-content/groupChat.txt','**/mewe-content/photos/*.jpg'),
        "function": "get_meweGroupChat"
    },
    "mewePosts": {
        "name": "MeWe Posts",
        "description": "This parses the Posts from a MeWe warrant return.",
        "author": "Troy Schnack (@TheBaldJedi)",
        "version": "1.0.1",
        "date": "2024-05-15",
        "requirements": "",
        "category": "MeWe",
        "paths": (
            '**/mewe-content/posts.txt','**/mewe-content/photos/*.jpg'),
        "function": "get_mewePosts"
    },
    "meweUserChat": {
        "name": "MeWe Posts",
        "description": "This parses the User Chat Posts from a MeWe warrant return.",
        "author": "Troy Schnack (@TheBaldJedi)",
        "version": "1.2.0",
        "date": "2024-05-16",
        "requirements": "",
        "category": "MeWe",
        "paths": (
            '**/mewe-content/userChat.txt','**/mewe-content/photos/*.jpg','**mewe-content/documents/**'),
        "function": "get_meweUserChat"
    },
    "meweLoginStats": {
        "name": "MeWe Login Stats",
        "description": "This parses the User Login Stats from a MeWe warrant return.",
        "author": "Troy Schnack (@TheBaldJedi)",
        "version": "1.0.1",
        "date": "2024-05-16",
        "requirements": "",
        "category": "MeWe",
        "paths": (
            '**/mewe-content/logins/stats.txt'),
        "function": "get_meweLoginStats"
    },
    "meweLoginLogs": {
        "name": "MeWe Login Logs",
        "description": "This parses the User Login Logs from a MeWe warrant return.",
        "author": "Troy Schnack (@TheBaldJedi)",
        "version": "1.0.1",
        "date": "2024-05-16",
        "requirements": "",
        "category": "MeWe",
        "paths": (
            '**/mewe-content/logins/logs.txt'),
        "function": "get_meweLoginLogs"
    }
}


import os
import csv
import datetime

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, media_to_html


def get_meweLoginLogs(files_found, report_folder, seeker, wrap_text):


    for file_found in files_found:
        file_found = str(file_found)
    
        filename = os.path.basename(file_found)
        csvname = filename
        
        if file_found.endswith('.txt'):
            
            data_list_dm =[]
            
            with open(file_found, encoding = 'utf-8', mode = 'r', errors='backslashreplace') as f:
                delimited = csv.reader(f, delimiter=',')
                for item in delimited:
                    dateCreated = item[0].lstrip('date: ')
                    dateCreated = datetime.datetime.fromisoformat(dateCreated)
                    ipAddress = item[1].lstrip('ip: ')
                                                
                    data_list_dm.append((dateCreated,ipAddress))
        
            if data_list_dm:
                report = ArtifactHtmlReport(f'MeWe - Login Logs ')
                report.start_artifact_report(report_folder, f'MeWe - Logins Logs - {csvname}')
                report.add_script()
                data_headers = ('Login Date','IP Address')
                report.write_artifact_data_table(data_headers, data_list_dm, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'MeWe - Logins Logs - {csvname}'
                tsv(report_folder, data_headers, data_list_dm, tsvname)

                tlactivity = f'MeWe - Logins Logs'
                timeline(report_folder, tlactivity, data_list_dm, data_headers)

                
            else:
                logfunc(f'No MeWe - Logins Logs - {csvname}')


def get_meweLoginStats(files_found, report_folder, seeker, wrap_text):


    for file_found in files_found:
        file_found = str(file_found)
    
        filename = os.path.basename(file_found)
        csvname = filename
        
        if file_found.endswith('.txt'):
            
            data_list_dm =[]
            
            with open(file_found, encoding = 'utf-8', mode = 'r', errors='backslashreplace') as f:
                delimited = csv.reader(f, delimiter=',')
                for item in delimited:
                    ipAddress = item[0].lstrip('ip: ')
                    totalCount = item[1].lstrip('totalCount: ')
                                                
                    data_list_dm.append((ipAddress,totalCount))
                        
        
            if data_list_dm:
                report = ArtifactHtmlReport(f'MeWe - Login Stats ')
                report.start_artifact_report(report_folder, f'MeWe - Logins Stats - {csvname}')
                report.add_script()
                data_headers = ('IP Adress','Total Logins From IP')
                report.write_artifact_data_table(data_headers, data_list_dm, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'MeWe - Logins Stats - {csvname}'
                tsv(report_folder, data_headers, data_list_dm, tsvname)
               
            else:
                logfunc(f'No MeWe - Logins Stats - {csvname}')


def get_meweUserChat(files_found, report_folder, seeker, wrap_text):


    for file_found in files_found:
        file_found = str(file_found)
    
        filename = os.path.basename(file_found)
        csvname = filename
        folderPath = os.path.dirname(file_found)
        
        ''' Define subfolder paths for photos and other file types.'''
        ''' Example: mp4's are stored in the documents folder.'''
        photoPath = folderPath + '/photos'
        attachPath = folderPath + '/documents'
        
        
        if file_found.endswith('.txt'):
            
            with open(file_found, encoding = 'utf-8', mode = 'r', errors='backslashreplace') as f:
                data = f.readlines()
                
                data_list_dm =[]
                dateCreated = chatText = senderID = threadID = chatType = recipientID = documentID = imageID = thumb = ''
    
                for line in data:
                    
                    if 'date_created:' in line:
                        dateCreated = line.split(': ')[1].strip()
                        dateCreated = datetime.datetime.fromisoformat(dateCreated)
                    elif 'text:' in line:
                        chatText = line.split(': ')[1].strip()
                    elif 'sender_id:' in line:
                        senderID = line.split(': ')[1].strip()
                    elif 'threadId:' in line:
                        threadID = line.split(': ')[1].strip()
                    elif 'chatThreadType:' in line:
                        chatType = line.split(': ')[1].strip()
                    elif 'recipientUsersId' in line:
                        recipientID = line.split(': ')[1].strip()
                    elif 'document_id:' in line:
                        documentID = line.split(': ')[1].strip()
                        thumb = media_to_html(documentID,files_found,report_folder)
                    elif 'image_id:' in line:
                        imageID = line.split(': ')[1].strip()
                        thumb = media_to_html(imageID,files_found,report_folder)
                    elif '---------------' in line:
                        data_list_dm.append((dateCreated,chatText,senderID,threadID,chatType,recipientID,documentID,imageID,thumb))
                        dateCreated = chatText = senderID = threadID = chatType = recipientID = documentID = imageID = thumb = ''
                        
        
            if data_list_dm:
                report = ArtifactHtmlReport(f'MeWe - User Chat ')
                report.start_artifact_report(report_folder, f'MeWe - User Chat - {csvname}')
                report.add_script()
                data_headers = ('Created Date','Text','Sender ID','Thread ID','Chat Type','Recipient ID','Attached Filename','Photo Filename','Media')
                report.write_artifact_data_table(data_headers, data_list_dm, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'MeWe - User Chat - {csvname}'
                tsv(report_folder, data_headers, data_list_dm, tsvname)

                tlactivity = f'MeWe - User Chat'
                timeline(report_folder, tlactivity, data_list_dm, data_headers)
                
            else:
                logfunc(f'No MeWe - User Chat - {csvname}')


def get_mewePosts(files_found, report_folder, seeker, wrap_text):


    for file_found in files_found:
        file_found = str(file_found)
    
        filename = os.path.basename(file_found)
        csvname = filename
        
        if file_found.endswith('.txt'):
            
            with open(file_found, encoding = 'utf-8', mode = 'r', errors='backslashreplace') as f:
                data = f.readlines()
                
                data_list_dm =[]
                dateCreated = chatText = imageID = thumb = ''
    
                for line in data:
                    
                    if 'date_created:' in line:
                        dateCreated = line.split(': ')[1].strip()
                        dateCreated = datetime.datetime.fromisoformat(dateCreated)
                    elif 'text:' in line:
                        chatText = line.split(': ')[1].strip()
                    elif 'image_id:' in line:
                        imageID = line.split(': ')[1].strip()
                        thumb = media_to_html(imageID,files_found,report_folder)
                    elif '---------------' in line:
                        data_list_dm.append((dateCreated,chatText,imageID,thumb))
                        dateCreated = chatText = imageID = thumb = ''
                        
        
            if data_list_dm:
                report = ArtifactHtmlReport(f'MeWe - Posts ')
                report.start_artifact_report(report_folder, f'MeWe - Posts - {csvname}')
                report.add_script()
                data_headers = ('Created Date','Text','Image ID','Media')
                report.write_artifact_data_table(data_headers, data_list_dm, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'MeWe - Posts - {csvname}'
                tsv(report_folder, data_headers, data_list_dm, tsvname)

                tlactivity = f'MeWe - Posts'
                timeline(report_folder, tlactivity, data_list_dm, data_headers)
                
            else:
                logfunc(f'No MeWe - Posts - {csvname}')


def get_meweGroupChat(files_found, report_folder, seeker, wrap_text):


    for file_found in files_found:
        file_found = str(file_found)
    
        filename = os.path.basename(file_found)
        csvname = filename
        
        if file_found.endswith('.txt'):
            
            with open(file_found, encoding = 'utf-8', mode = 'r', errors='backslashreplace') as f:
                data = f.readlines()
                
                data_list_dm =[]
                dateCreated = chatID = chatText = senderID = threadID = chatType = imageID = thumb = ''
    
                for line in data:
                    
                    if 'date_created' in line:
                        dateCreated = line.split(': ')[1].strip()
                        dateCreated = datetime.datetime.fromisoformat(dateCreated)
                    elif 'text:' in line:
                        chatText = line.split(': ')[1].strip()
                    elif 'sender_id:' in line:
                        senderID = line.split(': ')[1].strip()
                    elif 'threadId' in line:
                        threadID = line.split(': ')[1].strip()
                    elif 'chatThreadType' in line:
                        chatType = line.split(': ')[1].strip()
                    elif 'image_id:' in line:
                        imageID = line.split(': ')[1].strip()
                        thumb = media_to_html(imageID,files_found,report_folder)

                    elif '---------------' in line:
                        data_list_dm.append((dateCreated,chatText,senderID,threadID,chatType,imageID,thumb))
                        dateCreated = chatID = chatText = senderID = threadID = chatType = imageID = thumb = ''
                        
        
            if data_list_dm:
                report = ArtifactHtmlReport(f'MeWe - Group Chat ')
                report.start_artifact_report(report_folder, f'MeWe - Group Chat - {csvname}')
                report.add_script()
                data_headers = ('Created Date','Text','Sender ID','Thread ID','Chat Type','Image ID','Media')
                report.write_artifact_data_table(data_headers, data_list_dm, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'MeWe - Group Chat - {csvname}'
                tsv(report_folder, data_headers, data_list_dm, tsvname)

                tlactivity = f'MeWe - Group Chat'
                timeline(report_folder, tlactivity, data_list_dm, data_headers)
                
            else:
                logfunc(f'No MeWe - Group Chat - {csvname}')


def get_meweProfile(files_found, report_folder, seeker, wrap_text):


    for file_found in files_found:
        file_found = str(file_found)
    
        filename = os.path.basename(file_found)
        csvname = filename
        
        if file_found.endswith('.txt'):
            
            with open(file_found, encoding = 'utf-8', mode = 'r', errors='backslashreplace') as f:
                data = f.readlines()
                
                data_list_dm =[]
                userid = dateRegistered = firstName = lastName = email = lastSeen = timeZone = profileText = isBanned = urlPage = coverImage = profileImage = profileThumb = coverThumb =''
    
                for line in data:
                    
                    if 'user_id:' in line:
                        userid = line.split(': ')[1].strip()
                    elif 'date_registered:' in line:
                        dateRegistered = line.split(': ')[1].strip()
                        dateRegistered = datetime.datetime.fromisoformat(dateRegistered)
                    elif 'first_name' in line:
                        firstName = line.split(': ')[1].strip()
                    elif 'last_name' in line:
                        lastName = line.split(': ')[1].strip()
                    elif 'email' in line:
                        email = line.split(': ')[1].strip()
                    elif 'last_seen_login' in line:
                        lastSeen = line.split(': ')[1].strip()
                        lastSeen = datetime.datetime.fromisoformat(lastSeen)
                    elif 'registration_time_zone' in line:
                        timeZone = line.split(': ')[1].strip()
                    elif 'profile_text' in line:
                        profileText = line.split(': ')[1].strip()
                    elif 'is_banned' in line:
                        isBanned = line.split(': ')[1].strip()
                    elif 'url' in line:
                        urlPage = line.split(': ')[1].strip()
                    elif 'cover_image' in line:
                        coverImage = line.split(': ')[1].strip()
                        coverThumb = media_to_html(coverImage,files_found,report_folder)
                    elif 'profile_image' in line:
                        profileImage = line.split(': ')[1].strip()
                        profileThumb = media_to_html(profileImage,files_found,report_folder)
                    elif '---------------' in line:
                        data_list_dm.append((userid,dateRegistered,firstName,lastName,email,lastSeen,timeZone,profileText,isBanned,urlPage,coverImage,coverThumb,profileImage,profileThumb))
                        userid = dateRegistered = firstName = lastName = email = lastSeen = timeZone = profileText = isBanned = urlPage = coverImage = profileImage = profileThumb = coverThumb =''
                        
        
            if data_list_dm:
                report = ArtifactHtmlReport(f'MeWe - Profile ')
                report.start_artifact_report(report_folder, f'MeWe - Profile - {csvname}')
                report.add_script()
                data_headers = ('User ID','Date Registered','First Name','Last Name','Email','Last Seen','Registration TimeZone','Profile Text','Is Banned','MeWe URL','Cover Filename','Cover Media','Profile Filename','Profile Media')
                report.write_artifact_data_table(data_headers, data_list_dm, file_found, html_no_escape=['Cover Media','Profile Media'])
                report.end_artifact_report()
                
                tsvname = f'MeWe - Profile - {csvname}'
                tsv(report_folder, data_headers, data_list_dm, tsvname)
                
            else:
                logfunc(f'No MeWe - Profile - {csvname}')


def get_meweGroupmemberships(files_found, report_folder, seeker, wrap_text):


    for file_found in files_found:
        file_found = str(file_found)
    
        filename = os.path.basename(file_found)
        csvname = filename
        
        if file_found.endswith('.txt'):
            data_list_dm =[]
            with open(file_found, encoding = 'utf-8', mode = 'r', errors='backslashreplace') as f:
                delimited = csv.reader(f, delimiter=',')
                for item in delimited:
                    groupid = item[0].lstrip('id: ')
                    groupname = item[1].lstrip('name: ')
                                                
                    data_list_dm.append((groupid,groupname))
                        
        
            if data_list_dm:
                report = ArtifactHtmlReport(f'MeWe - Group Membership ')
                report.start_artifact_report(report_folder, f'MeWe - Group Membership - {csvname}')
                report.add_script()
                data_headers = ('Group ID','Group Name')
                report.write_artifact_data_table(data_headers, data_list_dm, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'MeWe - Group Membership - {csvname}'
                tsv(report_folder, data_headers, data_list_dm, tsvname)
                
            else:
                logfunc(f'No MeWe - Group Membership - {csvname}')



def get_meweEmails(files_found, report_folder, seeker, wrap_text):


    for file_found in files_found:
        file_found = str(file_found)
    
        filename = os.path.basename(file_found)
        csvname = filename
        
        if file_found.endswith('.txt'):
            data_list_dm =[]
            with open(file_found, mode = 'r', errors='backslashreplace') as f:
                delimited = csv.reader(f)
                for item in delimited:
                    email = item[0].lstrip('email: ')
                    timestamp = item[1].lstrip('createdAt: ')
                    timestamp = datetime.datetime.fromisoformat(timestamp)

                    data_list_dm.append((timestamp,email))
                        
        
            if data_list_dm:
                report = ArtifactHtmlReport(f'MeWe - Emails ')
                report.start_artifact_report(report_folder, f'MeWe - Emails - {csvname}')
                report.add_script()
                data_headers = ('Created Date','Email Account')
                report.write_artifact_data_table(data_headers, data_list_dm, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'MeWe - Emails - {csvname}'
                tsv(report_folder, data_headers, data_list_dm, tsvname)

            else:
                logfunc(f'No MeWe - Emails - {csvname}')
                


def get_meweDevices(files_found, report_folder, seeker, wrap_text):


    for file_found in files_found:
        file_found = str(file_found)
    
        filename = os.path.basename(file_found)
        csvname = filename
        
        if file_found.endswith('.txt'):
            data_list_dm =[]
            with open(file_found, mode = 'r', errors='backslashreplace') as f:
                delimited = csv.reader(f)
                for item in delimited:
                    deviceid = item[0].lstrip('deviceId: ')
                    vendordeviceid = item[1].lstrip('vendorDeviceID: ')
                    devicetype = item[2].split(': ')[1].strip()
                    timestamp = item[3].split(': ')[1].strip()
                    timestamp = datetime.datetime.fromisoformat(timestamp)
                
                    data_list_dm.append((devicetype,timestamp,deviceid,vendordeviceid))
                        
        
            if data_list_dm:
                report = ArtifactHtmlReport(f'MeWe - Devices ')
                report.start_artifact_report(report_folder, f'MeWe - Devices - {csvname}')
                report.add_script()
                data_headers = ('Device Type','Created Timestamp','Device ID','Vendor Device ID')
                report.write_artifact_data_table(data_headers, data_list_dm, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'MeWe - Devices - {csvname}'
                tsv(report_folder, data_headers, data_list_dm, tsvname)

            else:
                logfunc(f'No MeWe - Devices - {csvname}')
                

def get_meweContacts(files_found, report_folder, seeker, wrap_text):


    for file_found in files_found:
        file_found = str(file_found)
    
        filename = os.path.basename(file_found)
        csvname = filename
        
        if file_found.endswith('.txt'):
            data_list_dm =[]
            with open(file_found, encoding = 'utf-8', mode = 'r', errors='backslashreplace') as f:
                delimited = csv.reader(f, delimiter=',')
                for item in delimited:
                    userid = item[0].lstrip('_id: ')
                    username = item[1].lstrip('contactUserName: ')
                
                    data_list_dm.append((userid,username))
                        
        
            if data_list_dm:
                report = ArtifactHtmlReport(f'MeWe - Contacts ')
                report.start_artifact_report(report_folder, f'MeWe - Contacts - {csvname}')
                report.add_script()
                data_headers = ('User ID','Username')
                report.write_artifact_data_table(data_headers, data_list_dm, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'MeWe - Contacts - {csvname}'
                tsv(report_folder, data_headers, data_list_dm, tsvname)
                
            else:
                logfunc(f'No MeWe - Contacts - {csvname}')
                

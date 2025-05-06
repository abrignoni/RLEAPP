import os
import csv

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html, is_platform_windows, sanitize_file_path

def get_reddit(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        one = (os.path.split(file_found))
        usernamemain = (os.path.basename(one[0]))
        
        two = (os.path.split(one[0]))
        email = (os.path.basename(two[0]))
        email = email.split(' ')[-1].strip()
        
        three = (os.path.split(two[0]))
        records = (os.path.basename(three[0]))
        
        if is_platform_windows:
            email = sanitize_file_path(email)
            usernamemain = sanitize_file_path(usernamemain)
        
        if filename.startswith('chat_history.csv'):
            data_list = [] 
            
            with open(file_found, 'r', encoding='unicode_escape') as csvfile:
                data = csv.reader(csvfile)
                next(data) #Ignore the first line of the csv that contains the header
                for row in data:
                    messageid = (row[0])
                    createdtime = (row[1].replace('UTC', '').strip())
                    updatedattime = (row[2].replace('UTC', '').strip())
                    username = (row[3])
                    message = (row[4])
                    channel = (row[5])
                    subreddit = (row[6])
                    channelname = (row[7])
                    convtype = (row[8])
                    
                    data_list.append((createdtime,updatedattime,username,message,messageid,convtype,channel,channelname,subreddit))
    
                if len(data_list) > 0:
                    report = ArtifactHtmlReport(f'Reddit {records} - Chat History - {usernamemain}, {email}')
                    report.start_artifact_report(report_folder, f'Reddit {records} - Chat History - {usernamemain}, {email}')
                    report.add_script()
                    data_headers = ('Created At', 'Updated At', 'Username', 'Message', 'Message ID', 'Conversation Type', 'Channel', 'Channel Name', 'Subreddit')
                    report.write_artifact_data_table(data_headers, data_list, file_found)
                    report.end_artifact_report()
                    
                    tlactivity = f'Reddit {records} - Chat History - {usernamemain}, {email}'
                    timeline(report_folder, tlactivity, data_list, data_headers)
                else:
                    logfunc(f'No Reddit {records} - Chat History - {usernamemain}, {email}')
            
        if filename.startswith('comment_votes.csv'):
            data_list = [] 
            
            with open(file_found, 'r', encoding='unicode_escape') as csvfile:
                data = csv.reader(csvfile)
                next(data)
                for row in data:
                    id = (row[0])
                    permalink = (row[1])
                    direction = (row[2])
                    
                    data_list.append((id,permalink,direction))
                    
                if len(data_list) > 0:
                    report = ArtifactHtmlReport(f'Reddit {records} - Comment Votes - {usernamemain}, {email}')
                    report.start_artifact_report(report_folder, f'Reddit {records} - Comment Votes - {usernamemain}, {email}')
                    report.add_script()
                    data_headers = ('ID','Permalink','Direction')
                    report.write_artifact_data_table(data_headers, data_list, file_found)
                    report.end_artifact_report()
                    
                    tlactivity = f'Reddit {records} - Comment Votes - {usernamemain}, {email}'
                    timeline(report_folder, tlactivity, data_list, data_headers)
                else:
                    logfunc(f'No Reddit {records} - Comment Votes - {usernamemain}, {email}')

        if filename.startswith('comments.csv'):
            data_list = [] 
            
            with open(file_found, 'r', encoding='unicode_escape') as csvfile:
                data = csv.reader(csvfile)
                next(data) #Ignore the first line of the csv that contains the header
                for row in data:
                    id = (row[0])
                    permalink = (row[1])
                    date = (row[2].replace('UTC', '').strip())
                    ip = (row[3])
                    subreddit = (row[4])
                    gildings = (row[5])
                    link = (row[6])
                    parent = (row[7])
                    body = (row[8])
                    media = (row[9])
                    
                    data_list.append((date,ip,body,permalink,id,subreddit,gildings,link,parent,media))
                    
                if len(data_list) > 0:
                    report = ArtifactHtmlReport(f'Reddit {records} - Comments - {usernamemain}, {email}')
                    report.start_artifact_report(report_folder, f'Reddit {records} - Comments - {usernamemain}, {email}')
                    report.add_script()
                    data_headers = ('Timestamp','IP','Body','Permalink','ID','Subreddit','Gildings','Link','Parent','Media')
                    report.write_artifact_data_table(data_headers, data_list, file_found)
                    report.end_artifact_report()
                    
                    tlactivity = f'Reddit {records} - Comments - {usernamemain}, {email}'
                    timeline(report_folder, tlactivity, data_list, data_headers)
                else:
                    logfunc(f'No Reddit {records} - Comments - {usernamemain}, {email}')
        
        if filename.startswith('drafts.csv'):
            data_list = [] 
            
            with open(file_found, 'r', encoding='unicode_escape') as csvfile:
                data = csv.reader(csvfile)
                next(data) #Ignore the first line of the csv that contains the header
                for row in data:
                    id = (row[0])
                    title = (row[1])
                    body = (row[2])
                    kind = (row[3])
                    created = (row[4].replace('UTC', '').strip())
                    modified = (row[5].replace('UTC', '').strip())
                    spoiler = (row[6])
                    nsfw = (row[7])
                    original_content = (row[8])
                    content_category = (row[9])
                    flair_id = (row[10])
                    flair_text = (row[11])
                    send_replies = (row[12])
                    subreddit = (row[13])
                    is_public_link = (row[14])
                    data_list.append((created,modified,id,title,body,kind,spoiler,nsfw,original_content,content_category,flair_id,flair_text,send_replies,subreddit,is_public_link))
                
                if len(data_list) > 0:
                    report = ArtifactHtmlReport(f'Reddit {records} - Drafts - {usernamemain}, {email}')
                    report.start_artifact_report(report_folder, f'Reddit {records} - Drafts - {usernamemain}, {email}')
                    report.add_script()
                    data_headers = ('Created','Modified','ID','Title','Body','Kind','Spoiler','NSFW','Original Content','Content Category','Flair ID','Flair Text','Send Replies','Subreddit','Is Public Link')
                    report.write_artifact_data_table(data_headers, data_list, file_found)
                    report.end_artifact_report()
                    
                    tlactivity = f'Reddit {records} - Drafts - {usernamemain}, {email}'
                    timeline(report_folder, tlactivity, data_list, data_headers)
                else:
                    logfunc(f'No Reddit {records} - Drafts - {usernamemain}, {email}')    
            
        if filename.startswith('gilded_comments.csv'):
            data_list = [] 
            
            with open(file_found, 'r', encoding='unicode_escape') as csvfile:
                data = csv.reader(csvfile)
                next(data) #Ignore the first line of the csv that contains the header
                for row in data:
                    id = (row[0])
                    permalink = (row[1])
                    award_id = (row[2])
                    quantity = (row[3])
                    
                    data_list.append((id,permalink,award_id,quantity))
                    
                if len(data_list) > 0:
                    report = ArtifactHtmlReport(f'Reddit {records} - Gilded Comments - {usernamemain}, {email}')
                    report.start_artifact_report(report_folder, f'Reddit {records} - Gilded Comments - {usernamemain}, {email}')
                    report.add_script()
                    data_headers = ('ID','Permalink','Award ID','Quantity')
                    report.write_artifact_data_table(data_headers, data_list, file_found)
                    report.end_artifact_report()
                    
                    tlactivity = f'Reddit {records} - Gilded Comments - {usernamemain}, {email}'
                    timeline(report_folder, tlactivity, data_list, data_headers)
                else:
                    logfunc(f'No Reddit {records} - Gilded Comments - {usernamemain}, {email}')
                    
        if filename.startswith('gilded_posts.csv'):
            data_list = [] 
            
            with open(file_found, 'r', encoding='unicode_escape') as csvfile:
                data = csv.reader(csvfile)
                next(data) #Ignore the first line of the csv that contains the header
                for row in data:
                    id = (row[0])
                    permalink = (row[1])
                    award_id = (row[2])
                    quantity = (row[3])
                    
                    data_list.append((id,permalink,award_id,quantity))
                    
                if len(data_list) > 0:
                    report = ArtifactHtmlReport(f'Reddit {records} - Gilded Posts - {usernamemain}, {email}')
                    report.start_artifact_report(report_folder, f'Reddit {records} - Gilded Posts - {usernamemain}, {email}')
                    report.add_script()
                    data_headers = ('ID','Permalink','Award ID','Quantity')
                    report.write_artifact_data_table(data_headers, data_list, file_found)
                    report.end_artifact_report()
                    
                    tlactivity = f'Reddit {records} - Gilded Posts - {usernamemain}, {email}'
                    timeline(report_folder, tlactivity, data_list, data_headers)
                else:
                    logfunc(f'No Reddit {records} - Gilded Posts - {usernamemain}, {email}')
                    
        if filename.startswith('hidden_posts.csv'):
            data_list = [] 
            
            with open(file_found, 'r', encoding='unicode_escape') as csvfile:
                data = csv.reader(csvfile)
                next(data) #Ignore the first line of the csv that contains the header
                for row in data:
                    id = (row[0])
                    permalink = (row[1])
                    
                    data_list.append((id,permalink))
                
                if len(data_list) > 0:
                    report = ArtifactHtmlReport(f'Reddit {records} - Hidden Posts - {usernamemain}, {email}')
                    report.start_artifact_report(report_folder, f'Reddit {records} - Hidden Posts - {usernamemain}, {email}')
                    report.add_script()
                    data_headers = ('ID','Permalink')
                    report.write_artifact_data_table(data_headers, data_list, file_found)
                    report.end_artifact_report()
                    
                    tlactivity = f'Reddit {records} - Hidden Posts - {usernamemain}, {email}'
                    timeline(report_folder, tlactivity, data_list, data_headers)
                else:
                    logfunc(f'No Reddit {records} - Hidden Posts - {usernamemain}, {email}')

        if filename.startswith('ip_logs.csv'):
            data_list = []
            data_list_reg = []
            
            with open(file_found, 'r', encoding='unicode_escape') as csvfile:
                data = csv.reader(csvfile)
                next(data) #Ignore the first line of the csv that contains the header
                for row in data:
                    if row[0] == 'registration ip':
                        registrationip = row[1] 
                        data_list_reg.append(('Registration IP',registrationip))
                    else:
                        date = (row[0].replace('UTC', '').strip())
                        ip = (row[1])
                        
                        data_list.append((date,ip))
                        
                if len(data_list) > 0:
                    report = ArtifactHtmlReport(f'Reddit {records} - IP Logs - {usernamemain}, {email}')
                    report.start_artifact_report(report_folder, f'Reddit {records} - IP Logs - {usernamemain}, {email}')
                    report.add_script()
                    data_headers = ('Timestamp','Permalink')
                    report.write_artifact_data_table(data_headers, data_list, file_found)
                    report.end_artifact_report()
                    
                    tlactivity = f'Reddit {records} - IP Logs - {usernamemain}, {email}'
                    timeline(report_folder, tlactivity, data_list, data_headers)
                else:
                    logfunc(f'No Reddit {records} - IP Logs - {usernamemain}, {email}')
                    
                if len(data_list_reg) > 0:
                    report = ArtifactHtmlReport(f'Reddit {records} - Registration IP - {usernamemain}, {email}')
                    report.start_artifact_report(report_folder, f'Reddit {records} - Registration IP - {usernamemain}, {email}')
                    report.add_script()
                    data_headers = ('Key','Value')
                    report.write_artifact_data_table(data_headers, data_list_reg, file_found)
                    report.end_artifact_report()
                    
                    tlactivity = f'Reddit {records} - Registration IP - {usernamemain}, {email}'
                    timeline(report_folder, tlactivity, data_list_reg, data_headers)
                else:
                    logfunc(f'No Reddit {records} - Registration IP - {usernamemain}, {email}')
                    
        if filename.startswith('linked_phone_number.csv'):
            data_list = [] 
            
            with open(file_found, 'r', encoding='unicode_escape') as csvfile:
                data = csv.reader(csvfile)
                next(data) #Ignore the first line of the csv that contains the header
                for row in data:
                    number = (row[0])
                    
                    data_list.append((number,))
                    
                if len(data_list) > 0:
                    report = ArtifactHtmlReport(f'Reddit {records} - Linked Phone - {usernamemain}, {email}')
                    report.start_artifact_report(report_folder, f'Reddit {records} - Linked Phone - {usernamemain}, {email}')
                    report.add_script()
                    data_headers = ('Number',)
                    report.write_artifact_data_table(data_headers, data_list, file_found)
                    report.end_artifact_report()
                    
                    tlactivity = f'Reddit {records} - Linked Phone - {usernamemain}, {email}'
                    timeline(report_folder, tlactivity, data_list, data_headers)
                else:
                    logfunc(f'No Reddit {records} - Linked Phone - {usernamemain}, {email}')
                    
        if filename.startswith('live_stream_posts.csv'):
            data_list = [] 
            
            with open(file_found, 'r', encoding='unicode_escape') as csvfile:
                data = csv.reader(csvfile)
                next(data) #Ignore the first line of the csv that contains the header
                for row in data:
                    posturl = (row[0])
                    filename(row[1])
                    
                    data_list.append((posturl,filename))
                    
                if len(data_list) > 0:
                    report = ArtifactHtmlReport(f'Reddit {records} - Live Stream Posts - {usernamemain}, {email}')
                    report.start_artifact_report(report_folder, f'Reddit {records} - Live Stream Posts - {usernamemain}, {email}')
                    report.add_script()
                    data_headers = ('Post URL','Filename')
                    report.write_artifact_data_table(data_headers, data_list, file_found)
                    report.end_artifact_report()
                    
                    tlactivity = f'Reddit {records} - Live Stream Posts - {usernamemain}, {email}'
                    timeline(report_folder, tlactivity, data_list, data_headers)
                else:
                    logfunc(f'No Reddit {records} - Live Stream Posts - {usernamemain}, {email}')
                        
        if filename.startswith('messages.csv'):
            data_list = [] 
            
            with open(file_found, 'r', encoding='unicode_escape') as csvfile:
                data = csv.reader(csvfile)
                next(data) #Ignore the first line of the csv that contains the header
                for row in data:
                    id = (row[0])
                    permalink = (row[1])
                    thread_id = (row[2])
                    date = (row[3].replace('UTC', '').strip())
                    ip = (row[4])
                    fromm = (row[5])
                    to = (row[6])
                    subject = (row[7])
                    body = (row[8])
                    
                    data_list.append((date,ip,to,fromm,subject,body,permalink,thread_id,id))
                    
                if len(data_list) > 0:
                    report = ArtifactHtmlReport(f'Reddit {records} - Messages - {usernamemain}, {email}')
                    report.start_artifact_report(report_folder, f'Reddit {records} - Messages - {usernamemain}, {email}')
                    report.add_script()
                    data_headers = ('Timestamp','IP','To','From','Subject','Body','Permalink','Thread ID','ID')
                    report.write_artifact_data_table(data_headers, data_list, file_found)
                    report.end_artifact_report()
                    
                    tlactivity = f'Reddit {records} - Messages - {usernamemain}, {email}'
                    timeline(report_folder, tlactivity, data_list, data_headers)
                else:
                    logfunc(f'No Reddit {records} - Messages - {usernamemain}, {email}')

        if filename.startswith('poll_votes.csv'):
            data_list = [] 
            
            with open(file_found, 'r', encoding='unicode_escape') as csvfile:
                data = csv.reader(csvfile)
                next(data) #Ignore the first line of the csv that contains the header
                for row in data:
                    post_id = (row[0])
                    user_selection = (row[1])
                    text = (row[2])
                    image_url = (row[3])
                    is_prediction = (row[4])
                    stake_amount = (row[5])
                    
                    data_list.append((post_id,user_selection,text,image_url,is_prediction,stake_amount))

                if len(data_list) > 0:
                    report = ArtifactHtmlReport(f'Reddit {records} - Poll Votes - {usernamemain}, {email}')
                    report.start_artifact_report(report_folder, f'Reddit {records} - Poll Votes - {usernamemain}, {email}')
                    report.add_script()
                    data_headers = ('Post ID','User Selection','Text','Image URL','Is Prediction','Stake Amount')
                    report.write_artifact_data_table(data_headers, data_list, file_found)
                    report.end_artifact_report()
                    
                    tlactivity = f'Reddit {records} - Poll Votes - {usernamemain}, {email}'
                    timeline(report_folder, tlactivity, data_list, data_headers)
                else:
                    logfunc(f'No Reddit {records} - Poll Votes - {usernamemain}, {email}')
                    

        if filename.startswith('post_votes.csv'):
            data_list = [] 
            
            with open(file_found, 'r', encoding='unicode_escape') as csvfile:
                data = csv.reader(csvfile)
                next(data) #Ignore the first line of the csv that contains the header
                for row in data:
                    id = (row[0])
                    permalink = (row[1])
                    direction = (row[2])
                    
                    data_list.append((id,permalink,direction))
                
                if len(data_list) > 0:
                    report = ArtifactHtmlReport(f'Reddit {records} - Post Votes - {usernamemain}, {email}')
                    report.start_artifact_report(report_folder, f'Reddit {records} - Post Votes - {usernamemain}, {email}')
                    report.add_script()
                    data_headers = ('ID','Permalink','Direction')
                    report.write_artifact_data_table(data_headers, data_list, file_found)
                    report.end_artifact_report()
                    
                    tlactivity = f'Reddit {records} - Post Votes - {usernamemain}, {email}'
                    timeline(report_folder, tlactivity, data_list, data_headers)
                else:
                    logfunc(f'No Reddit {records} - Post Votes - {usernamemain}, {email}')
                    
        if filename.startswith('posts.csv'):
            data_list = [] 
            
            with open(file_found, 'r', encoding='unicode_escape') as csvfile:
                data = csv.reader(csvfile)
                next(data) #Ignore the first line of the csv that contains the header
                for row in data:
                    id = (row[0])
                    permalink = (row[1])
                    date = (row[2].replace('UTC', '').strip())
                    ip = (row[3])
                    subreddit = (row[4])
                    gildings = (row[5])
                    title = (row[6])
                    url = (row[7])
                    body = (row[8])
                    
                    data_list.append((date,ip,id,title,url,body,permalink,subreddit,gildings))
                    
                if len(data_list) > 0:
                    report = ArtifactHtmlReport(f'Reddit {records} - Posts - {usernamemain}, {email}')
                    report.start_artifact_report(report_folder, f'Reddit {records} - Posts - {usernamemain}, {email}')
                    report.add_script()
                    data_headers = ('Timestamp','IP','ID','Title','URL','Body','Permalink','Subreddit','Gildings')
                    report.write_artifact_data_table(data_headers, data_list, file_found)
                    report.end_artifact_report()
                    
                    tlactivity = f'Reddit {records} - Posts - {usernamemain}, {email}'
                    timeline(report_folder, tlactivity, data_list, data_headers)
                else:
                    logfunc(f'No Reddit {records} - Posts - {usernamemain}, {email}')
                    
        if filename.startswith('reddit_gold_information.csv'):
            data_list = [] 
            
            with open(file_found, 'r', encoding='unicode_escape') as csvfile:
                data = csv.reader(csvfile)
                next(data) #Ignore the first line of the csv that contains the header
                for row in data:
                    processor = (row[0])
                    transaction_id= (row[1])
                    date = (row[2].replace('UTC', '').strip())
                    cost = (row[3])
                    payer_email = (row[4])
                    
                    data_list.append((date,processor,transaction_id,cost,payer_email))
                    
                if len(data_list) > 0:
                    report = ArtifactHtmlReport(f'Reddit {records} - Reddit Gold Info - {usernamemain}, {email}')
                    report.start_artifact_report(report_folder, f'Reddit {records} - Reddit Gold Info - {usernamemain}, {email}')
                    report.add_script()
                    data_headers = ('Timestamp','Processor','Transaction ID','Cost','Payer Email')
                    report.write_artifact_data_table(data_headers, data_list, file_found)
                    report.end_artifact_report()
                    
                    tlactivity = f'Reddit {records} - Reddit Gold Info - {usernamemain}, {email}'
                    timeline(report_folder, tlactivity, data_list, data_headers)
                else:
                    logfunc(f'No Reddit {records} - Reddit Gold Info - {usernamemain}, {email}')
                    

        if filename.startswith('saved_comments.csv'):
            data_list = [] 
                
            with open(file_found, 'r', encoding='unicode_escape') as csvfile:
                data = csv.reader(csvfile)
                next(data) #Ignore the first line of the csv that contains the header
                for row in data:
                    id = (row[0])
                    permalink= (row[1])
                
                    data_list.append((id,permalink))
                    
                if len(data_list) > 0:
                    report = ArtifactHtmlReport(f'Reddit {records} - Saved Comments - {usernamemain}, {email}')
                    report.start_artifact_report(report_folder, f'Reddit {records} - Saved Comments - {usernamemain}, {email}')
                    report.add_script()
                    data_headers = ('ID','Permalink')
                    report.write_artifact_data_table(data_headers, data_list, file_found)
                    report.end_artifact_report()
                    
                    tlactivity = f'Reddit {records} - Saved Comments - {usernamemain}, {email}'
                    timeline(report_folder, tlactivity, data_list, data_headers)
                else:
                    logfunc(f'No Reddit {records} - Saved Comments - {usernamemain}, {email}')

        if filename.startswith('saved_posts.csv'):
            data_list = [] 
            
            with open(file_found, 'r', encoding='unicode_escape') as csvfile:
                data = csv.reader(csvfile)
                next(data) #Ignore the first line of the csv that contains the header
                for row in data:
                    id = (row[0])
                    permalink= (row[1])
                    
                    data_list.append((id,permalink))
                
                if len(data_list) > 0:
                    report = ArtifactHtmlReport(f'Reddit {records} - Saved Posts - {usernamemain}, {email}')
                    report.start_artifact_report(report_folder, f'Reddit {records} - Saved Posts - {usernamemain}, {email}')
                    report.add_script()
                    data_headers = ('ID','Permalink')
                    report.write_artifact_data_table(data_headers, data_list, file_found)
                    report.end_artifact_report()
                    
                    tlactivity = f'Reddit {records} - Saved Posts - {usernamemain}, {email}'
                    timeline(report_folder, tlactivity, data_list, data_headers)
                else:
                    logfunc(f'No Reddit {records} - Saved Posts - {usernamemain}, {email}')
                    
        if filename.startswith('scheduled_posts.csv'):
            data_list = [] 
            
            with open(file_found, 'r', encoding='unicode_escape') as csvfile:
                data = csv.reader(csvfile)
                next(data) #Ignore the first line of the csv that contains the header
                for row in data:
                    scheduled_post_id = (row[0])
                    subreddit = (row[1])
                    title = (row[2])
                    body = (row[3])
                    url = (row[4])
                    submission_time = (row[5])
                    recurrence = (row[6])
                    
                    data_list.append((scheduled_post_id,subreddit,title,body,url,submission_time,recurrence))
                    
                if len(data_list) > 0:
                    report = ArtifactHtmlReport(f'Reddit {records} - Scheduled Posts - {usernamemain}, {email}')
                    report.start_artifact_report(report_folder, f'Reddit {records} - Scheduled Posts - {usernamemain}, {email}')
                    report.add_script()
                    data_headers = ('Scheduled Post ID','Subreddit','Title','Body','URL','Submission Time','Recurrence')
                    report.write_artifact_data_table(data_headers, data_list, file_found)
                    report.end_artifact_report()
                    
                    tlactivity = f'Reddit {records} - Scheduled Posts - {usernamemain}, {email}'
                    timeline(report_folder, tlactivity, data_list, data_headers)
                else:
                    logfunc(f'No Reddit {records} - Scheduled Posts - {usernamemain}, {email}')
                    
        if filename.startswith('statistics.csv'):
            data_list = [] 
            
            with open(file_found, 'r', encoding='unicode_escape') as csvfile:
                data = csv.reader(csvfile)
                next(data) #Ignore the first line of the csv that contains the header
                for row in data:
                    key = (row[0])
                    value = (row[1])
                    
                    data_list.append((key,value))
                
                if len(data_list) > 0:
                    report = ArtifactHtmlReport(f'Reddit {records} - Statistics - {usernamemain}, {email}')
                    report.start_artifact_report(report_folder, f'Reddit {records} - Statistics - {usernamemain}, {email}')
                    report.add_script()
                    data_headers = ('Key','Value')
                    report.write_artifact_data_table(data_headers, data_list, file_found)
                    report.end_artifact_report()
                    
                    tlactivity = f'Reddit {records} - Statistics - {usernamemain}, {email}'
                    timeline(report_folder, tlactivity, data_list, data_headers)
                else:
                    logfunc(f'No Reddit {records} - Statistics - {usernamemain}, {email}')
                

        if filename.startswith('user_preferences.csv'):
            data_list = [] 
            
            with open(file_found, 'r', encoding='unicode_escape') as csvfile:
                data = csv.reader(csvfile)
                next(data) #Ignore the first line of the csv that contains the header
                for row in data:
                    key = (row[0])
                    value = (row[1])
                
                if len(data_list) > 0:
                    report = ArtifactHtmlReport(f'Reddit {records} - User Prefs - {usernamemain}, {email}')
                    report.start_artifact_report(report_folder, f'Reddit {records} - User Prefs - {usernamemain}, {email}')
                    report.add_script()
                    data_headers = ('Key','Value')
                    report.write_artifact_data_table(data_headers, data_list, file_found)
                    report.end_artifact_report()
                    
                    tlactivity = f'Reddit {records} - User Prefs - {usernamemain}, {email}'
                    timeline(report_folder, tlactivity, data_list, data_headers)
                else:
                    logfunc(f'No Reddit {records} - User Prefs - {usernamemain}, {email}')
                    

__artifacts__ = {
        "reddit": (
            "Reddit Returns",
            ('*/Reddit production/*/account linked to */*/*.csv'),
            get_reddit)
}
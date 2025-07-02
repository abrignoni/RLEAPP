__artifacts_v2__ = {
    "tweets": {
        "name": "Tweets",
        "description": "Processes tweets from a twitter return",
        "author": "@AlexisBrignoni",
        "creation_date": "2025-06-23",
        "last_update_date": "2025-06-23",
        "requirements": "none",
        "category": "Twitter",
        "notes": "",
        "paths": ('*/*_tweets_media/*.*','*/*-tweets*.txt',),
        "output_types": "standard",
        "artifact_icon": "twitter",
    },
    "deltweets": {
        "name": "Deleted Tweets",
        "description": "Processes tweets from a twitter return",
        "author": "@AlexisBrignoni",
        "creation_date": "2025-06-24",
        "last_update_date": "2025-06-24",
        "requirements": "none",
        "category": "Twitter",
        "notes": "",
        "paths": ('*/*_deleted_tweets_media/*.*','*/*deleted-tweets*.txt',),
        "output_types": "standard",
        "artifact_icon": "twitter",
    },
    "dmtwitter": {
        "name": "Twitter DMs",
        "description": "Processes direct messages from a twitter return",
        "author": "@AlexisBrignoni",
        "creation_date": "2025-06-25",
        "last_update_date": "2025-06-25",
        "requirements": "none",
        "category": "Twitter",
        "notes": "",
        "paths": ('*/*_direct_messages_media/*.*','*/*direct-messages*.txt',),
        "output_types": "standard",
        "artifact_icon": "twitter",
    },
    "deleteddmtwitter": {
        "name": "Deleted Twitter DMs",
        "description": "Processes direct messages from a twitter return",
        "author": "@AlexisBrignoni",
        "creation_date": "2025-07-01",
        "last_update_date": "2025-07-01",
        "requirements": "none",
        "category": "Twitter",
        "notes": "",
        "paths": ('*/*_deleted_direct_messages_media/*.*','*/*-deleted-direct-messages*.txt',),
        "output_types": "standard",
        "artifact_icon": "twitter",
    },
    "blocktwitter": {
        "name": "Blocked Twitter",
        "description": "Processes direct messages from a twitter return",
        "author": "@AlexisBrignoni",
        "creation_date": "2025-07-02",
        "last_update_date": "2025-07-02",
        "requirements": "none",
        "category": "Twitter",
        "notes": "",
        "paths": ('*/*-block*.txt',),
        "output_types": "standard",
        "artifact_icon": "twitter",
    }
}

    
import os
from datetime import datetime, timezone
import csv
import codecs
import inspect
import shutil
import json
from pathlib import Path

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, is_platform_windows, artifact_processor, check_in_media

def load_json_from_signed_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Find where the actual JSON starts
    json_start_index = 0
    for i, line in enumerate(lines):
        if line.strip() == '':
            # Blank line separates headers from the message
            json_start_index = i + 1
            break
        
    # Now join the lines that contain the JSON body
    json_lines = []
    for line in lines[json_start_index:]:
        if line.startswith("-----BEGIN PGP SIGNATURE-----"):
            break  # Stop at the start of the PGP signature block
        json_lines.append(line)
        
    json_str = ''.join(json_lines)
    return json.loads(json_str)

@artifact_processor
def tweets(files_found, report_folder, seeker, wrap_text):
    artifact_info = inspect.stack()[0]
    data_list = []
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if '-' in filename:
            lastpart = filename.split('-')[1]
        else:
            lastpart = ''
        
        if filename.startswith('.'):
            pass
            
        elif lastpart.startswith('tweets'):
            #logfunc(file_found)
            filenametweets = file_found
            data = load_json_from_signed_file(filenametweets)
            
            for items in data:
            
                timestamp = (items['tweet'].get('created_at'))
                
                dt = datetime.strptime(timestamp, "%a %b %d %H:%M:%S %z %Y")
                dt_utc = dt.astimezone(timezone.utc)
                timestamp = dt_utc
                
                idstr = (items['tweet'].get('id_str'))
                fulltext = (items['tweet'].get('full_text'))
                #source = (items['tweet'].get('source'))
                tweetid = (items['tweet'].get('id'))
                
                initial = str((items['tweet']['edit_info']['initial']))
                retweeted = (items['tweet'].get('retweeted'))
                
                entities = (items['tweet'].get('entities'))
                favoritecount = (items['tweet'].get('favorite_count'))
                inreplytostatusid = (items['tweet'].get('in_reply_to_status_id_str'))
                inreplytouserid = (items['tweet'].get('in_reply_to_user_id'))
                truncated = (items['tweet'].get('truncated'))
                retweetecount = (items['tweet'].get('retweet_count'))
            
                favorited = (items['tweet'].get('favorited'))
            
                lang = (items['tweet'].get('lang'))
                inreplytoscreenname = (items['tweet'].get('in_reply_to_screen_name'))
                inreplytouseridstr = (items['tweet'].get('in_reply_to_user_id_str'))
                
                media_item = ''
                
                for tentative_media in files_found:
                    if idstr in tentative_media:
                        media_path = Path(tentative_media )
                        
                        filenamem = (media_path.name)
                        filepath = str(media_path.parents[1])
                        
                        #logfunc(f'{filename}-{artifact_info}')
                        media_item = check_in_media(tentative_media, filenamem)
                        break
                
                data_list.append((timestamp, idstr, fulltext, media_item, tweetid,
                                    initial, retweeted, entities, filename))
            
    data_headers = (('Timestamp', 'datetime'), 'ID Str', 'Full Text', ('Image', 'media'),
                'Tweet ID', 'Edit Info Initial', 'Retweeted', 'Entities', 'File Source')
    
    return data_headers, data_list, 'See source path(s) below'

@artifact_processor
def deltweets(files_found, report_folder, seeker, wrap_text):
    #artifact_info = inspect.stack()[0]
    data_list = []
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if '-' in filename:
            lastpart = filename.split('-',1)[1]
        else:
            lastpart = ''
            
        if filename.startswith('.'):
            pass
            
        elif lastpart.startswith('deleted-tweets'):
            #logfunc(file_found)
            filenametweets = file_found
            data = load_json_from_signed_file(filenametweets)
            
            for items in data:
                
                timestamp = (items['tweet'].get('created_at'))
                
                dt = datetime.strptime(timestamp, "%a %b %d %H:%M:%S %z %Y")
                dt_utc = dt.astimezone(timezone.utc)
                timestamp = dt_utc
                
                idstr = (items['tweet'].get('id_str'))
                fulltext = (items['tweet'].get('full_text'))
                #source = (items['tweet'].get('source'))
                tweetid = (items['tweet'].get('id'))
                
                initial = str((items['tweet']['edit_info']['initial']))
                retweeted = (items['tweet'].get('retweeted'))
                
                entities = (items['tweet'].get('entities'))
                favoritecount = (items['tweet'].get('favorite_count'))
                inreplytostatusid = (items['tweet'].get('in_reply_to_status_id_str'))
                inreplytouserid = (items['tweet'].get('in_reply_to_user_id'))
                truncated = (items['tweet'].get('truncated'))
                retweetecount = (items['tweet'].get('retweet_count'))
                
                favorited = (items['tweet'].get('favorited'))
                
                lang = (items['tweet'].get('lang'))
                inreplytoscreenname = (items['tweet'].get('in_reply_to_screen_name'))
                inreplytouseridstr = (items['tweet'].get('in_reply_to_user_id_str'))
                
                media_item = ''
                
                for tentative_media in files_found:
                    if idstr in tentative_media:
                        media_path = Path(tentative_media )
                        
                        filenamem = (media_path.name)
                        filepath = str(media_path.parents[1])
                        
                        #logfunc(f'{tentative_media}-{filenamem}')
                        media_item = check_in_media(tentative_media, filenamem)
                        break
                    
                data_list.append((timestamp, idstr, fulltext, media_item, tweetid,
                                    initial, retweeted, entities, filename))
                
    data_headers = (('Timestamp', 'datetime'), 'ID Str', 'Full Text', ('Image', 'media'),
                'Tweet ID', 'Edit Info Initial', 'Retweeted', 'Entities', 'File Source')
    
    return data_headers, data_list, 'See source path(s) below'

    
@artifact_processor
def dmtwitter(files_found, report_folder, seeker, wrap_text):
    artifact_info = inspect.stack()[0]
    data_list = []

    for file_found in files_found:
        file_found = str(file_found)

        filename = os.path.basename(file_found)

        if '-' in filename:
            lastpart = filename.split('-',1)[1]
        else:
            lastpart = ''

        if filename.startswith('.'):
            pass

        elif lastpart.startswith('direct-messages'):
            #logfunc(file_found)
            filenametweets = file_found
            data = load_json_from_signed_file(filenametweets)

            for items in data:
                convid = items['dmConversation']['conversationId']
                messages = items['dmConversation']['messages']
                #senderid = items['dmConversation']['messages']['messageCreate']['senderId']
                
                
                for message in messages:
                    senderid = message['messageCreate']['senderId']
                    recipientid = message['messageCreate']['recipientId']
                    text = message['messageCreate']['text']
                    timestamp = message['messageCreate']['createdAt']
                    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
                    mediaurls = message['messageCreate']['mediaUrls']
                    reactions = message['messageCreate']['reactions']
                    data_list.append((timestamp,senderid,recipientid,text,convid,mediaurls,reactions,filename))

    data_headers = (('Timestamp', 'datetime'),'Sender ID','Recipient ID','Text','Conversation ID','Media URLs','Reactions','File Source')

    return data_headers, data_list, 'See source path(s) below'

@artifact_processor
def deleteddmtwitter(files_found, report_folder, seeker, wrap_text):
    artifact_info = inspect.stack()[0]
    data_list = []
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if '-' in filename:
            lastpart = filename.split('-',1)[1]
        else:
            lastpart = ''
            
        if filename.startswith('.'):
            pass
            
        elif lastpart.startswith('deleted-direct-messages'):
            #logfunc(file_found)
            filenametweets = file_found
            data = load_json_from_signed_file(filenametweets)
            
            for items in data:
                convid = items['dmConversation']['conversationId']
                messages = items['dmConversation']['messages']
                #senderid = items['dmConversation']['messages']['messageCreate']['senderId']
                
                
                for message in messages:
                    idstr = message['messageCreate']['id']
                    senderid = message['messageCreate']['senderId']
                    recipientid = message['messageCreate']['recipientId']
                    text = message['messageCreate']['text']
                    timestamp = message['messageCreate']['createdAt']
                    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
                    mediaurls = message['messageCreate']['mediaUrls']
                    reactions = message['messageCreate']['reactions']
                    
                    media_item = ''
                    
                    for tentative_media in files_found:
                        if idstr in tentative_media:
                            media_path = Path(tentative_media )
                            
                            filenamem = (media_path.name)
                            filepath = str(media_path.parents[1])
                            
                            #logfunc(f'{tentative_media}-{filenamem}')
                            media_item = check_in_media(tentative_media, filenamem)
                            break
                    
                    data_list.append((timestamp,senderid,recipientid,text,media_item,convid,mediaurls,reactions,filename))
                    
    data_headers = (('Timestamp', 'datetime'),'Sender ID','Recipient ID','Text',('Image', 'media'),'Conversation ID','Media URLs','Reactions','File Source')
    
    return data_headers, data_list, 'See source path(s) below'

@artifact_processor
def blocktwitter(files_found, report_folder, seeker, wrap_text):
    artifact_info = inspect.stack()[0]
    data_list = []
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if '-' in filename:
            lastpart = filename.split('-',1)[1]
        else:
            lastpart = ''
            
        if filename.startswith('.'):
            pass
            
        elif lastpart.startswith('block'):
            #logfunc(file_found)
            filenametweets = file_found
            data = load_json_from_signed_file(filenametweets)
            
            for items in data:
                accountid = items['blocking']['accountId']
                userlink = items['blocking']['userLink']
                
                data_list.append((accountid,userlink,filename))
    
    data_headers = ('Account ID','User Link','File Source')
    
    return data_headers, data_list, 'See source path(s) below'            
                
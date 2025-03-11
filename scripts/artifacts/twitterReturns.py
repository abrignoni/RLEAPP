import os
from datetime import datetime
import csv
import codecs
import shutil
import json

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html

def get_twitterReturns(files_found, report_folder, seeker, wrap_text):
    data_list_dms =[]
    data_list_groupdm = []
    data_list_account = []
    data_list_followers = []
    data_list_following = []
    data_list_lists_created = []
    data_list_profile_description = []
    data_list_saved_searches = []
    data_list_screen_name_changes = []
    data_list_tweets = []
    data_list_devices = []
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.endswith('-dms.txt'):
            filenamedms = file_found
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
                    thumb = media_to_html(idc, files_found, report_folder)
                    
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
                    
                    data_list_dms.append((timestamp, convoid, sid, rid, text, thumb))	
                    
                
        if filename.endswith('-groupdm.txt'):
            filenamegroupdm = file_found
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
                    data_list_groupdm.append((timestampj, convoid, '', '', messagefinal, ''))
                    
                if 'ParticipantsJoin (user IDs):' in line:
                    #print(line)
                    timestampk = (line.split(': ')[0].split('+')[0].strip())
                    messagec = (line.split(': ')[1])
                    messaged = (line.split(': ')[2].strip())
                    messagefinala = (f'{messagec}: {messaged}')
                    data_list_groupdm.append((timestampk, convoid, '', '', messagefinala, ''))
                    
                if '"id" :' in line:
                    idc = line.split(': ')[1].replace(',', '').strip()
                    thumbs = media_to_html(str(idc), files_found, report_folder)
                    
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
                    
                    data_list_groupdm.append((timestamp, convoid, sid, rid, text, thumbs))

        if filename.endswith('-account.txt'):
            filenameaccount = file_found
            with open(file_found, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            count = 0
            account_id = created_at = updated_at = email = created_via = screen_name = creation_ip = time_zone = ''
            for line in lines:
                count += 1
                
                if count < 3:
                    pass
                    
                if 'account_id:' in line:
                    account_id = line.split(': ')[1].replace(',', '').strip()
                    
                if 'created_at:' in line:
                    created_at = line.split(': ')[1].replace(',', '').strip()
                
                if 'updated_at:' in line:
                    updated_at = line.split(': ')[1].replace(',', '').strip()
                
                if 'email:' in line:
                    email = line.split(': ')[1].replace(',', '').strip()
                    
                if 'created_via:' in line:
                    created_via = line.split(': ',1)[1].replace(',', '').strip()
                    
                if 'screen_name:' in line:
                    screen_name = line.split(': ')[1].replace(',', '').strip()
                    
                if 'creation_ip:' in line:
                    creation_ip = line.split(': ')[1].replace(',', '').strip()
                
                if 'time_zone:' in line:
                    time_zone = line.split(': ')[1].replace(',', '').strip()
                    data_list_account.append((created_at, screen_name, account_id, updated_at, email, creation_ip, created_via, time_zone))
                    account_id = created_at = updated_at = email = created_via = screen_name = creation_ip = time_zone = ''
        
        if filename.endswith('-followers.txt'):
            filenamefollowers = file_found
            with open(file_found, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            count = 0
            for line in lines:
                count += 1
                
                if count < 4:
                    continue
                
                if 'BEGIN PGP SIGNATURE' in line:
                    break
                else:
                    if len(line) > 1:
                        data_list_followers.append((line.strip(),))
    
        if filename.endswith('-following.txt'):
            filenamefollowing = file_found
            with open(file_found, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            count = 0
            for line in lines:
                count += 1
                
                if count < 4:
                    continue
                
                if 'BEGIN PGP SIGNATURE' in line:
                    break
                else:
                    if len(line) > 1:
                        data_list_following.append((line.strip(),))
        
        if filename.endswith('-lists_created.txt'):
            filenamelistscreated = file_found
            with open(file_found, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            count = 0
            for line in lines:
                count += 1
                
                if count < 4:
                    continue
                
                if 'BEGIN PGP SIGNATURE' in line:
                    break
                else:
                    if len(line) > 1:
                        data_list_lists_created.append((line.strip(),))
    
        if filename.endswith('-profile-description.txt'):
            filenameprofiledesc = file_found
            with open(file_found, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            count = 0    
            for line in lines:
                count += 1
                
                if count < 3:
                    pass
                    
                if 'bio:' in line:
                    bio = line.split(': ')[1].replace(',', '').replace('"','').strip()
                    
                if 'website:' in line:
                    website = line.split(': ')[1].replace(',', '').replace('"','').strip()
                    if website == '' and bio == '':
                        pass
                    else:
                        data_list_profile_description.append((bio, website))
    
        if filename.endswith('-saved-searches.txt'):
            filenamesavedsearch = file_found
            with open(file_found, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            count = 0    
            for line in lines:
                count += 1
                
                if count < 3:
                    pass
                    
                if 'id:' in line:
                    ids = line.split(': ')[1].replace(',', '').replace('"','').strip()
                    
                if 'query:' in line:
                    query = line.split(': ')[1].replace(',', '').replace('"','').strip()
                
                if 'name:' in line:
                    name = line.split(': ')[1].replace(',', '').replace('"','').strip()
                    
                    if ids == '' and query == '' and name == '':
                        pass
                    else:
                        data_list_saved_searches.append((ids, query, name ))
        
        if filename.endswith('-screen-name-changes.txt'):
            filenamescreenname = file_found
            with open(file_found, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            count = 0    
            for line in lines:
                count += 1
                
                if count < 3:
                    continue
                
                if 'BEGIN PGP SIGNATURE' in line:
                    break
                else:
                    if '->' in line:
                        namefrom = (line.split('->')[0].strip())
                        nameto = (line.split('->')[1].split(' ')[1])
                        timechange = (line.split('->')[1].split('(')[1].split('+')[0].strip())
                        data_list_screen_name_changes.append((timechange, namefrom, nameto))
                        
        if filename.endswith('-devices.txt'):
            filenamedevices = file_found
            with open(file_found, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            count = 0
            createdat = updatedat = typed = ipxcarry = phonen = ''
            for line in lines:
                count += 1
                
                if count < 2:
                    pass
                    
                if 'created_at:' in line:
                    dated = (line.split(' '))
                    createdat = f'{dated[1]} {dated[2]} {dated[3]}'
                    
                if 'updated_at:' in line:
                    dated = (line.split(' '))
                    updatedat = f'{dated[1]} {dated[2]} {dated[3]}'
                    
                if 'type:' in line:
                    typed = (line.split(' '))
                    typed = typed[1]
                
                if 'ipx_carrier_name:' in line:
                    ipxcarry = (line.split(' '))
                    ipxcarry = ipxcarry[1]
                    
                if 'phone_numer:' in line:
                    phonen = (line.split(' '))
                    phonen  = phonen[1]    
                    
                    if createdat == '' and updatedat == '' and typed == '' and ipxcarry == '' and phonen == '':
                        pass
                    else:
                        data_list_devices.append((createdat, updatedat, typed, ipxcarry, phonen ))
                        createdat = updatedat = typed = ipxcarry = phonen = ''
        
        if filename.endswith('-tweets.txt'):
            filenametweets = file_found
            aggregator = ' '
            dateds = timetochange = datetime_object = timestampeds = rtid = rttext = rtsource = rtcoor = ''
            with open(file_found, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            count = 0
            for line in lines:
                count += 1
                
                if count < 4:
                    continue
                
                if '* Tweet ID #' in line:
                    tweetid = (line.split('#')[1].split(' ')[0])
                    if aggregator == ' ':
                        pass
                    else:
                        work = json.loads(aggregator)
                        dated = (work['created_at'].split(' '))
                        timetochange = f'{dated[1]} {dated[2]} {dated[3]} {dated[5]}'
                        datetime_object = datetime.strptime(timetochange, '%b %d %H:%M:%S %Y')
                        timestamped = (datetime_object)
                        wid = (work['id'])
                        thumbs = media_to_html(str(wid), files_found, report_folder)
                        wtext = work.get('text')
                        wsource = work.get('source')
                        wcoord = work.get('coordinates')
                        
                        checkval = work.get('retweeted_status', ' ')
                        if checkval != ' ':
                            dateds = (work['retweeted_status']['created_at'].split(' '))
                            timetochange = f'{dateds[1]} {dateds[2]} {dateds[3]} {dateds[5]}'
                            datetime_object = datetime.strptime(timetochange, '%b %d %H:%M:%S %Y')
                            timestampeds = (datetime_object)
                            rtid = (work['retweeted_status']['id'])
                            rttext = work['retweeted_status'].get('text')
                            rtsource = work['retweeted_status'].get('source')
                            rtcoor = work['retweeted_status'].get('coordinates')
                        else:
                            timestampeds = rtid = rttext = rtsource = rtcoor = ' '
                            
                        data_list_tweets.append((timestamped, wid, wtext, thumbs, wsource, wcoord, timestampeds, rtid, rttext, rtsource, rtcoor))
                        aggregator = ' '
                else:
                    aggregator = aggregator + line.strip()
                    
                if '-----BEGIN PGP SIGNATURE-----' in line:
                    if data_list_tweets:
                        data_list_tweets.append((timestamped, wid, wtext, thumbs, wsource, wcoord, timestampeds, rtid, rttext, rtsource, rtcoor))
    
    if data_list_tweets:
        report = ArtifactHtmlReport('Twitter Returns - Tweets')
        report.start_artifact_report(report_folder, 'Twitter Returns - Tweets')
        report.add_script()
        data_headers = ('Timestamp','ID','Text','Media','Source','Coordinates','RT Timestamp','RT ID','RT Text','RT Source','RT Coordinates')
        report.write_artifact_data_table(data_headers, data_list_tweets, filenametweets, html_no_escape=['Media'])
        report.end_artifact_report()
        
        tsvname = f'Twitter Returns - Tweets'
        tsv(report_folder, data_list_tweets, data_headers, tsvname)
        
        tlactivity = f'Twitter Returns - Tweets'
        timeline(report_folder, tlactivity, data_list_tweets, data_headers)
    
    if data_list_screen_name_changes:
        report = ArtifactHtmlReport('Twitter Returns - Screen Name Changes')
        report.start_artifact_report(report_folder, 'Twitter Returns - Screen Name Changes')
        report.add_script()
        data_headers = ('Timestamp','Name From','Name To')
        report.write_artifact_data_table(data_headers, data_list_screen_name_changes, filenamescreenname)
        report.end_artifact_report()
        
        tsvname = f'Twitter Returns - Screen Name Changes'
        tsv(report_folder, data_list_screen_name_changes, data_headers, tsvname)
        
        tlactivity = f'Twitter Returns - Screen Name Changes'
        timeline(report_folder, tlactivity, data_list_screen_name_changes, data_headers)
    
    if data_list_saved_searches:
        report = ArtifactHtmlReport('Twitter Returns - Saved Searches')
        report.start_artifact_report(report_folder, 'Twitter Returns - Saved Searches')
        report.add_script()
        data_headers = ('ID','Query','Name')
        report.write_artifact_data_table(data_headers, data_list_saved_searches, filenamesavedsearch)
        report.end_artifact_report()
        
        tsvname = f'Twitter Returns - Saved Searches'
        tsv(report_folder, data_list_saved_searches, data_headers, tsvname)
        
    else:
        logfunc('No Twitter Returns - Saved Searches data available')
                            
    if data_list_profile_description:
        report = ArtifactHtmlReport('Twitter Returns - Profile Description')
        report.start_artifact_report(report_folder, 'Twitter Returns - Profile Description')
        report.add_script()
        data_headers = ('Bio','Website')
        report.write_artifact_data_table(data_headers, data_list_profile_description, filenameprofiledesc )
        report.end_artifact_report()
        
        tsvname = f'Twitter Returns - Profile Description'
        tsv(report_folder, data_list_profile_description, data_headers, tsvname)
        
    else:
        logfunc('No Twitter Returns - Profile Description data available')

    if data_list_lists_created:
        report = ArtifactHtmlReport('Twitter Returns - Lists Created')
        report.start_artifact_report(report_folder, 'Twitter Returns - Lists Created')
        report.add_script()
        data_headers = ('List',)
        report.write_artifact_data_table(data_headers, data_list_lists_created, filenamelistscreated)
        report.end_artifact_report()
        
        tsvname = f'Twitter Returns - Lists Created'
        tsv(report_folder, data_list_lists_created, data_headers, tsvname)
        
    else:
        logfunc('No Twitter Returns - Lists Created data available')
        
    if data_list_following:
        report = ArtifactHtmlReport('Twitter Returns - Following')
        report.start_artifact_report(report_folder, 'Twitter Returns - Following')
        report.add_script()
        data_headers = ('Following',)
        report.write_artifact_data_table(data_headers, data_list_following, filenamefollowing)
        report.end_artifact_report()
        
        tsvname = f'Twitter Returns - Following'
        tsv(report_folder, data_list_following, data_headers, tsvname)
        
    else:
        logfunc('No Twitter Returns - Following data available')
    
    if data_list_followers:
        report = ArtifactHtmlReport('Twitter Returns - Followers')
        report.start_artifact_report(report_folder, 'Twitter Returns - Followers')
        report.add_script()
        data_headers = ('Followers',)
        report.write_artifact_data_table(data_headers, data_list_followers, filenamefollowers)
        report.end_artifact_report()
        
        tsvname = f'Twitter Returns - Followers'
        tsv(report_folder, data_list_followers, data_headers, tsvname)
        
    else:
        logfunc('No Twitter Returns - Followers data available')
        
        
    if data_list_account:
        report = ArtifactHtmlReport('Twitter Returns - Account Data')
        report.start_artifact_report(report_folder, 'Twitter Returns - Account Data')
        report.add_script()
        data_headers = ('Created At', 'Screen Name', 'Account ID', 'Updated At', 'Email', 'Creation IP', 'Created Via', 'Time Zone')
        report.write_artifact_data_table(data_headers, data_list_account, filenameaccount )
        report.end_artifact_report()
        
        tsvname = f'Twitter Returns - Account Data'
        tsv(report_folder, data_list_account, data_headers, tsvname)
        
        tlactivity = f'Twitter Returns - Account Data'
        timeline(report_folder, tlactivity, data_list_account, data_headers)
    else:
        logfunc('No Twitter Returns - Account Data available')
        

    if data_list_dms:
        report = ArtifactHtmlReport('Twitter Returns - Direct Messages')
        report.start_artifact_report(report_folder, 'Twitter Returns - Direct Messages')
        report.add_script()
        data_headers = ('Timestamp', 'Conversation ID', 'Sender ID', 'Recipient ID', 'Message', 'Media')
        report.write_artifact_data_table(data_headers, data_list_dms, filenamedms, html_no_escape=['Media'])
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
        data_headers = ('Timestamp', 'Conversation ID', 'Sender ID', 'Recipient ID', 'Message', 'Media')
        report.write_artifact_data_table(data_headers, data_list_groupdm, filenamegroupdm, html_no_escape=['Media'])
        report.end_artifact_report()
        
        tsvname = f'Twitter Returns - Group Messages'
        tsv(report_folder, data_list_groupdm, data_headers, tsvname)
        
        tlactivity = f'Twitter Returns - Group Messages'
        timeline(report_folder, tlactivity, data_list_groupdm, data_headers)
    else:
        logfunc('No Twitter Returns - Group Messages data available')
        
    
    if data_list_devices:
        report = ArtifactHtmlReport('Twitter Returns - Devices')
        report.start_artifact_report(report_folder, 'Twitter Returns - Devices')
        report.add_script()
        data_headers = ('Created At', 'Updated At', 'Type', 'IPX Carrier Name', 'Phone Number')
        report.write_artifact_data_table(data_headers, data_list_devices, filenamedevices)
        report.end_artifact_report()
        
        tsvname = f'Twitter Returns - Devices'
        tsv(report_folder, data_list_devices, data_headers, tsvname)
        
        tlactivity = f'Twitter Returns - Devices'
        timeline(report_folder, tlactivity, data_list_devices, data_headers)
    else:
        logfunc('No Twitter Returns - Devices')

__artifacts__ = {
        "twitterReturns": (
            "Twitter Returns",
            ('*/*/*','*/*.txt'),
            get_twitterReturns)
}
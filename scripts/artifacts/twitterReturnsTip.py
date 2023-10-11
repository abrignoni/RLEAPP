import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html

def timestamps(line):
    date = (line.split('T'))
    
    dateall = (date[0].split(': "')[1].split('-'))
    year = (dateall[0])
    month = (dateall[1])
    day = (dateall[2])
    
    hours = (date[1].split(':')[0])
    minutes = (date[1].split(':')[1])
    seconds = (date[1].split(':')[2].replace('Z"','').replace(',','').strip())
    
    timestamp = f'{year}-{month}-{day} {hours}:{minutes}:{seconds}'
    return timestamp

def monthletter(month):
    monthdict = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    return monthdict[month]

def get_twitterReturnsTip(files_found, report_folder, seeker, wrap_text, time_offset):
    
    if is_platform_windows():
        separator = '\\'
    else:
        separator = '/'
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.endswith('-direct-messages.txt'):
            data_list = []
            filenamedms = file_found
            filenamenoext = (filename.split('-', 1)[1].replace('.txt','').strip())
            with open(file_found, 'r', encoding='utf-8') as f:	
                
                    for line in f:
                        if '**** conversationId:' in line:
                            convoid = line.split(': ')[1].replace('*','').strip()
                            #print(convoid)
                        elif '"id" :' in line:
                            idc = line.split(': ')[1].replace(',', '').replace('"', '').strip()
                            #print(idc)
                        elif  '"senderId" :' in line:
                            sid = line.split(': ')[1].replace(',', '').replace('"', '').strip()
                            #print(sid)
                        elif  '"recipientId" :' in line:
                            rid = line.split(': ')[1].replace(',', '').replace('"', '').strip()
                            #print(rid)
                        elif  '"text" :' in line:
                            text = line.split(': ')[1].replace(',', '').replace('"', '').strip()
                            #print(text)
                        elif '"createdAt" :' in line:
                            timestamp = timestamps(line)
                            
                        elif  '"mediaUrls" :' in line:
                            line = line.strip()
                            if line.endswith('[ ],'):
                                mediaurl = ''
                                thumb = ''
                            else:
                                extraline = next(f)
                                mediaurl = extraline.replace('"','').strip()
                                if 'ton' in mediaurl:
                                    mediaident = mediaurl.split(separator)[-1]
                                    thumb = media_to_html(mediaident, files_found, report_folder)
                                elif 'video' in mediaurl:
                                    mediaident = mediaurl.split(separator)[-1].split('?')[0]
                                    thumb = media_to_html(mediaident, files_found, report_folder)
                                else:
                                    thumb = ''
                                
                        elif '"reactions" :' in line:
                            line = line.strip()
                            if line.endswith('[ ],'):
                                reactkey = rsenderid = reventid = rtimestamp = ''
                            else:
                                extraline = next(f)
                                extraline = next(f)
                                rsenderid = extraline.split(' : ')[1].replace('"','').replace(',','').strip()
                                #print(rsenderid)
                                extraline = next(f)
                                reactkey = extraline.split(' : ')[1].replace('"','').replace(',','').strip()
                                #print(reactkey)
                                extraline = next(f)
                                reventid = extraline.split(' : ')[1].replace('"','').replace(',','').strip()
                                #print(reventid)
                                extraline = next(f)
                                if rtimestamp == '':
                                    pass
                                else:
                                    rtimestamp = timestamps(extraline)
                                
                        elif  '"urls" :' in line:
                            line = line.strip()
                            if line.endswith(']'):
                                url = expanded = display = ''
                            else:
                                extraline = next(f)
                                #print(extraline,'0')
                                extraline = next(f)
                                url = extraline.split(': ')[1].replace('"','').replace(',','').strip()
                                #print(url)
                                extraline = next(f)
                                expanded = extraline.split(': ')[1].replace('"','').replace(',','').strip()
                                #print(expanded)
                                extraline = next(f)
                                if extraline == '':
                                    pass
                                else:
                                    display = extraline.split(': ')[1].replace('"','').replace(',','').strip()
                                #print(display)
                                
                            data_list.append((timestamp, convoid, sid, rid, text, thumb, mediaurl, url, expanded, display, rtimestamp, rsenderid, reactkey, reventid, idc ))
                            timestamp = sid = rid = text = mediaurl = url = expanded = display = rtimestamp = rsenderid = reactkey = reventid = idc = '' 
        
    
            if data_list:
                report = ArtifactHtmlReport(f'Twitter Returns - {filenamenoext}')
                report.start_artifact_report(report_folder, f'Twitter Returns - {filenamenoext}')
                report.add_script()
                data_headers = ('Created At', 'Conversation ID', 'Sender ID', 'Recipient ID', 'Text', 'Media', 'Media URL', 'URL', 'Expanded URL', 'Display URL', 'Reaction Timestamp', 'Reaction Sender ID', 'Reaction', 'Reaction Event ID', 'ID')
                report.write_artifact_data_table(data_headers, data_list, filenamedms, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Twitter Returns - {filenamenoext}'
                tsv(report_folder, data_list, data_headers, tsvname)
                
                tlactivity = f'Twitter Returns - {filenamenoext}'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc(f'No Twitter Returns - {filenamenoext}')
                
        if filename.endswith('-account-creation-ip.txt'):
            data_list = []
            filenamedms = file_found
            filenamenoext = (filename.split('-', 1)[1].replace('.txt','').strip())
            with open(file_found, 'r', encoding='utf-8') as f:	
                
                    for line in f:
                        if '"accountId"' in line:
                            accountid = line.split(': ')[1].replace(',', '').replace('"', '').strip()
                            
                        elif '"userCreationIp"' in line:
                            ucip = line.split(': ')[1].replace(',', '').replace('"', '').strip()
                            
                            data_list.append((accountid, ucip))
                            
            if data_list:
                report = ArtifactHtmlReport(f'Twitter Returns - {filenamenoext}')
                report.start_artifact_report(report_folder, f'Twitter Returns - {filenamenoext}')
                report.add_script()
                data_headers = ('Account ID','User Creation IP')
                report.write_artifact_data_table(data_headers, data_list, filenamedms, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Twitter Returns - {filenamenoext}'
                tsv(report_folder, data_list, data_headers, tsvname)
                
            else:
                logfunc(f'No Twitter Returns - {filenamenoext}')
        
        if filename.endswith('-account-suspension.txt'):
            data_list = []
            filenamedms = file_found
            filenamenoext = (filename.split('-', 1)[1].replace('.txt','').strip())
            with open(file_found, 'r', encoding='utf-8') as f:	
                
                    for line in f:
                        if '"timeStamp"' in line:
                            timestamp = timestamps(line)
                        elif '"action"' in line:
                            action = line.split(': ')[1].replace('"', '').strip()
                            
                            data_list.append((timestamp, action))
                            
            if data_list:
                report = ArtifactHtmlReport(f'Twitter Returns - {filenamenoext}')
                report.start_artifact_report(report_folder, f'Twitter Returns - {filenamenoext}')
                report.add_script()
                data_headers = ('Timestamp','Action')
                report.write_artifact_data_table(data_headers, data_list, filenamedms, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Twitter Returns - {filenamenoext}'
                tsv(report_folder, data_list, data_headers, tsvname)
                
                tlactivity = f'Twitter Returns - {filenamenoext}'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc(f'No Twitter Returns - {filenamenoext}')
                
        if filename.endswith('-account.txt'):
            data_list = []
            filenamedms = file_found
            filenamenoext = (filename.split('-', 1)[1].replace('.txt','').strip())
            with open(file_found, 'r', encoding='utf-8') as f:	
                email = timestamp = accountid = cvia = usern = accdn = ''
                for line in f:
                    if '"createdAt"' in line:
                        timestamp = timestamps(line)
                    elif '"accountId"' in line:
                        accountid = line.split(': ')[1].replace('"', '').replace(',', '').strip()
                    elif '"email" :' in line:
                        email = line.split(': ')[1].replace('"', '').replace(',', '').strip()
                    elif '"createdVia"' in line:
                        cvia = line.split(': ')[1].replace('"', '').replace(',', '').strip()
                    elif '"username"' in line:
                        usern = line.split(': ')[1].replace('"', '').replace(',', '').strip()
                    elif '"accountDisplayName"' in line:
                        accdn = line.split(': ')[1].replace('"', '').strip()
                    
                data_list.append((timestamp, accountid, email, cvia, usern, accdn))
                            
            if data_list:
                report = ArtifactHtmlReport(f'Twitter Returns - {filenamenoext}')
                report.start_artifact_report(report_folder, f'Twitter Returns - {filenamenoext}')
                report.add_script()
                data_headers = ('Created At','Account ID', 'Email', 'Created Via', 'Username', 'Account Display Name')
                report.write_artifact_data_table(data_headers, data_list, filenamedms, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Twitter Returns - {filenamenoext}'
                tsv(report_folder, data_list, data_headers, tsvname)
                
                tlactivity = f'Twitter Returns - {filenamenoext}'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc(f'No Twitter Returns - {filenamenoext}')
                
        if filename.endswith('-ageinfo.txt'):
            data_list = []
            filenamedms = file_found
            filenamenoext = (filename.split('-', 1)[1].replace('.txt','').strip())
            with open(file_found, 'r', encoding='utf-8') as f:	
                
                    for line in f:
                        if  '"age" :' in line:
                            line = line.strip()
                            if line.endswith(']'):
                                age = ''
                            else:
                                extraline = next(f)
                                age = extraline.replace('"', '').strip()
                        elif '"birthDate"' in line:
                            birth = line.split(': ')[1].replace('"', '').strip()
                            
                            data_list.append((birth, age))
                            
            if data_list:
                report = ArtifactHtmlReport(f'Twitter Returns - {filenamenoext}')
                report.start_artifact_report(report_folder, f'Twitter Returns - {filenamenoext}')
                report.add_script()
                data_headers = ('Birthdate', 'Age')
                report.write_artifact_data_table(data_headers, data_list, filenamedms, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Twitter Returns - {filenamenoext}'
                tsv(report_folder, data_list, data_headers, tsvname)
                
            else:
                logfunc(f'No Twitter Returns - {filenamenoext}')
        
        if filename.endswith('-block.txt'):
            data_list = []
            filenamedms = file_found
            filenamenoext = (filename.split('-', 1)[1].replace('.txt','').strip())
            with open(file_found, 'r', encoding='utf-8') as f:	
                
                    for line in f:
                        if '"accountId"' in line:
                            accountid = line.split(': ')[1].replace('"', '').replace(',', '').strip()                        
                        elif '"userLink"' in line:
                            userl = line.split(': ')[1].replace('"', '').strip()
                            
                            data_list.append((accountid, userl))
                            
            if data_list:
                report = ArtifactHtmlReport(f'Twitter Returns - {filenamenoext}')
                report.start_artifact_report(report_folder, f'Twitter Returns - {filenamenoext}')
                report.add_script()
                data_headers = ('Account ID', 'User Link')
                report.write_artifact_data_table(data_headers, data_list, filenamedms, html_no_escape=['User Link'])
                report.end_artifact_report()
                
                tsvname = f'Twitter Returns - {filenamenoext}'
                tsv(report_folder, data_list, data_headers, tsvname)
                
            else:
                logfunc(f'No Twitter Returns - {filenamenoext}')
        
        if filename.endswith('-device-token.txt'):
            data_list = []
            filenamedms = file_found
            filenamenoext = (filename.split('-', 1)[1].replace('.txt','').strip())
            with open(file_found, 'r', encoding='utf-8') as f:	
                
                    for line in f:
                        if '"token" :' in line:
                            token = line.split(': ')[1].replace('"', '').replace(',', '').strip()
                        elif '"lastSeenAt"' in line:
                            lastseen = timestamps(line)
                        elif '"clientApplicationId"' in line:
                            clientappid = line.split(': ')[1].replace('"', '').replace(',', '').strip()
                        elif '"clientApplicationName"' in line:
                            clientappname = line.split(': ')[1].replace('"', '').replace(',', '').strip()
                        elif '"createdAt"' in line:
                            timestampt = timestamps(line)
                            
                            data_list.append((timestampt, lastseen, clientappid, clientappname, token))
                            
            if data_list:
                report = ArtifactHtmlReport(f'Twitter Returns - {filenamenoext}')
                report.start_artifact_report(report_folder, f'Twitter Returns - {filenamenoext}')
                report.add_script()
                data_headers = ('Created At', 'Last Seen At', 'Client Application ID', 'Client Application Name', 'Token')
                report.write_artifact_data_table(data_headers, data_list, filenamedms, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Twitter Returns - {filenamenoext}'
                tsv(report_folder, data_list, data_headers, tsvname)
                
                tlactivity = f'Twitter Returns - {filenamenoext}'
                timeline(report_folder, tlactivity, data_list, data_headers)
                
            else:
                logfunc(f'No Twitter Returns - {filenamenoext}')
        
        if filename.endswith('-follower.txt'):
            data_list = []
            filenamedms = file_found
            filenamenoext = (filename.split('-', 1)[1].replace('.txt','').strip())
            with open(file_found, 'r', encoding='utf-8') as f:	
                
                    for line in f:
                        if '"accountId"' in line:
                            accountid = line.split(': ')[1].replace('"', '').replace(',', '').strip()                        
                        elif '"userLink"' in line:
                            userl = line.split(': ')[1].replace('"', '').strip()
                            
                            data_list.append((accountid, userl))
                            
            if data_list:
                report = ArtifactHtmlReport(f'Twitter Returns - {filenamenoext}')
                report.start_artifact_report(report_folder, f'Twitter Returns - {filenamenoext}')
                report.add_script()
                data_headers = ('Account ID', 'User Link')
                report.write_artifact_data_table(data_headers, data_list, filenamedms, html_no_escape=['User Link'])
                report.end_artifact_report()
                
                tsvname = f'Twitter Returns - {filenamenoext}'
                tsv(report_folder, data_list, data_headers, tsvname)
                
            else:
                logfunc(f'No Twitter Returns - {filenamenoext}')
                
        if filename.endswith('-following.txt'):
            data_list = []
            filenamedms = file_found
            filenamenoext = (filename.split('-', 1)[1].replace('.txt','').strip())
            with open(file_found, 'r', encoding='utf-8') as f:	
                
                    for line in f:
                        if '"accountId"' in line:
                            accountid = line.split(': ')[1].replace('"', '').replace(',', '').strip()                        
                        elif '"userLink"' in line:
                            userl = line.split(': ')[1].replace('"', '').strip()
                            
                            data_list.append((accountid, userl))
                            
            if data_list:
                report = ArtifactHtmlReport(f'Twitter Returns - {filenamenoext}')
                report.start_artifact_report(report_folder, f'Twitter Returns - {filenamenoext}')
                report.add_script()
                data_headers = ('Account ID', 'User Link')
                report.write_artifact_data_table(data_headers, data_list, filenamedms, html_no_escape=['User Link'])
                report.end_artifact_report()
                
                tsvname = f'Twitter Returns - {filenamenoext}'
                tsv(report_folder, data_list, data_headers, tsvname)
                
            else:
                logfunc(f'No Twitter Returns - {filenamenoext}')
                
        if filename.endswith('-ip-audit.txt'):
            data_list = []
            filenamedms = file_found
            filenamenoext = (filename.split('-', 1)[1].replace('.txt','').strip())
            with open(file_found, 'r', encoding='utf-8') as f:	
                
                    for line in f:
                        if '"accountId"' in line:
                            accid = line.split(': ')[1].replace('"', '').replace(',', '').strip()
                        elif '"createdAt"' in line:
                            timestampt = timestamps(line)
                        elif '"loginIp"' in line:
                            loginip = line.split(': ')[1].replace('"', '').replace(',', '').strip()
                            
                            data_list.append((timestampt, loginip,  accid))
                            
            if data_list:
                report = ArtifactHtmlReport(f'Twitter Returns - {filenamenoext}')
                report.start_artifact_report(report_folder, f'Twitter Returns - {filenamenoext}')
                report.add_script()
                data_headers = ('Created At', 'Login IP', 'Account ID')
                report.write_artifact_data_table(data_headers, data_list, filenamedms, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Twitter Returns - {filenamenoext}'
                tsv(report_folder, data_list, data_headers, tsvname)
                
                tlactivity = f'Twitter Returns - {filenamenoext}'
                timeline(report_folder, tlactivity, data_list, data_headers)
                
            else:
                logfunc(f'No Twitter Returns - {filenamenoext}')
                
        if filename.endswith('-like.txt'):
            data_list = []
            filenamedms = file_found
            filenamenoext = (filename.split('-', 1)[1].replace('.txt','').strip())
            with open(file_found, 'r', encoding='utf-8') as f:	
                
                    for line in f:
                        if '"tweetId"' in line:
                            tweetid = line.split(': ')[1].replace('"', '').replace(',', '').strip()
                        elif '"fullText"' in line:
                            fulltxt = line.split(': ')[1].replace('"', '').replace(',', '').strip()
                        elif '"expandedUrl"' in line:
                            expurl = line.split(': ')[1].replace('"', '').replace(',', '').strip()
                            
                            data_list.append((tweetid, fulltxt,  expurl))
                            
            if data_list:
                report = ArtifactHtmlReport(f'Twitter Returns - {filenamenoext}')
                report.start_artifact_report(report_folder, f'Twitter Returns - {filenamenoext}')
                report.add_script()
                data_headers = ('Tweet ID', 'Full Text', 'Expanded URL')
                report.write_artifact_data_table(data_headers, data_list, filenamedms, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Twitter Returns - {filenamenoext}'
                tsv(report_folder, data_list, data_headers, tsvname)
                
            else:
                logfunc(f'No Twitter Returns - {filenamenoext}')
                
        if filename.endswith('-mute.txt'):
            data_list = []
            filenamedms = file_found
            filenamenoext = (filename.split('-', 1)[1].replace('.txt','').strip())
            with open(file_found, 'r', encoding='utf-8') as f:	
                
                    for line in f:
                        if '"accountId"' in line:
                            accountid = line.split(': ')[1].replace('"', '').replace(',', '').strip()
                        elif '"userLink"' in line:
                            userl = line.split(': ')[1].replace('"', '').strip()
                            
                            data_list.append((accountid, userl))
                            
            if data_list:
                report = ArtifactHtmlReport(f'Twitter Returns - {filenamenoext}')
                report.start_artifact_report(report_folder, f'Twitter Returns - {filenamenoext}')
                report.add_script()
                data_headers = ('Account ID', 'User Link')
                report.write_artifact_data_table(data_headers, data_list, filenamedms, html_no_escape=['User Link'])
                report.end_artifact_report()
                
                tsvname = f'Twitter Returns - {filenamenoext}'
                tsv(report_folder, data_list, data_headers, tsvname)
                
            else:
                logfunc(f'No Twitter Returns - {filenamenoext}')
                
        if filename.endswith('-tweet.txt'):
            data_list = []
            filenamedms = file_found
            filenamenoext = (filename.split('-', 1)[1].replace('.txt','').strip())
            msgbase = 0
            mediabase = 0
            mediaagg = ''
            videomediaident = ''
            createdat = ''
            date = ''
            with open(file_found, 'r', encoding='utf-8') as f:	
                    for line in f:
                        if '**** id: ' in line:
                            if msgbase == 0:
                                msgbase = 1
                            else:
                                date = createdat.replace("'",'').strip().split(' ')
                                year = date[5]
                                month = monthletter(date[1])
                                day = date[2]
                                time = date[3]
                                date = (f'{year}-{month}-{day} {time}')
                                
                                mediabase = 0

                                data_list.append((date, fulltext, mediaagg, videomediaident))
                                date = ''
                                fulltxt = ''
                                mediaagg = ''
                                videomediaident = ''
                        elif "-----END PGP SIGNATURE-----" in line:
                            if date == '':
                                pass
                            else:
                                date = createdat.replace("'",'').strip().split(' ')
                                year = date[5]
                                month = monthletter(date[1])
                                day = date[2]
                                time = date[3]
                                date = (f'{year}-{month}-{day} {time}')
                                data_list.append((date, fulltext, mediaagg, videomediaident))
                        elif '"created_at" : ' in line:
                            createdat = line.split(': ')[1].replace(',', '').replace('"', '').strip()
                            
                        elif '"full_text" : ' in line:
                            fulltext = line.split(': "')[1].replace(',', '').replace('"', '').strip()
                        elif '"media_url" : ' in line:
                            if mediabase == 0:
                                mediabase = 1
                                mediaurl = ''
                            elif mediabase == 1:
                                mediaurl = line.split(': ')[1].replace(',','').replace('"', '').strip()
                                mediaurl = mediaurl.split(separator)[-1].split('.')[0]
                                
                                mediaurl = media_to_html(mediaurl, files_found, report_folder)
                                mediaagg = mediaurl
                                mediabase = 2
                            elif mediabase == 2:
                                mediaurl = line.split(': ')[1].replace(',','').replace('"', '').strip()
                                mediaurl = mediaurl.split(separator)[-1].split('.')[0]
                                mediaurl = media_to_html(mediaurl, files_found, report_folder)
                                mediaagg = mediaagg + '<br><br>' + mediaurl
                        elif '"bitrate" : "2176000"' in line:
                            extraline = next(f)
                            extraline = next(f)
                            videomedia = extraline.split(separator)[-1].split('?')[0]
                            videomedia = videomedia.replace('"','').strip()
                            videomediaident = videomedia.split(separator)[-1].split('?')[0]
                            videomediaident = media_to_html(videomediaident, files_found, report_folder)
                        
                        
            if data_list:
                report = ArtifactHtmlReport(f'Twitter Returns - {filenamenoext}')
                report.start_artifact_report(report_folder, f'Twitter Returns - {filenamenoext}')
                report.add_script()
                data_headers = ('Timestamp', 'Full Text', 'Media', 'Video')
                report.write_artifact_data_table(data_headers, data_list, filenamedms, html_no_escape=['Media','Video'])
                report.end_artifact_report()
                
                tsvname = f'Twitter Returns - {filenamenoext}'
                tsv(report_folder, data_list, data_headers, tsvname)
                
                tlactivity = f'Twitter Returns - {filenamenoext}'
                timeline(report_folder, tlactivity, data_list, data_headers)
                
            else:
                logfunc(f'No Twitter Returns - {filenamenoext}')

__artifacts__ = {
        "twitterReturnsTip": (
            "Twitter Returns",
            ('*/*.jpg','*/*.mp4','*/*.txt'),
            get_twitterReturnsTip)
}
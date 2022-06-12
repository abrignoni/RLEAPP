import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html

def get_twitterReturnsTip(files_found, report_folder, seeker, wrap_text):
    
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
                            date = (line.split('T'))
                            
                            dateall = (date[0].split(': "')[1].split('-'))
                            year = (dateall[0])
                            month = (dateall[1])
                            day = (dateall[2])
                            
                            hours = (date[1].split(':')[0])
                            minutes = (date[1].split(':')[1])
                            seconds = (date[1].split(':')[2].replace('Z"','').replace(',','').strip())
                            
                            timestamp = f'{year}-{month}-{day} {hours}:{minutes}:{seconds}'
                            #print(timestamp)
                            
                        elif  '"mediaUrls" :' in line:
                            line = line.strip()
                            if line.endswith('[ ],'):
                                mediaurl = ''
                                thumb = ''
                            else:
                                extraline = next(f)
                                mediaurl = extraline.replace('"','').strip()
                                if 'ton' in mediaurl:
                                    mediaident = mediaurl.split('/')[-1]
                                elif 'video' in mediaurl:
                                    mediaident = mediaurl.split('/')[-1].split('?')[0]
                                thumb = media_to_html(mediaident, files_found, report_folder)
                                
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
                                date = (extraline.split('T'))
                                
                                dateall = (date[0].split(': "')[1].split('-'))
                                year = (dateall[0])
                                month = (dateall[1])
                                day = (dateall[2])
                                
                                hours = (date[1].split(':')[0])
                                minutes = (date[1].split(':')[1])
                                seconds = (date[1].split(':')[2].replace('Z"','').strip())
                                
                                rtimestamp = f'{year}-{month}-{day} {hours}:{minutes}:{seconds}'
                                #print(rtimestamp)
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
        
import os
import datetime
import json
import shutil
from bs4 import BeautifulSoup
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows, utf8_in_extended_ascii, media_to_html

def get_fbigUnifiedmessaging(files_found, report_folder, seeker, wrap_text, time_offset):
    data_list = []
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        rfilename = filename
        
        if filename.startswith('records.html') or filename.startswith('preservation'):
            with open(file_found, encoding='utf-8') as fp:
                soup = BeautifulSoup(fp, 'lxml')
                
            threadparticipants = []
            threadid = currpar = pastpar = ''
            control = 0
            controlt = 0
            data_list = []
            autor = sent = body = attach = typef = sizef = url = lmf = pt = dcf = textf = urlb = subsevent = ''
            agg = set()
            lmftime = 0
            # Find all divs with class "div_table inner"
            divs = soup.find_all("div", class_="div_table inner")
            # Extract and print text from each div in the order they appear
            for div in divs:
                text = div.get_text(separator='|', strip=True)
                text = text.split('|')
                if text[0] == 'Thread':
                    if controlt == 0:
                        threadid = text[1]
                        controlt = 1
                    elif  controlt == 1:
                        threadparticipants.append((threadid,currpar,pastpar))
                        threadid = currpar = pastpar = ''
                        threadid = text[1]
                elif text[0] == 'Current Participants':
                    currpar = div
                elif text[0] == 'Past Participants':
                    pastpar = div
                if text[0] == 'Author':
                    #print(text[1], control)
                    if control == 0:
                        author = (text[1])
                        control = 1
                    elif control == 1:
                        for x in agg:
                            x = media_to_html(x, files_found, report_folder)
                            lmf = lmf + x + '<br><br>'
                        data_list.append((sent,author,body,lmf,attach,typef,sizef,url,pt,dcf,textf,urlb,subsevent,threadid))
                        autor = sent = body = attach = typef = sizef = url = lmf = pt = dcf = textf = urlb = subsevent = ''
                        agg.clear()
                        author = (text[1])
                elif text[0] == 'Sent':
                    #print(div)
                    sent = (text[1])
                    
                elif text[0] == 'Body':
                    if len(text) == 1:
                        body = ''
                    else:
                        body = text[1]
                elif text[0] == 'Attachments':
                    attach = (text[1])
                elif text[0] == 'Type':
                    typef = (text[1])
                elif text[0] == 'Size':
                    if len(text) == 1:
                        sizef = ''
                    else:
                        sizef = text[1]
                elif text[0] == 'URL':
                    if len(text) == 1:
                        url = ''
                    else:
                        url = text[1]
                elif text[0] == 'Product Type':
                    pt = (text[1])
                elif text[0] == 'Date Created':
                    if len(text) == 1:
                        dcf = ''
                    else:
                        dcf = text[1]
                elif text[0] == 'Text':
                    if len(text) == 1:
                        textf = ''
                    else:
                        textf = text[1]
                elif text[0] == 'Linked Media File:':
                    if lmftime == sent:
                        agg.add(text[1])
                    else:
                        agg.clear()
                        agg.add(text[1])
                        lmftime = sent
                elif text[0] == 'Url':
                    urlb = (text[1])
                elif text[0] == 'Subscription Event':
                    subsevent = div
                else:
                    pass
                    #print(text[0],text[1])
                    
                    #print(text)
                
                    
                    
            data_list.append((sent,author,body,lmf,attach,typef,sizef,url,pt,dcf,textf,urlb,subsevent,threadid))
            threadparticipants.append((threadid,currpar,pastpar))
    
            if data_list:
                reportnumber = 1
                data_list.sort(key=lambda x: (x[1], x[0]))
                chunk_size = 10000
                for i in range(0, len(data_list), chunk_size):
                    chunk = data_list[i:i + chunk_size]
                    
                    start = str(i)
                    end = i + chunk_size
                    end = str(end)
                    
                    report = ArtifactHtmlReport(f'Facebook & Instagram - Unified Messaging - {rfilename} - {reportnumber}')
                    report.start_artifact_report(report_folder, f'Facebook Instagram - Unified Messaging - {rfilename} - {reportnumber}')
                    report.add_script()
                    data_headers = ('Timestamp','Author','Body','Linked Media File','Attachments','Type','Size', 'URL','Product Type','Date Created Share','Text','Url','Subscription Event','Thread ID')
                    report.write_artifact_data_table(data_headers, chunk, file_found, html_no_escape=['Linked Media File','Subscription Event'])
                    report.end_artifact_report()
                    
                    tsvname = f'Facebook Instagram - Unified Messaging - {rfilename} - {reportnumber}'
                    tsv(report_folder, data_headers, chunk, tsvname)
                    
                    tlactivity = f'Facebook Instagram - Unified Messaging - {rfilename} - {reportnumber}'
                    timeline(report_folder, tlactivity, chunk, data_headers)
                    
                    reportnumber = reportnumber + 1
        
            else:
                logfunc(f'No Facebook Instagram - Unified Messaging - {rfilename}')
            
            if len(threadparticipants) > 0:
                report = ArtifactHtmlReport(f'Facebook & Instagram - Thread Participants  - {rfilename}')
                report.start_artifact_report(report_folder, f'Facebook Instagram - Thread Participants  - {rfilename}')
                report.add_script()
                data_headers = ('Thread ID','Current Participants','Past Participants')
                report.write_artifact_data_table(data_headers, threadparticipants, file_found, html_no_escape=['Current Participants','Past Participants'])
                report.end_artifact_report()
                
                tsvname = f'Facebook Instagram - Thread Participants - {rfilename}'
                tsv(report_folder, data_headers, threadparticipants, tsvname)
                
            else:
                logfunc(f'No Facebook & Instagram Thread Participants - {rfilename}')
        else:
            pass
__artifacts__ = {
        "fbigUnifiedmessaging": (
            "Facebook - Instagram Returns",
            ('*/records.html', '*/preservation*.html', '*/linked_media/*.*'),
            get_fbigUnifiedmessaging)
}
import os
import datetime
import json
import magic
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
    
        if filename.startswith('index.html') or filename.startswith('preservation'):
            rfilename = filename
            file_to_report_data = file_found
            data_list = []
            with open(file_found, encoding='utf-8') as fp:
                soup = BeautifulSoup(fp, 'html.parser')
            #<div id="property-unified_messages" class="content-pane">
            uni = soup.find_all("div", {"id": "property-unified_messages"})
            
            control = 0
            itemsdict = {}
            lmf = []
            for x in uni:
                tables = x.find_all("table")
                
                for table in tables:
                    thvalue = (table.find('th').get_text())
                    tdvalue = (table.find('th').find_next_sibling("td").get_text())
                    
                    if thvalue == 'Unified Messages':
                        for subtable in table.find_all('table'):
                            thvalue = (subtable.find('th').get_text())
                            tdvalue = (subtable.find('th').find_next_sibling("td").get_text())
                            wtag = subtable.find('th').find_next_sibling("td")
                            wtag = str(wtag)
                            if thvalue == 'Thread':
                                split = tdvalue.split(')')
                                threadid = split[0].replace('(','').strip()
                            else:
                                wtag = wtag.replace('<td>', '').replace('</td>', '').strip()
                                if thvalue == 'Current Participants':
                                    current_part = wtag
                                elif thvalue == 'Share':
                                    pass
                                elif thvalue == 'Attachments':
                                    pass
                                else:
                                    if thvalue == 'Author':
                                        author = tdvalue
                                        
                                        itemsdict['author'] = author
                                        if control == 0:
                                            control = 1
                                        else:
                                            itemsdict['threadid'] = threadid
                                            current_split = current_part.split('<br/>', 1)
                                            ag = ''
                                            for current_items in current_split[1:]:
                                                ag = ag + current_items
                                            itemsdict['currentpart'] = ag.strip()
                                            if len(lmf) > 0:
                                                counterl = 0
                                                agregator = agregator + ('<table>')
                                                for item in lmf:
                                                    if counterl == 0:
                                                        agregator = agregator +('<tr>')
                                                
                                                    thumb = media_to_html(item, files_found, report_folder)
                                                    
                                                    counterl = counterl + 1
                                                    agregator = agregator + f'<td>{thumb}</td>'
                                                    #hacer uno que no tenga html
                                                    if counterl == 2:
                                                        counterl = 0
                                                        agregator = agregator + ('</tr>')
                                                if counterl == 1:
                                                    agregator = agregator + ('</tr>')
                                                agregator = agregator + ('</table><br>')
                                            else:
                                                agregator = ''
                                                
                                            data_list.append((itemsdict.get('sent', ''),itemsdict.get('threadid', ''), itemsdict.get('currentpart', ''), itemsdict.get('author', ''), itemsdict.get('body', ''), itemsdict.get('missed', ''), itemsdict.get('duration', ''), agregator, itemsdict.get('summary', ''), itemsdict.get('title', ''), itemsdict.get('url', '') ))
                                            #print(lmf)
                                            #to do: check lmf in dictionary, pull and find the files to attach to the report
                                            agregator = ''
                                            itemsdict = {}
                                            lmf = []
                                    elif thvalue == 'Sent':
                                        sent = tdvalue
                                        itemsdict['sent'] = sent.replace('UTC', '').strip()
                                    elif thvalue == 'Body':
                                        body = tdvalue
                                        itemsdict['body'] = body
                                    elif thvalue == 'Date Created':
                                        dcreated = tdvalue
                                        itemsdict['dcreated'] = dcreated
                                    elif thvalue == 'Summary':
                                        summary = tdvalue
                                        itemsdict['summary'] = summary
                                    elif thvalue == 'Title':
                                        title = tdvalue
                                        itemsdict['title'] = title
                                    elif thvalue == 'Url':
                                        url = tdvalue
                                        itemsdict['url'] = url
                                    elif thvalue == 'Duration':
                                        duration = tdvalue
                                        itemsdict['duration'] = duration
                                    elif thvalue == 'Missed':
                                        missed = tdvalue
                                        itemsdict['missed'] = missed
                                    elif thvalue == 'Attachments':
                                        attach = tdvalue
                                        itemsdict['attach'] = attach
                                    elif thvalue == 'Linked Media File:':
                                        lmf.append(tdvalue)
                                        itemsdict['lmf'] = lmf
                                    else:
                                        pass
                        itemsdict['author'] = author
                        itemsdict['threadid'] = threadid
                        current_split = current_part.split('<br/>', 1)
                        ag = ''
                        for current_items in current_split[1:]:
                            ag = ag + current_items
                        itemsdict['currentpart'] = ag.strip()
                        data_list.append((itemsdict.get('sent', ''),itemsdict.get('threadid', ''),itemsdict.get('currentpart', ''), itemsdict.get('author', ''), itemsdict.get('body', ''),  itemsdict.get('missed', ''), itemsdict.get('duration', ''), agregator, itemsdict.get('summary', ''), itemsdict.get('title', ''), itemsdict.get('url', '') ))
        
        if filename.startswith('index.html') or filename.startswith('preservation'):
            if data_list:
                report = ArtifactHtmlReport(f'Facebook & Instagram - Unified Messaging - {rfilename}')
                report.start_artifact_report(report_folder, f'Facebook Instagram - Unified Messaging - {rfilename}')
                report.add_script()
                data_headers = ('Timestamp','Thread ID','Current Participants', 'Author', 'Body', 'Missed','Duration', 'Linked Media File','Summary', 'Title', 'URL' )
                report.write_artifact_data_table(data_headers, data_list, file_to_report_data, html_no_escape=['Current Participants', 'Linked Media File'])
                report.end_artifact_report()
                
                tsvname = f'Facebook Instagram - Unified Messaging - {rfilename}'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                tlactivity = f'Facebook Instagram - Unified Messaging - {rfilename}'
                timeline(report_folder, tlactivity, data_list, data_headers)
        
            else:
                logfunc(f'No Facebook Instagram - Unified Messaging - {rfilename}')
                
__artifacts__ = {
        "fbigUnifiedmessaging": (
            "Facebook - Instagram Returns",
            ('*/index.html', '*/preservation*.html', '*/linked_media/unified_message_*'),
            get_fbigUnifiedmessaging)
}
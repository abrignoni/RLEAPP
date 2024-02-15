import os
import datetime
import json
import shutil
from bs4 import BeautifulSoup
from pathlib import Path

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows, utf8_in_extended_ascii, media_to_html

def get_fbigArchiveStories(files_found, report_folder, seeker, wrap_text, time_offset):
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
                
            uni = soup.find_all("div", {"id": "property-archived_stories"})
            
            control = 0
            agg = ''
            
            for x in uni:
                tables = x.find_all("table")
                
                for table in tables:
                    thvalue = (table.find('th').get_text())
                    tdvalue = (table.find('th').find_next_sibling("td").get_text())
                    
                    if thvalue == 'Archived Stories':
                        pass
                    elif thvalue == 'Story Id':
                        storyid = tdvalue
                    elif thvalue == 'Timestamp':
                        time = tdvalue
                    elif thvalue == 'Linked Media File:':
                        media = tdvalue.split('/')[1]
                        thumb = media_to_html(media,files_found, report_folder)
                        data_list.append((time,storyid,tdvalue,thumb))
                
        if data_list:
            report = ArtifactHtmlReport(f'Facebook & Instagram - Archived Stories - {rfilename}')
            report.start_artifact_report(report_folder, f'Facebook Instagram - Archived Stories - {rfilename}')
            report.add_script()
            data_headers = ('Timestamp','Story ID','Filename','Thumb' )
            report.write_artifact_data_table(data_headers, data_list, file_to_report_data, html_no_escape=['Thumb'])
            report.end_artifact_report()
            
            tsvname = f'Facebook Instagram - Archived Stories - {rfilename}'
            tsv(report_folder, data_headers, data_list, tsvname)
        
        else:
            logfunc(f'No Facebook Instagram - Archived Stories - {rfilename}')
                
__artifacts__ = {
        "fbigArchiveStories": (
            "Facebook - Instagram Returns",
            ('*/index.html', '*/preservation*.html', '*/linked_media/archived_stories_*'),
            get_fbigArchiveStories)
}
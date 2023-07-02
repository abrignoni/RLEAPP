import os
import datetime
import json
import magic
import shutil
from bs4 import BeautifulSoup
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows, utf8_in_extended_ascii, media_to_html

def get_fbigVideos(files_found, report_folder, seeker, wrap_text):
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
                
            uni = soup.find_all("div", {"id": "property-videos"})
            
            control = 0
            agg = ''
            
            for x in uni:
                tables = x.find_all("table")
                
                for table in tables:
                    
                    
                    thvalue = (table.find('th').get_text())
                    tdvalue = (table.find('th').find_next_sibling("td"))
                    
                    if thvalue == 'Videos Definition':
                        pass
                    elif thvalue == 'User:':
                        pass
                    elif thvalue == 'Text:':
                        pass
                    elif thvalue == 'Time:':
                        pass
                    elif thvalue == 'Videos':
                        pass
                    elif thvalue == 'Video':
                        pass
                    elif thvalue == 'Linked Media File:':
                        if control == 0:
                            media = tdvalue.get_text().split('/')[1]
                            thumb = media_to_html(media,files_found, report_folder)
                            control = 1
                        else:
                            data_list.append((media,thumb,agg))
                            agg  = ''
                            media = tdvalue.get_text().split('/')[1]
                            thumb = media_to_html(media,files_found, report_folder)
                    else:
                        agg = agg + f"<table>{table.find('th')} {tdvalue}</table>"
                data_list.append((media,thumb,agg))
                
        if data_list:
            report = ArtifactHtmlReport(f'Facebook & Instagram - Videos - {rfilename}')
            report.start_artifact_report(report_folder, f'Facebook Instagram - Videos - {rfilename}')
            report.add_script()
            data_headers = ('Filename','Thumb','Data' )
            report.write_artifact_data_table(data_headers, data_list, file_to_report_data, html_no_escape=['Thumb','Data'])
            report.end_artifact_report()
            
            #tsvname = f'Facebook Instagram - Videos - {rfilename}'
            #tsv(report_folder, data_headers, data_list, tsvname)
        
        else:
            logfunc(f'No Facebook Instagram - Videos - {rfilename}')
                
__artifacts__ = {
        "fbigVideos": (
            "Facebook - Instagram Returns",
            ('*/index.html', '*/preservation*.html', '*/linked_media/videos_*'),
            get_fbigVideos)
}
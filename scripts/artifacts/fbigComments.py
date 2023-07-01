import os
import datetime
import json
import magic
import shutil
from bs4 import BeautifulSoup
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows, utf8_in_extended_ascii, media_to_html

def get_fbigComments(files_found, report_folder, seeker, wrap_text):
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
                
            uni = soup.find_all("div", {"id": "property-comments"})
            
            control = 0
            itemsdict = {}
            lmf = []
            for x in uni:
                tables = x.find_all("table")
                
                for table in tables:
                    thvalue = (table.find('th').get_text())
                    tdvalue = (table.find('th').find_next_sibling("td").get_text())
                    
                    if thvalue == 'Comments':
                        dataagg = []
                        for subtable in table.find_all('table'):
                            thvalue = (subtable.find('th').get_text())
                            tdvalue = (subtable.find('th').find_next_sibling("td").get_text())
                            
                            if control < 5:
                                control = control+1
                                if thvalue == 'Id':
                                    id = tdvalue
                                if thvalue == 'Date Created':
                                    date = tdvalue
                                if thvalue == 'Status':
                                    status = tdvalue
                                if thvalue == 'Text':
                                    text = tdvalue
                                if thvalue == 'Media Content Id':
                                    mediacont = tdvalue
                                if thvalue == 'Media Owner':
                                    mediaown = tdvalue
                            else:
                                control = 0
                                if thvalue == 'Media Owner':
                                    mediaown = tdvalue
                                data_list.append((date,id,status,text,mediacont,mediaown))
        
        if data_list:
            report = ArtifactHtmlReport(f'Facebook & Instagram - Comments - {rfilename}')
            report.start_artifact_report(report_folder, f'Facebook Instagram - Comments - {rfilename}')
            report.add_script()
            data_headers = ('Timestamp','ID','Status', 'Text', 'Media Account ID', 'Media Owner' )
            report.write_artifact_data_table(data_headers, data_list, file_to_report_data, html_no_escape=['Current Participants', 'Linked Media File'])
            report.end_artifact_report()
            
            tsvname = f'Facebook Instagram - Comments - {rfilename}'
            tsv(report_folder, data_headers, data_list, tsvname)
            
            tlactivity = f'Facebook Instagram - Comments- {rfilename}'
            timeline(report_folder, tlactivity, data_list, data_headers)
        
        else:
            logfunc(f'No Facebook Instagram - Comments - {rfilename}')
                
__artifacts__ = {
        "fbigComments": (
            "Facebook - Instagram Returns",
            ('*/index.html', '*/preservation*.html'),
            get_fbigComments)
}
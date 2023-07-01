import os
import datetime
import json
import magic
import shutil
from bs4 import BeautifulSoup
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows, utf8_in_extended_ascii, media_to_html

def get_fbigFollowers(files_found, report_folder, seeker, wrap_text):
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
                
            uni = soup.find_all("div", {"id": "property-followers"})
            
            control = 0
            itemsdict = {}
            lmf = []
            for x in uni:
                tables = x.find_all("table")
                
                for table in tables:
                    thvalue = (table.find('th').get_text())
                    tdvalue = (table.find('th').find_next_sibling("td"))
                    tdvalue = ((str(tdvalue).split('<br/>')))
                    
            for x in tdvalue:
                x = x.strip('<td>')
                x = x.strip('</td>')
                data_list.append((x,))
        
        if data_list:
            report = ArtifactHtmlReport(f'Facebook & Instagram - Followers - {rfilename}')
            report.start_artifact_report(report_folder, f'Facebook Instagram - Followers - {rfilename}')
            report.add_script()
            data_headers = ('User', )
            report.write_artifact_data_table(data_headers, data_list, file_to_report_data, html_no_escape=['Current Participants', 'Linked Media File'])
            report.end_artifact_report()
            
            tsvname = f'Facebook Instagram - Followers - {rfilename}'
            tsv(report_folder, data_headers, data_list, tsvname)
        
        else:
            logfunc(f'No Facebook Instagram - Followers - {rfilename}')
                
__artifacts__ = {
        "fbigFollowers": (
            "Facebook - Instagram Returns",
            ('*/index.html', '*/preservation*.html'),
            get_fbigFollowers)
}
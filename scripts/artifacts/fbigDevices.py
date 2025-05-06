import os
import datetime
import json
import shutil
from bs4 import BeautifulSoup
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows, utf8_in_extended_ascii, media_to_html

def get_fbigDevices(files_found, report_folder, seeker, wrap_text):
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
                
            uni = soup.find_all("div", {"id": "property-devices"})
            
            control = 0
            itemsdict = {}
            lmf = []
            for x in uni:
                tables = x.find_all("table")
                
                for table in tables:
                    thvalue = (table.find('th').get_text())
                    tdvalue = (table.find('th').find_next_sibling("td").get_text())
                    
                    if thvalue == 'Devices':
                        for subtable in table.find_all('table'):
                            thvalue = (subtable.find('th').get_text())
                            tdvalue = (subtable.find('th').find_next_sibling("td").get_text())
                            
                            if control < 4:
                                control = control+1
                                if thvalue == 'Type':
                                    typeof = tdvalue
                                if thvalue == 'Id':
                                    idof = tdvalue
                                if thvalue == 'Active':
                                    active = tdvalue
                                    data_list.append((typeof,idof,active,''))
                            else:
                                control = 0
                            if thvalue == 'User':
                                user = tdvalue
                                data_list.append(('','','',user))
        
        if data_list:
            report = ArtifactHtmlReport(f'Facebook & Instagram - Devices - {rfilename}')
            report.start_artifact_report(report_folder, f'Facebook Instagram - Devices - {rfilename}')
            report.add_script()
            data_headers = ('Type','ID','Active', 'User' )
            report.write_artifact_data_table(data_headers, data_list, file_to_report_data, html_no_escape=['Current Participants', 'Linked Media File'])
            report.end_artifact_report()
            
            tsvname = f'Facebook Instagram - Devices - {rfilename}'
            tsv(report_folder, data_headers, data_list, tsvname)
        
        else:
            logfunc(f'No Facebook Instagram - Devices - {rfilename}')
                
__artifacts__ = {
        "fbigDevices": (
            "Facebook - Instagram Returns",
            ('*/index.html', '*/preservation*.html'),
            get_fbigDevices)
}
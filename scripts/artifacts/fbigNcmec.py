import os
import datetime
import json
import magic
import shutil
from bs4 import BeautifulSoup
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows, utf8_in_extended_ascii, media_to_html

def get_fbigNcmec(files_found, report_folder, seeker, wrap_text, time_offset):
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
                
            uni = soup.find_all("div", {"id": "property-ncmec_reports"})
            
            control = 0
            agg = ''
            
            for x in uni:
                tables = x.find_all("table")
                
                for table in tables:
                    
                    
                    thvalue = (table.find('th').get_text())
                    tdvalue = (table.find('th').find_next_sibling("td").get_text())
                    thvalue = str(thvalue)
                    tdvalue = str(tdvalue)
                    
                    
                    if thvalue == 'Ncmec Reports Definition':
                        pass
                    elif thvalue == 'NCMEC Cybertips':
                        pass
                    elif thvalue == 'Media uploaded in this cybertip':
                        pass
                    elif thvalue == 'CyberTip ID':
                        if control == 0:
                            cybertipid = tdvalue
                            control = 1
                        else:
                            data_list.append((time,cybertipid,resid,agg))
                            agg  = ''
                            cybertipid = tdvalue
                    elif thvalue == 'Time':
                        time = tdvalue
                    elif thvalue == 'Responsible Id':
                        resid = tdvalue
                    else:
                        if thvalue == 'Linked Media File:':
                            media = tdvalue.split('/')[1]
                            tdvalue = media_to_html(media,files_found, report_folder)
                        agg = agg + f'{thvalue} {tdvalue} <br>'
                        
                data_list.append((time,cybertipid,resid,agg))
                
        if data_list:
            report = ArtifactHtmlReport(f'Facebook & Instagram - NECMEC Reports - {rfilename}')
            report.start_artifact_report(report_folder, f'Facebook Instagram - NECMEC Reports - {rfilename}')
            report.add_script()
            data_headers = ('Time','CyberTip ID','Responsible ID','Data' )
            report.write_artifact_data_table(data_headers, data_list, file_to_report_data, html_no_escape=['Data'])
            report.end_artifact_report()
            
            tsvname = f'Facebook Instagram - NECMEC Reports - {rfilename}'
            tsv(report_folder, data_headers, data_list, tsvname)
        
        else:
            logfunc(f'No Facebook Instagram - NECMEC Reports - {rfilename}')
                
__artifacts__ = {
        "fbigNcmec": (
            "Facebook - Instagram Returns",
            ('*/index.html', '*/preservation*.html', '*/linked_media/ncmec_reports_*'),
            get_fbigNcmec)
}
import os
import datetime
import json
import shutil
from bs4 import BeautifulSoup
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows, utf8_in_extended_ascii, media_to_html

def get_fbigLikes(files_found, report_folder, seeker, wrap_text, time_offset):
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
                
            uni = soup.find_all("div", {"id": "property-likes"})
            #print(uni)
            control = 0
            idd = taken = status = url = source = fil = ispub = sba = ui = ci = ''
            for x in uni:
                tables = x.find_all("table")
                
                for table in tables:
                    
                    thvalue = (table.find('th').get_text())
                    tdvalue = (table.find('th').find_next_sibling("td").get_text())
                    
                    if thvalue == 'likes':
                        pass
                    else:
                        for subtable in table.find_all('table'):
                            thvalue = (subtable.find('th').get_text())
                            tdvalue = (subtable.find('th').find_next_sibling("td").get_text())
                            
                            #print(thvalue, tdvalue)
                            
                            if thvalue == 'Id':
                                if control == 0:
                                    idd = tdvalue
                                    control = 1
                                else:
                                    data_list.append((taken,idd,status,url,source,fil,ispub,sba,ui,ci))
                                    idd = taken = status = url = source = fil = ispub = sba = ui = ci = ''
                                    idd = tdvalue
                            if thvalue == 'Taken':
                                taken = tdvalue
                            if thvalue == 'Status':
                                status = tdvalue
                            if thvalue == 'Url':
                                url = tdvalue
                            if thvalue == 'Source':
                                source = tdvalue
                            if thvalue == 'Filter':
                                fil = tdvalue
                            if thvalue == 'Is Published':
                                ispub = tdvalue
                            if thvalue == 'Shared By Author':
                                sba = tdvalue
                            if thvalue == 'Upload Ip':
                                ui = tdvalue
                            if thvalue == 'Carousel Id':
                                ci = tdvalue
                                
                data_list.append((taken,idd,status,url,source,fil,ispub,sba,ui,ci))
                
        if data_list:
            report = ArtifactHtmlReport(f'Facebook & Instagram - Likes - {rfilename}')
            report.start_artifact_report(report_folder, f'Facebook Instagram - Likes - {rfilename}')
            report.add_script()
            data_headers = ('Timestamp','ID','Status','URL','Source','Filter','Is Published','Shared By Author','Upload IP','Carousel Id')
            report.write_artifact_data_table(data_headers, data_list, file_to_report_data, html_no_escape=['Current Participants', 'Linked Media File'])
            report.end_artifact_report()
            
            tsvname = f'Facebook Instagram - Likes - {rfilename}'
            tsv(report_folder, data_headers, data_list, tsvname)
        
        else:
            logfunc(f'No Facebook Instagram - Likes - {rfilename}')
                
__artifacts__ = {
        "fbigLikes": (
            "Facebook - Instagram Returns",
            ('*/index.html', '*/preservation*.html'),
            get_fbigLikes)
}
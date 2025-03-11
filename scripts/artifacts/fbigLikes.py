import os
import datetime
import json
import shutil
from bs4 import BeautifulSoup
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows, utf8_in_extended_ascii, media_to_html

def get_fbigLikes(files_found, report_folder, seeker, wrap_text):
    data_list = []
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        rfilename = filename
        
        if filename.startswith('records.html') or filename.startswith('preservation'):
            with open(file_found, encoding='utf-8') as fp:
                soup = BeautifulSoup(fp, 'lxml')
                
            data_list = []
            controlt = 0
            id = taken = status = vanity = ltime = url = source = filter = ispub = sba = uip = cid = ''
            
            uni = soup.find_all("div", {"id": "property-likes"})
            
            divs = uni[0].find_all('div', class_='div_table inner')
            
            for index, div in enumerate(divs):
                if index > 1:
                    text = div.get_text(separator='|', strip=True)
                    text = text.split('|')
                    if text[0] == 'Id':
                        if controlt == 0:
                            ids = text[1]
                            controlt = 1
                        elif  controlt == 1:
                            data_list.append((taken,ids,status,vanity,ltime,url,source,filter,ispub,cid,sba,uip))
                            ids = taken = status = vanity = ltime = url = source = filter = ispub = sba = uip = cid = ''
                            ids = text[1]
                    elif text[0] == 'Taken':
                        taken = text[1]
                    elif text[0] == 'Status':
                        status = text[1]
                    elif text[0] == 'Liked Post Author Vanity':
                        vanity = text[1]
                    elif text[0] == 'Like Timestamp':
                        ltime = text[1]
                    elif text[0] == 'Url':
                        url = text[1]
                    elif text[0] == 'Source':
                        source = text[1]
                    elif text[0] == 'Filter':
                        filter = text[1]
                    elif text[0] == 'Is Published':
                        ispub = text[1]
                    elif text[0] == 'Carousel Id':
                        cid = text[1]
                    elif text[0] == 'Shared By Author':
                        sba = text[1]
                    elif text[0] == 'Upload Ip':
                        uip = text[1]
                    else:
                        print(text[0],text[1])
                        
            data_list.append((taken,ids,status,vanity,ltime,url,source,filter,ispub,cid,sba,uip))
                
            if data_list:
                report = ArtifactHtmlReport(f'Facebook & Instagram - Likes - {rfilename}')
                report.start_artifact_report(report_folder, f'Facebook Instagram - Likes - {rfilename}')
                report.add_script()
                data_headers = ('Timestamp','ID','Status','Vanity','Like Timestamp','URL','Source','Filter','Is Published','Carousel Id','Shared By Author','Upload IP')
                report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Current Participants', 'Linked Media File'])
                report.end_artifact_report()
                
                tsvname = f'Facebook Instagram - Likes - {rfilename}'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                tlactivity = f'Facebook Instagram - Likes - {rfilename}'
                timeline(report_folder, tlactivity, data_list, data_headers)
            
            else:
                logfunc(f'No Facebook Instagram - Likes - {rfilename}')
                
__artifacts__ = {
        "fbigLikes": (
            "Facebook - Instagram Returns",
            ('*/records.html', '*/preservation*.html'),
            get_fbigLikes)
}
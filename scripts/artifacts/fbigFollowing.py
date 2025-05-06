import os
import datetime
import json
import shutil
from bs4 import BeautifulSoup
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows, utf8_in_extended_ascii, media_to_html

def get_fbigFollowing(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
    
        if filename.startswith('records.html') or filename.startswith('preservation'):
            rfilename = filename
            
            with open(file_found, encoding='utf-8') as fp:
                soup = BeautifulSoup(fp, 'lxml')
            
            data_list = []
            uni = soup.find_all("div", {"id": "property-following"})
            divs = uni[0].find_all('div', class_='div_table inner')
            
            for index, div in enumerate(divs):
                if index > 0:
                    divinn = (div.find('div', class_='most_inner'))
                    divinn = str(divinn)
                    #divtext = (divinn.get_text())
                    divinn = divinn.replace('<div class="most_inner">','')
                    divinn = divinn.replace('<div>','')
                    divinn = divinn.replace('</div>','')
                    divinn = divinn.split('<br/>')

                    for x in divinn:
                        data_list.append((x,))
        
        if divinn:
            report = ArtifactHtmlReport(f'Facebook & Instagram - Following - {rfilename}')
            report.start_artifact_report(report_folder, f'Facebook Instagram - Following - {rfilename}')
            report.add_script()
            data_headers = ('User', )
            report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=[''])
            report.end_artifact_report()
            
            tsvname = f'Facebook Instagram - Following - {rfilename}'
            tsv(report_folder, data_headers, data_list, tsvname)
        
        else:
            logfunc(f'No Facebook Instagram - Following - {rfilename}')
                
__artifacts__ = {
        "fbigFollowing": (
            "Facebook - Instagram Returns",
            ('*/records.html', '*/preservation*.html'),
            get_fbigFollowing)
}
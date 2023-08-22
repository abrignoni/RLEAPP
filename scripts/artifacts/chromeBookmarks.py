# Module Description: Parses Google Chrome bookmarks from Takeout
# Author: @KevinPagano3
# Date: 2023-08-21
# Artifact version: 0.0.1
# Requirements: none

import datetime
import os
import textwrap
import bs4

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_chromeBookmarks2(files_found, report_folder, seeker, wrap_text):

    for file_found in files_found:
        file_found = str(file_found)
        filename = os.path.basename(file_found)

        with open(file_found, encoding='utf-8') as fp:
            soup = bs4.BeautifulSoup(fp.read(), 'html.parser')
            
        data_list = []
        dt = soup.find_all('dt')
        
        add_date = ''
        last_modified = ''
        title = ''
        url = ''
        folder_name = ''
        
        for i in dt:
            n = i.find_next()
            if n.name == 'h3':
                folder_name = n.text
                title = n.text
                add_date = n.get('add_date','')
                if add_date == '0' or len(add_date) == 0:
                    add_date = ''
                else:
                    if len(add_date) == 13:
                        add_date = datetime.datetime.fromtimestamp(int(add_date)/1000).strftime('%Y-%m-%d %H:%M:%S')  
                    else:
                        add_date = datetime.datetime.fromtimestamp((int(add_date)/1000000)-11644473600).strftime('%Y-%m-%d %H:%M:%S')
                
                last_modified = n.get('last_modified','')
                if last_modified == '0' or len(last_modified) == 0:
                    last_modified = ''
                else:    
                    last_modified = datetime.datetime.fromtimestamp(int(last_modified)/1000).strftime('%Y-%m-%d %H:%M:%S')
                
                data_list.append((add_date,last_modified,title,'',''))
                add_date = ''
                last_modified = ''
                title = ''
                continue
            else:
                url = n.get('href','')
                title = n.text
                add_date = n.get('add_date','')
                if len(add_date) == 13:
                    add_date = datetime.datetime.fromtimestamp(int(add_date)/1000).strftime('%Y-%m-%d %H:%M:%S')  
                else:
                    add_date = datetime.datetime.fromtimestamp((int(add_date)/1000000)-11644473600).strftime('%Y-%m-%d %H:%M:%S')
                last_modified = n.get('last_modified','')
                if last_modified == '0' or len(last_modified) == 0:
                    last_modified = ''
                else:    
                    last_modified = datetime.datetime.fromtimestamp(int(last_modified)/1000).strftime('%Y-%m-%d %H:%M:%S')  
                
                data_list.append((add_date,last_modified,title,url,folder_name))

        num_entries = len(data_list)
        if num_entries > 0:
            report = ArtifactHtmlReport('Chrome Bookmarks')
            report.start_artifact_report(report_folder, 'Chrome Bookmarks')
            report.add_script()
            data_headers = ('Added Timestamp','Last Modified','Title','URL','Parent Folder Name')

            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()

            tsvname = f'Chrome Bookmarks'
            tsv(report_folder, data_headers, data_list, tsvname)

            tlactivity = f'Chrome Bookmarks'
            timeline(report_folder, tlactivity, data_list, data_headers)
        else:
            logfunc('No Chrome Bookmarks data available')

__artifacts__ = {
        "chromeBookmarks2": (
            "Google Takeout Archive",
            ('*/Chrome/Bookmarks.html'),
            get_chromeBookmarks2)
}
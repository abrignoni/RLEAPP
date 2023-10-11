# Module Description: Parses Google Chrome reading list from Takeout
# Author: @KevinPagano3
# Date: 2023-08-24
# Artifact version: 0.0.1
# Requirements: none

import datetime
import os
import textwrap
import bs4

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_chromeReadingList(files_found, report_folder, seeker, wrap_text, time_offset):

    for file_found in files_found:
        file_found = str(file_found)
        filename = os.path.basename(file_found)

        with open(file_found, encoding='utf-8') as fp:
            soup = bs4.BeautifulSoup(fp.read(), 'html.parser')
            
        data_list = []
        dt = soup.find_all('dt')
        
        for i in dt:
            n = i.find_next()
            url = n.get('href','')
            title = n.text
            add_date = n.get('add_date','')
            add_date = datetime.datetime.utcfromtimestamp((int(add_date)/1000000)).strftime('%Y-%m-%d %H:%M:%S')
                
            data_list.append((add_date,title,url))
            
        num_entries = len(data_list)
        if num_entries > 0:
            report = ArtifactHtmlReport('Chrome Reading List')
            report.start_artifact_report(report_folder, 'Chrome Reading List')
            report.add_script()
            data_headers = ('Added Timestamp','Title','URL')

            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()

            tsvname = f'Chrome Reading List'
            tsv(report_folder, data_headers, data_list, tsvname)

            tlactivity = f'Chrome Reading List'
            timeline(report_folder, tlactivity, data_list, data_headers)
        else:
            logfunc('No Chrome Reading List data available')

__artifacts__ = {
        "chromeReadingList": (
            "Google Takeout Archive",
            ('*/Chrome/ReadingList.html'),
            get_chromeReadingList)
}

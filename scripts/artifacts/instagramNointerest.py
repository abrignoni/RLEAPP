import os
import datetime
import json
import magic
import shutil
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows, utf8_in_extended_ascii, media_to_html

def get_instagramNointerest(files_found, report_folder, seeker, wrap_text, time_offset):
    data_list = []
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith("accounts_you're_not_interested_in.json"):
            
            with open(file_found, "r") as fp:
                deserialized = json.load(fp)
        
            for x in deserialized['impressions_history_recs_hidden_authors']:
                value = x['string_map_data']['Username'].get('value', '')
                timestamp = x['string_map_data']['Time'].get('timestamp', '')
                if timestamp > 0:
                    timestamp = (datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
                
                data_list.append((timestamp, value))
    
                
    if data_list:
        report = ArtifactHtmlReport('Instagram Archive - Accounts No Interest')
        report.start_artifact_report(report_folder, 'Instagram Archive - Accounts No Interest')
        report.add_script()
        data_headers = ('Timestamp','Username')
        report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Media'])
        report.end_artifact_report()
        
        tsvname = f'Instagram Archive - Accounts No Interest'
        tsv(report_folder, data_headers, data_list, tsvname)
        
        tlactivity = f'Instagram Archive - Accounts No Interest'
        timeline(report_folder, tlactivity, data_list, data_headers)

    else:
        logfunc('No Instagram Archive - Accounts No Interest')
                
__artifacts__ = {
        "instagramNointerest": (
            "Instagram Archive",
            ('*/ads_and_content/*re_not_interested_in.json'),
            get_instagramNointerest)
}
import os
import datetime
import json
import shutil
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows, utf8_in_extended_ascii, media_to_html

def get_instagramSearches(files_found, report_folder, seeker, wrap_text):
    data_list = []
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('account_searches.json'):
            
            with open(file_found, "r") as fp:
                deserialized = json.load(fp)
        
            for x in deserialized['searches_user']:
                search = x['string_map_data']['Search'].get('value', '')
                timestamp = x['string_map_data']['Time'].get('timestamp', '')
                if timestamp > 0:
                    timestamp = (datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
                
                data_list.append((timestamp, search))
    
                
    if data_list:
        report = ArtifactHtmlReport('Instagram Archive - Searches')
        report.start_artifact_report(report_folder, 'Instagram Archive - Searches')
        report.add_script()
        data_headers = ('Timestamp', 'Search')
        report.write_artifact_data_table(data_headers, data_list, file_found)
        report.end_artifact_report()
        
        tsvname = f'Instagram Archive - Searches'
        tsv(report_folder, data_headers, data_list, tsvname)
        
        tlactivity = f'Instagram Archive - Searches'
        timeline(report_folder, tlactivity, data_list, data_headers)

    else:
        logfunc('No Instagram Archive - Searches data available')
                
__artifacts__ = {
        "instagramSearches": (
            "Instagram Archive",
            ('*/recent_searches/account_searches.json'),
            get_instagramSearches)
}
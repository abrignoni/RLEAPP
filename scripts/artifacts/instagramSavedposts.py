import os
import datetime
import json
import magic
import shutil
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows, utf8_in_extended_ascii, media_to_html

def get_instagramSavedposts(files_found, report_folder, seeker, wrap_text):
    data_list = []
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('saved_posts.json'):
            
            with open(file_found, "r") as fp:
                deserialized = json.load(fp)
        
            for x in deserialized['saved_saved_media']:
                by = x['string_map_data']['Shared By'].get('value', '')
                href = x['string_map_data']['Shared By'].get('href', '')
                timestamp = x['string_map_data']['Shared By'].get('timestamp', '')
                if timestamp > 0:
                    timestamp = (datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
                    
                data_list.append((timestamp, by, href))
    
                
    if data_list:
        report = ArtifactHtmlReport('Instagram Archive - Saved Posts')
        report.start_artifact_report(report_folder, 'Instagram Archive - Saved Posts')
        report.add_script()
        data_headers = ('Timestamp', 'By', 'HREF')
        report.write_artifact_data_table(data_headers, data_list, file_found)
        report.end_artifact_report()
        
        tsvname = f'Instagram Archive - Saved Posts'
        tsv(report_folder, data_headers, data_list, tsvname)
        
        tlactivity = f'Instagram Archive - Saved Posts'
        timeline(report_folder, tlactivity, data_list, data_headers)

    else:
        logfunc('No Instagram Archive - Saved Posts data available')
                
        
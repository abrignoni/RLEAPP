import os
import datetime
import json
import shutil
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows

def get_instagramPostcom(files_found, report_folder, seeker, wrap_text, time_offset):
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
    
        if filename.startswith("post_comments.json"):
            data_list =[]
            with open(file_found, "rb") as fp:
                deserialized = json.load(fp)
                
            items = (deserialized['comments_media_comments'])
            for x in items:
                #print(x)
                title = (x.get('title', ''))
                hrefval = (x['string_list_data'][0].get('value', ''))
                timestamp = (x['string_list_data'][0].get('timestamp', ''))
                if timestamp > 0:
                    timestamp = (datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
                    
                data_list.append((timestamp, title, hrefval))
                
            if data_list:
                report = ArtifactHtmlReport('Instagram Archive - Post Comments')
                report.start_artifact_report(report_folder, 'Instagram Archive - Post Comments')
                report.add_script()
                data_headers = ('Timestamp', 'Title', 'Comment')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Instagram Archive - Post Comments'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                tlactivity = f'Instagram Archive - Post Comments'
                timeline(report_folder, tlactivity, data_list, data_headers)
                
            else:
                logfunc('No Instagram Archive - Post Comments data available')
                
__artifacts__ = {
        "instagramPostcom": (
            "Instagram Archive",
            ('*/comments/post_comments.json'),
            get_instagramPostcom)
}
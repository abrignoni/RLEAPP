import os
import datetime
import json
import magic
import shutil
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows, utf8_in_extended_ascii, media_to_html

def get_instagramPolls(files_found, report_folder, seeker, wrap_text):
    data_list = []
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('polls.json'):
            
            with open(file_found, "r") as fp:
                deserialized = json.load(fp)
        
            for x in deserialized['story_activities_polls']:
                user = x.get('title', '')
                timestamp = x['string_list_data'][0].get('timestamp', '')
                if timestamp > 0:
                    timestamp = (datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'))             
                
                data_list.append((timestamp, user))
    
                
    if data_list:
        report = ArtifactHtmlReport('Instagram Archive - Polls')
        report.start_artifact_report(report_folder, 'Instagram Archive - Polls')
        report.add_script()
        data_headers = ('Timestamp','User')
        report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Media'])
        report.end_artifact_report()
        
        tsvname = f'Instagram Archive - Polls'
        tsv(report_folder, data_headers, data_list, tsvname)
        
        tlactivity = f'Instagram Archive - Polls'
        timeline(report_folder, tlactivity, data_list, data_headers)

    else:
        logfunc('No Instagram Archive - Polls')
                
__artifacts__ = {
        "instagramPolls": (
            "Instagram Archive",
            ('*/story_sticker_interactions/polls.json'),
            get_instagramPolls)
}
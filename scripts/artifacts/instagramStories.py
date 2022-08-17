import os
import datetime
import json
import magic
import shutil
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows, utf8_in_extended_ascii, media_to_html

def get_instagramStories(files_found, report_folder, seeker, wrap_text):
    data_list = []
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('stories.json'):
            
            with open(file_found, "r") as fp:
                deserialized = json.load(fp)
        
            for x in deserialized['ig_stories']:
                title = x.get('title', '')
                uri = x.get('uri', '')
                timestamp = x.get('creation_timestamp', '')
                if timestamp > 0:
                    timestamp = (datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
                thumb = media_to_html(uri, files_found, report_folder)
                
                data_list.append((timestamp, title, thumb))
    
                
    if data_list:
        report = ArtifactHtmlReport('Instagram Archive - Stories')
        report.start_artifact_report(report_folder, 'Instagram Archive - Stories')
        report.add_script()
        data_headers = ('Timestamp','Title', 'Media')
        report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Media'])
        report.end_artifact_report()
        
        tsvname = f'Instagram Archive - Sotries'
        tsv(report_folder, data_headers, data_list, tsvname)
        
        tlactivity = f'Instagram Archive - Stories'
        timeline(report_folder, tlactivity, data_list, data_headers)

    else:
        logfunc('No Instagram Archive - Stories')
                
__artifacts__ = {
        "instagramStories": (
            "Instagram Archive",
            ('*/content/stories.json', '*/media/stories/*'),
            get_instagramStories)
}
import os
import datetime
import json
import magic
import shutil
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows, utf8_in_extended_ascii, media_to_html

def get_instagramInterests(files_found, report_folder, seeker, wrap_text):
    data_list = []
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('ads_interests.json'):
            
            with open(file_found, "r") as fp:
                deserialized = json.load(fp)
        
            for x in deserialized['inferred_data_ig_interest']:
                interest = x['string_map_data']['Interest'].get('value', '')      
                
                data_list.append((interest,))
    
                
    if data_list:
        report = ArtifactHtmlReport('Instagram Archive - Interests')
        report.start_artifact_report(report_folder, 'Instagram Archive - Interests')
        report.add_script()
        data_headers = ('Interests',)
        report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Media'])
        report.end_artifact_report()
        
        tsvname = f'Instagram Archive - Interests'
        tsv(report_folder, data_headers, data_list, tsvname)
        
        
    else:
        logfunc('No Instagram Archive - Interests')
                
        
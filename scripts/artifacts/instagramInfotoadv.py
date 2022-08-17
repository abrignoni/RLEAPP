import os
import datetime
import json
import magic
import shutil
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows

def get_instagramInfotoadv(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
    
        if filename.startswith("information_you've_submitted_to_advertisers.json"):
            data_list =[]
            with open(file_found, "rb") as fp:
                deserialized = json.load(fp)
                
            devices = (deserialized['ig_lead_gen_info'])
            for x in devices:
                label = x['label']
                value = x['value']
                    
                data_list.append((label, value))
                
            if data_list:
                report = ArtifactHtmlReport('Instagram Archive - Info Submitted to Adv ')
                report.start_artifact_report(report_folder, 'Instagram Archive - Info Submitted to Adv')
                report.add_script()
                data_headers = ('Label', 'Value')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Instagram Archive - Info Submitted to Adv'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                tlactivity = f'Instagram Archive - Info Submitted to Adv'
                timeline(report_folder, tlactivity, data_list, data_headers)
                
            else:
                logfunc('No Instagram Archive - Info Submitted to Adv data available')
                
__artifacts__ = {
        "instagramInfotoadv": (
            "Instagram Archive",
            ("*/ads_and_businesses/information_you've_submitted_to_advertisers.json"),
            get_instagramInfotoadv)
}
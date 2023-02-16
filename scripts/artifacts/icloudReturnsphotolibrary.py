import os
import datetime
import json
import magic
import shutil
import base64

from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows, media_to_html

def get_icloudReturnsphotolibrary(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        
        if is_platform_windows():
            separator = '\\'
        else:
            separator = '/'
            
        split_path = file_found.split(separator)
        account = (split_path[-3])
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('Metadata.txt'):
            #print(file_found)
            data_list =[]
            with open(file_found, "rb") as fp:
                data = json.load(fp)
                
            for deserialized in data:
                filenameEnc = deserialized['fields'].get('filenameEnc','Negative')
                isdeleted = deserialized['fields'].get('isDeleted')
                isexpunged = deserialized['fields'].get('isExpunged')
                originalcreationdate = deserialized['fields'].get('originalCreationDate')
        
                
                if (filenameEnc != 'Negative') and (filenameEnc is not None):
                    if isinstance(filenameEnc, dict):
                        filenameEnc = filenameEnc['value']
                    
                    filenamedec = (base64.b64decode(filenameEnc).decode('ascii'))
                    
                    if isinstance(originalcreationdate, dict):
                        originalcreationdate = originalcreationdate['value']
                        
                    originalcreationdatedec = (datetime.datetime.fromtimestamp(int(originalcreationdate)/1000).strftime('%Y-%m-%d %H:%M:%S'))
                    thumb = media_to_html(filenamedec, files_found, report_folder)
                    
                    data_list.append((originalcreationdatedec, thumb, filenamedec, filenameEnc, isdeleted, isexpunged))
                    
                
            if data_list:
                report = ArtifactHtmlReport(f'iCloud Returns - Photo Library - {account}')
                report.start_artifact_report(report_folder, f'iCloud Returns - Photo Library - {account}')
                report.add_script()
                data_headers = ('Timestamp', 'Media', 'Filename', 'Filename base64', 'Is Deleted', 'Is Expunged')
                report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'iCloud Returns - Photo Library - {account}'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                tlactivity = f'iCloud Returns - Photo Library - {account}'
                timeline(report_folder, tlactivity, data_list, data_headers)
                
            else:
                logfunc(f'No iCloud Returns - Photo Library - {account} data available')
                
__artifacts__ = {
        "icloudReturnsphotolibrary": (
            "iCloud Returns",
            ('*/*/cloudphotolibrary/*'),
            get_icloudReturnsphotolibrary)
}
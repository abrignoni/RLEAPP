import os
import datetime
import csv
import codecs
import shutil
import magic

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html

def get_kikProfilepic(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('profile-pic.jpg'):
            
            data_list =[]
            thumb = media_to_html(filename, files_found, report_folder)
            data_list.append((thumb, ))
                    
            if data_list:
                report = ArtifactHtmlReport('Kik - Profile Pic')
                report.start_artifact_report(report_folder, 'Kik - Profile Pic')
                report.add_script()
                data_headers = ('Profile Pic', )
                report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Profile Pic'])
                report.end_artifact_report()
                
            else:
                logfunc('No Kik Profile Pic data available')
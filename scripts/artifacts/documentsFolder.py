# Module Description: PDFs
# Author: infosec.exchange/@abrignoni
# Date: 2022-02-15
# Artifact version: 0.0.1
# Requirements: none

import os
import datetime
import magic

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html


def get_documentsFolder(files_found, report_folder, seeker, wrap_text):
    
    data_list = []

    for file_found in files_found:
        file_found = str(file_found)
        filename = os.path.basename(file_found)
        
    
        modified_time = os.path.getmtime(file_found)
        utc_modified_date = datetime.datetime.utcfromtimestamp(modified_time)
        
        if os.path.isfile(file_found):
            mime = magic.from_file(file_found, mime=True)
            ext = (mime.split('/')[1])
            
            linktofile = media_to_html(file_found, files_found, report_folder)
            if is_platform_windows:
                linktofile = linktofile.replace('/?','',1)
                
            data_list.append((utc_modified_date, filename, linktofile, ext, mime, file_found))
        
    if len(data_list) > 0:
        description = 'iCloud Documents Folders'
        note = 'Source location in extraction found in the report for each item.'
        report = ArtifactHtmlReport(f'iCloud Documents Folders')
        report.start_artifact_report(report_folder, f'iCloud Documents Folder', description)
        report.add_script()
        data_headers = ('Modified Date', 'Filename', 'Media', 'EXT', 'MIME', 'Path')

        report.write_artifact_data_table(data_headers, data_list, note, html_no_escape=['Media'])
        report.end_artifact_report()
        
        tsvname = f'iCloud Documents Folders'
        tsv(report_folder, data_headers, data_list, tsvname)
        
        tlactivity = f'iCloud Documents Folders'
        timeline(report_folder, tlactivity, data_list, data_headers)
        
    else:
        logfunc(f'No iCloud Documents Folders')

__artifacts__ = {
        "documentsFolder": (
            "iCloud Documents Folders",
            ('*/backup/*/Documents/**'),
            get_documentsFolder)
}
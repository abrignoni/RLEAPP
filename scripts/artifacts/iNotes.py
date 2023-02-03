import os
import datetime
import json

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html, kmlgen

def get_iNotes(files_found, report_folder, seeker, wrap_text):
    data_list = []

    for file_found in files_found:
        file_found = str(file_found)
    
        filename = os.path.basename(file_found)
        
        if file_found.endswith('Metadata.txt'):
            with open(file_found, 'r') as f:
                data = json.load(f)
                for x in data:
                    
                    recordname = (x['recordName'])
                    
                    created = (x['created'])
                    if created is not None:
                        created = created['timestamp']
                        created = datetime.datetime.fromtimestamp(created/1000)
                    
                    modified = (x['modified'])
                    if modified is not None:
                        modified = modified['timestamp']
                        modified = datetime.datetime.fromtimestamp(modified/1000)
                    
                    deleted = (x['deleted'])
                    participants = (x['participants'])
                    datas = ''
                    for match in files_found:
                        if recordname in match:
                            with open(match, 'r') as g:
                                datas = g.read()
                                datas = datas.replace('\n','<br>')
                    data_list.append((created, modified, datas, recordname, deleted, participants, match))
                        
        
    if data_list:
        note = 'Path for each note in the report. Timestamps possibly in Pacific Time'
        description = 'iOS Notes - Only Notes in text format'
        report = ArtifactHtmlReport(f'Notes - Text')
        report.start_artifact_report(report_folder, f'Notes - Text')
        report.add_script()
        data_headers = ('Timestamp Created','Timestamp Modified','Note','Record Name','Deleted?','Participants')
        report.write_artifact_data_table(data_headers, data_list, note, html_no_escape=['Note'])
        report.end_artifact_report()
        
        tsvname = f'Notes - Text'
        tsv(report_folder, data_headers, data_list, tsvname)
        
        tlactivity = f'Notes - Text'
        timeline(report_folder, tlactivity, data_list, data_headers)
    else:
        logfunc(f'No Notes - Text data available')
                
__artifacts__ = {
        "notesText": (
            "Apple Notes",
            ('*/Notes/Metadata.txt', '*/Notes/*/*.txt'),
            get_iNotes)
}
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
        
        if file_found.endswith('DS_Store'):
            continue
        
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
                    agregator = ''
                    notapath = ''
                    for match in files_found:
                        if match.endswith('.DS_Store'):
                            continue
                        if recordname in match:
                            if os.path.isfile(match):
                                if 'content' not in match:
                                    with open(match, 'r') as g:
                                        datas = g.read()
                                        datas = datas.replace('\n','<br>')
                                        thumb = media_to_html(match, files_found, report_folder)
                                        agregator = agregator + thumb + '<br><br>'
                                        notapath = match
                                if 'content' in match:
                                    thumb = media_to_html(match, files_found, report_folder)
                                    agregator = agregator + thumb + '<br><br>'
                                    notapath = match
                                
                                
                    data_list.append((created, modified, datas, recordname, agregator,deleted, participants, notapath))
                    
                        
        
    if data_list:
        note = 'Path for each note in the report. Timestamps possibly in Pacific Time'
        description = 'iOS Notes with attachments.'
        report = ArtifactHtmlReport(f'iOS Notes')
        report.start_artifact_report(report_folder, f'iOS Notes')
        report.add_script()
        data_headers = ('Timestamp Created','Timestamp Modified','Note','Record Name','Attachments', 'Deleted?','Participants','Source')
        report.write_artifact_data_table(data_headers, data_list, note, html_escape=False)
        report.end_artifact_report()
        
        tsvname = f'iOS Notes'
        tsv(report_folder, data_headers, data_list, tsvname)
        
        tlactivity = f'iOS Notes'
        timeline(report_folder, tlactivity, data_list, data_headers)
    else:
        logfunc(f'No iOS Notes data available')
                
__artifacts__ = {
        "iOSnotes": (
            "Apple Notes",
            ('*/Notes/Metadata.txt', '*/Notes/*/**'),
            get_iNotes)
}
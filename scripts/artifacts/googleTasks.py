# Module Description: Parses Google Tasks from Takeout
# Author: @KevinPagano3
# Date: 2022-04-28
# Artifact version: 0.0.1
# Requirements: none

import json
import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_googleTasks(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        if not os.path.basename(file_found) == 'Tasks.json': # skip -journal and other files
            continue

        with open(file_found, encoding = 'utf-8', mode = 'r') as f:
            data = json.loads(f.read())
        data_list = []

        for x in data['items']:
    
            tasklist_title = x.get('title','')
            tasklist_updated = x.get('updated','')
            
            for task in x['items']:
            
                task_created = task.get('created','').replace('T', ' ').replace('Z', '')
                task_due = task.get('due','').replace('T', ' ').replace('Z', '')
                task_updated = task.get('updated','').replace('T', ' ').replace('Z', '')
                task_title = task.get('title','')
                task_status = task.get('status','')
                task_id = task.get('id','')
                task_type = task.get('type','')
                
                data_list.append((task_created,task_updated,task_due,task_title,task_status,task_id,task_type,tasklist_title))
    
        num_entries = len(data_list)
        if num_entries > 0:
            description = 'List of tasks lists and tasks created in Google Task.'
            report = ArtifactHtmlReport('Google Tasks')
            report.start_artifact_report(report_folder, 'Google Tasks', description)
            report.add_script()
            data_headers = ('Task Created','Task Updated','Task Due','Task','Task Status','Task ID','Task Type','Tast List Name')

            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()
            
            tsvname = f'Google Tasks'
            tsv(report_folder, data_headers, data_list, tsvname)
            
            tlactivity = f'Google Tasks'
            timeline(report_folder, tlactivity, data_list, data_headers)
        else:
            logfunc('No Google Tasks data available')

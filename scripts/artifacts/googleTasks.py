# Module Description: Parses Google Tasks from Takeout
# Author: @KevinPagano3
# Date: 2022-04-28
# Artifact version: 0.0.3
# Requirements: none

import json
import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_googleTasks(files_found, report_folder, seeker, wrap_text, time_offset):
    
    for file_found in files_found:
        file_found = str(file_found)
        if not os.path.basename(file_found) == 'Tasks.json': # skip -journal and other files
            continue

        with open(file_found, encoding = 'utf-8', mode = 'r') as f:
            data = json.loads(f.read())
        
        parent_dict = {}
        id_list = []
        title_list = []
        data_list = []
        task_id = ''
        task_title = ''
        task_parent_title = ''
        task_created = ''
        task_due = ''
        task_updated = ''
        task_status = ''
        task_parent_id = ''
        task_type = ''
        task_notes = ''
        task_starred = ''
        
        for x in data['items']:
        
            tasklist_title = x.get('title','')
            tasklist_updated = x.get('updated','')

            if x.get('items','') != '':
                for parent_task in x['items']:
                    task_id = parent_task.get('id','')
                    task_title = parent_task.get('title','')
                    
                    id_list.append(task_id)
                    title_list.append(task_title)
            
                parent_dict = dict(zip(id_list,title_list))

                for task in x['items']:
                    task_created = task.get('created','').replace('T', ' ').replace('Z', '')
                    task_due = task.get('due','').replace('T', ' ').replace('Z', '')
                    task_updated = task.get('updated','').replace('T', ' ').replace('Z', '')
                    task_title = task.get('title','')
                    task_status = task.get('status','')
                    task_id = task.get('id','')
                    task_parent_id = task.get('parent','')
                    task_type = task.get('task_type','')
                    task_notes = task.get('notes','')
                    task_starred = task.get('starred','')
                    
                    if task_parent_id in parent_dict.keys():
                        task_parent_title = parent_dict.get(task_parent_id)
                        
                        data_list.append((task_created,task_updated,task_due,task_status,tasklist_title,task_parent_title,task_title,task_notes,task_type,task_parent_id,task_id,task_starred))
                    else:                     
                        data_list.append((task_created,task_updated,task_due,task_status,tasklist_title,"",task_title,task_notes,task_type,task_parent_id,task_id,task_starred))
                    
            else:
                data_list.append((task_created,task_updated,task_due,task_status,tasklist_title,task_parent_title,task_title,task_notes,task_type,task_parent_id,task_id,task_starred))
        
        num_entries = len(data_list)
        if num_entries > 0:
            description = 'List of tasks lists and tasks created in Google Task.'
            report = ArtifactHtmlReport('Google Tasks')
            report.start_artifact_report(report_folder, 'Google Tasks', description)
            report.add_script()
            data_headers = ('Task Created','Task Updated','Task Due','Task Status','Task List Name','Parent Task Name','Task Name','Notes','Task Type','Parent Task ID','Task ID','Favorited')

            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()
            
            tsvname = f'Google Tasks'
            tsv(report_folder, data_headers, data_list, tsvname)
            
            tlactivity = f'Google Tasks'
            timeline(report_folder, tlactivity, data_list, data_headers)
        else:
            logfunc('No Google Tasks data available')

__artifacts__ = {
        "googleTasks": (
            "Google Takeout Archive",
            ('*/Tasks/Tasks.json'),
            get_googleTasks)
}
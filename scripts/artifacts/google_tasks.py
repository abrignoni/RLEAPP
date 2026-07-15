__artifacts_v2__ = {
    "google_tasks": {
        "name": "Google Tasks",
        "description": "Parses Google Tasks from a Takeout archive includes tasks and task lists",
        "author": "@stark4n6",
        "creation_date": "2022-04-28",
        "last_update_date": "2026-06-01",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": ('*/Tasks/Tasks.json',),
        "output_types": "standard",  # or ["html", "tsv", "timeline", "lava"]
        "artifact_icon": "circle-check",
    }
}

import json
import os

from scripts.ilapfuncs import artifact_processor

@artifact_processor
def google_tasks(context):
    files_found = context.get_files_found()
    file_found = ''

    for file_found in files_found:
        file_found = str(file_found)
        if not os.path.basename(file_found) == 'Tasks.json':
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
    
    data_headers = (('Task Created','datetime'),('Task Updated','datetime'),('Task Due','datetime'),'Task Status','Task List Name','Parent Task Name','Task Name','Notes','Task Type','Parent Task ID','Task ID','Favorited')

    return data_headers, data_list, file_found

__artifacts_v2__ = {
    "OmegaChatMessages": {
        "name": "Omega Chat Messages",
        "description": "Parses Omega Chat Messages",
        "author": "Alexis Brigs Brignoni",
        "category": "Omega Chat",
        "notes": "",
        "paths": ('*/hicht.json'),
        "function": "get_OmegaChatMessages"
    }
}

import json
from datetime import timezone, datetime

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, timeline, tsv

def get_OmegaChatMessages(files_found, report_folder, seeker, wrap_text, timezone_offset):
    data_list = []  
    
    for file_found in files_found:
        file_found = str(file_found)
        
        
        if file_found.endswith('hicht.json'):
            with open(file_found, encoding='utf-8') as f:  
                data = f.read()
    
            data = json.loads(data)

            dictofusers = {}
            
            listofusers = data[2]
            for user in listofusers:
                userid = int(user)
                userdata = data[userid]
                indvid = userdata['id']
                del userdata['id']
                dictofusers[indvid] = userdata

            listofconvs = data[3]

            for conv in listofconvs:
                conv = int(conv)
                conversationMD = data[conv]
                convcreatedat = conversationMD['createdAt'] 
    
                contentindex = int(conversationMD['content'])
                content = data[contentindex]
    
                convindex = int(conversationMD['conversation'])
                conversation = data[convindex]
                userid = int(conversation['user_id'])
                userdata = dictofusers[userid]
    
                fname = int(userdata['first_name'])
                fname = data[fname]
                
                translate = conversationMD.get('translate')
                if translate is not None:
                    translate = int(translate)
                    translate = data[translate]

                convcreatedat = datetime.fromtimestamp(convcreatedat / 1000, tz=timezone.utc)
                data_list.append((convcreatedat, fname, content, translate))
        
    if data_list:
        description = 'Omega Chat Messages'
        report = ArtifactHtmlReport('Omega Chat Messages')
        report.start_artifact_report(report_folder, 'Omega Chat Messages', description)
        report.add_script()
        data_headers = ('createdAt', 'first_name', 'content', 'translate')
        report.write_artifact_data_table(data_headers, data_list, file_found, html_escape=False)
        report.end_artifact_report()
        
        tsvname = 'Omega Chat Messages'
        tsv(report_folder, data_headers, data_list, tsvname)
        
        tlactivity = 'Omega Chat Messages'
    




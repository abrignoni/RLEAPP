__artifacts_v2__ = {
    "OmegaChatAccount": {
        "name": "Omega Chat Account",
        "description": "Parses Omega Chat Account",
        "author": "Heather Charpentier",
        "category": "Omega Chat",
        "notes": "",
        "paths": ('*/hicht.json'),
        "function": "get_OmegaChatAccount"
    }
}

import json
from datetime import timezone, datetime

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, timeline, tsv

def get_OmegaChatAccount(files_found, report_folder, seeker, wrap_text, timezone_offset):
    data_list = []  
    
    for file_found in files_found:
        file_found = str(file_found)
        
        if file_found.endswith('hicht.json'):
            with open(file_found, encoding='utf-8') as f:  
                data = f.read()
    
            data = json.loads(data)

            dictofusers = {}
            
            users = data[8]
            for user in users:
                userid = int(user)
                userdata = data[userid]
                indvid = userdata.get('id')
                if indvid is not None:
                    dictofusers[indvid] = userdata

                actcreatedat = userdata.get('created_timestamp', 'Unknown')
                if actcreatedat != 'Unknown':
                    actcreatedat = datetime.fromtimestamp(actcreatedat, tz=timezone.utc)

                actno = int(userdata['mbx_uid'])
                actno = data[actno]

                fname = int(userdata['first_name'])
                fname = data[fname]
                
                bdate = int(userdata['birthday'])
                bdate = data[bdate]
                
                lat = userdata.get('lat', 'Unknown')
                
                lon = userdata.get('lon', 'Unknown')
                
                cit = int(userdata['city'])
                cit = data[cit]
                
                reg = int(userdata['region'])
                reg = data[reg]
                
                nat = int(userdata['nation'])
                nat = data[nat]
                
                gen = int(userdata['gender'])
                gen = data[gen]
                
                age = userdata.get('age', 'Unknown')

                data_list.append((actcreatedat, actno, fname, bdate, lat, lon, cit, reg, nat, gen, age))
        
    if data_list:
        description = 'Omega Chat Account'
        report = ArtifactHtmlReport('Omega Chat Account')
        report.start_artifact_report(report_folder, 'Omega Chat Account', description)
        report.add_script()
        data_headers = ('createdAt', 'mbx_uid', 'first_name', 'birthday', 'lat', 'lon', 'city', 'region', 'nation', 'gender', 'age')
        report.write_artifact_data_table(data_headers, data_list, file_found, html_escape=False)
        report.end_artifact_report()
        
        tsvname = 'Omega Chat Account'
        tsv(report_folder, data_headers, data_list, tsvname)
        
        tlactivity = 'Omega Chat Account'
        timeline(report_folder, tlactivity, data_list, data_headers)  
    
    else:
        logfunc('No Omega Chat Account data available')

    




__artifacts_v2__ = {
    "OmegaChatUsers": {
        "name": "Omega Chat Users",
        "description": "Parses Omega Chat Users",
        "author": "Heather Charpentier",
        "category": "Omega Chat",
        "notes": "",
        "paths": ('*/hicht.json'),
        "function": "get_OmegaChatUsers"
    }
}

import json
from datetime import timezone, datetime

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, timeline, tsv

def get_OmegaChatUsers(files_found, report_folder, seeker, wrap_text, timezone_offset):
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
    
                actno = int(userdata['mbx_uid'])
                actno = data[actno]
    
                fname = int(userdata['first_name'])
                fname = data[fname]
                
                bdate = int(userdata['birthday'])
                bdate = data[bdate]
                
                lat = int(userdata['lat'])
                lat = data[lat]
                
                lon = int(userdata['lon'])
                lon = data[lon]
                
                cit = int(userdata['city'])
                cit = data[cit]
                
                reg = int(userdata['region'])
                reg = data[reg]
                
                nat = int(userdata['nation'])
                nat = data[nat]
                
                gen = int(userdata['gender'])
                gen = data[gen]
                
                age = userdata.get('age', 'Unknown')
                               
                data_list.append((actno, fname, bdate, lat, lon, cit, reg, nat, gen, age))
        
    if data_list:
        description = 'Omega Chat Users'
        report = ArtifactHtmlReport('Omega Chat Users')
        report.start_artifact_report(report_folder, 'Omega Chat Users', description)
        report.add_script()
        data_headers = ('mbx_uid', 'first_name', 'birthday', 'lat', 'lon', 'city', 'region', 'nation', 'gender', 'age')
        report.write_artifact_data_table(data_headers, data_list, file_found, html_escape=False)
        report.end_artifact_report()
        
        tsvname = 'Omega Chat Users'
        tsv(report_folder, data_headers, data_list, tsvname)
        
        tlactivity = 'Omega Chat Users'
    




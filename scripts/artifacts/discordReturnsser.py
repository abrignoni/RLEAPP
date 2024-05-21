import os
import json

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html, kmlgen

def get_discordReturnsser(files_found, report_folder, seeker, wrap_text, time_offset):

    for file_found in files_found:
        file_found = str(file_found)
    
        filename = os.path.basename(file_found)
        csvname = filename
        
        if file_found.endswith('.json'):
            data_list_dm =[]
            with open(file_found, 'r', errors='backslashreplace') as f:
                data = json.load(f)
                
            id = data.get('id','')
            name = data.get('name','')
            owner_id = data.get('owner_id','')
            banner = data.get('banner','')
            preferred_locale = data.get('preferred_locale','')
            region = data.get('region','')
            splash = data.get('splash','')
            threads = data.get('threads','')
            channels = data.get('channels','')
            agregator = '<table>'
            if channels == '':
                pass
            else:
                for key, value in channels.items():
                    agregator = f'{agregator}<tr><td>{key}</td><td>{value}</td></tr>'
            agregator = f'{agregator} </table>'
            description = data.get('description','')
            icon = data.get('icon','')
            
            data_list_dm.append((name,description,agregator,banner,icon,id,owner_id,preferred_locale,region,threads))
            
                        
        
            if len(data_list_dm) > 1:
                report = ArtifactHtmlReport(f'Discord - Server Metadata ')
                report.start_artifact_report(report_folder, f'Discord - Server Metadata - {csvname}')
                report.add_script()
                data_headers = ('Name','Description','Channels','Banner','Icon ID','ID','Owner ID','Preferred Locale','Region','Threads')
                report.write_artifact_data_table(data_headers, data_list_dm, file_found, html_no_escape=['Channels'])
                report.end_artifact_report()
                
                tsvname = f'Discord - Server Metadata - {csvname}'
                tsv(report_folder, data_headers, data_list_dm, tsvname)
                
            else:
                logfunc(f'No data in Discord - Server Metadata - {csvname}')
                
__artifacts__ = {
        "discordReturnsser": (
            "Discord Returns",
            ('*/servers/*.json'),
            get_discordReturnsser)
}
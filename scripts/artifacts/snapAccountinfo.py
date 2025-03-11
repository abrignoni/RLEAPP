import os
import json

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html

def get_snapAccountinfo(files_found, report_folder, seeker, wrap_text):

    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        one = (os.path.split(file_found))
        username = (os.path.basename(one[0]))
        
        if filename.startswith('account.json'):
            data_list =[]
            with open(file_found, 'r') as fp:
                deserialized = json.load(fp)
            
            for key, value in deserialized.items():
                if key == 'Basic Information':
                    data_list_bi = []
                    data_list_bi.append((value['Creation Date'],value['Username'],value['Name'],value.get('Registration IP',''),value.get('Country',''),value.get('PhoneNumber',''),value.get('Carrier','')))
                    
                if key == 'Device Information':
                    data_list_di = []
                    data_list_di.append((value['Make'],value['Model ID'],value['Model Name'],value.get('User Agent',''),value['Language'],value['OS Type'],value['OS Version'],value['Connection Type']))
                    
                if key == 'Device History':
                    data_list_dh = []
                    for items in value:
                        data_list_dh.append((items['Start Time'],items['Make'],items['Model'],items['Device Type']))
                        
                if key == 'Login History':
                    data_list_lh = []
                    for items in value:
                        data_list_lh.append((items['Created'],items['IP'],items['Country'],items['Status'],items['Device']))
            
            if data_list_lh:
                report = ArtifactHtmlReport(f'Snapchat - Login History')
                report.start_artifact_report(report_folder, f'Snapchat - Login History')
                report.add_script()
                data_headers = ('Timestamp','IP','Country','Status','Device')
                report.write_artifact_data_table(data_headers, data_list_lh, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Login History'
                tsv(report_folder, data_headers, data_list_lh, tsvname)
                
                tlactivity = f'Snapchat - Login History'
                timeline(report_folder, tlactivity, data_list_lh, data_headers)
                    
            else:
                logfunc(f'No Snapchat - Login History')
            
            if data_list_di:
                report = ArtifactHtmlReport(f'Snapchat - Device History')
                report.start_artifact_report(report_folder, f'Snapchat - Device History')
                report.add_script()
                data_headers = ('Start Time','Make','Model','Device type')
                report.write_artifact_data_table(data_headers, data_list_di, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Device History'
                tsv(report_folder, data_headers, data_list_di, tsvname)
                
                tlactivity = f'Snapchat - Device History'
                timeline(report_folder, tlactivity, data_list_di, data_headers)
                
            else:
                logfunc(f'No Snapchat - Device History')
            
            if data_list_di:
                report = ArtifactHtmlReport(f'Snapchat - Device Information')
                report.start_artifact_report(report_folder, f'Snapchat - Device Information')
                report.add_script()
                data_headers = ('Make','Model ID','Model Name','User Agent','Language','OS Type','OS Version','Connection Type')
                report.write_artifact_data_table(data_headers, data_list_di, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Device Information'
                tsv(report_folder, data_headers, data_list_di, tsvname)
                
            else:
                logfunc(f'No Snapchat - Device Information')
            
            if data_list_bi:
                report = ArtifactHtmlReport(f'Snapchat - Account Basic Info')
                report.start_artifact_report(report_folder, f'Snapchat - Account Basic Info')
                report.add_script()
                data_headers = ('Timestamp','Username','Name','Registration IP','Country','Phone Number','Carrier')
                report.write_artifact_data_table(data_headers, data_list_bi, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Account Basic Info'
                tsv(report_folder, data_headers, data_list_bi, tsvname)
                
                tlactivity = f'Snapchat - Account Basic Info'
                timeline(report_folder, tlactivity, data_list_bi, data_headers)
                
            else:
                logfunc(f'No Snapchat - Account Basic Info')
            
        
            
    
__artifacts__ = {
        "snapAccountinfo": (
            "Snapchat Archive",
            ('*/account.json'),
            get_snapAccountinfo)
}
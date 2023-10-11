import os
import fitz

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_tikToksubsinfo(files_found, report_folder, seeker, wrap_text, time_offset):
    files = 0
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('~'):
            continue
        if filename.startswith('.'):
            continue
        
        subscriber = filename.split(' ')
        
        dth = []
        listtemp = []
        data_headers = []
        data_list =[]
        
        with fitz.open(file_found) as doc:
            text = ""
            for page in doc:
                pagedata = page.getText()
                
        items = pagedata.split('\n')
        username = registrationmethod = phone = registrationdate = registrationip = registrationdeviceinfo = ''
        for x in items:
            if x == ' ':
                continue
            else:
                value = x.strip()
                value = value.split(':')
                if 'username' in value[0]:
                    username = value[1].strip()
                elif 'registration method' in value[0]:
                    registrationmethod = value[1].strip()
                elif 'phone' in value[0]:
                    phone = value[1].strip()
                elif 'registration date' in value[0]:
                    registrationdate = f'{value[1].strip()}:{value[2]}:{value[3]}'
                elif 'registration ip' in value[0]:
                    registrationip = value[1].strip()
                elif 'registration device info' in value[0]:
                    registrationdeviceinfo = value[1].strip()
        
        data_list.append((registrationdate, username, registrationmethod, phone, registrationip, registrationdeviceinfo))
        
        if data_list:
            report = ArtifactHtmlReport(f'TikTok - Subscriber Info [{subscriber[0]}]')
            report.start_artifact_report(report_folder, f'TikTok - Subscriber Info [{subscriber[0]}]')
            report.add_script()
            data_headers = ('Registration Date','Username','Registration Method','Phone','Registration IP','Registration Device Info' )
            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()
            files = files + 1
        else:
            logfunc(f'No TikTok - Subscriber [{subscriber[0]}] available')

__artifacts__ = {
        "tikToksubsinfo": (
            "TikTok Returns",
            ('*/*/*(Subscriber information).pdf'),
            get_tikToksubsinfo)
}
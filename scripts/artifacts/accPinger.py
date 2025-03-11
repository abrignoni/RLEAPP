import os
import mammoth

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_accPinger(files_found, report_folder, seeker, wrap_text):
    data_list = []
    for file_found in files_found:
        file_found = str(file_found)
        filename = os.path.basename(file_found)
        
        if filename.startswith('~'):
            continue
        if filename.startswith('.'):
            continue
        
        loc = file_found
        
        
        with open(file_found, "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
            html = result.value 
            data_list.append((html,))
            
        
        if data_list:
            description = f'User account data'
            report = ArtifactHtmlReport('Pinger - Account')
            report.start_artifact_report(report_folder, 'Pinger - Account', description)
            report.add_script()
            data_headers = ('User Data',)
            report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['User Data'])
            report.end_artifact_report()
            
        else:
            logfunc('No Pinger Account data available')
            
__artifacts__ = {
        "Pinger Account": (
            "Pinger",
            ('*/*.docx'),
            get_accPinger)
}
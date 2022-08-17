import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_gooReturnsact(files_found, report_folder, seeker, wrap_text):
    
    data_list = []
    for file_found in files_found:
        file_found = str(file_found)
        
        with open(file_found, 'r') as file:	
            lines = file.readlines()
            header = 0
        for line in lines:
            if header == 0:
                line = line.strip()
                data_headers = line.split(',')
                topop = data_headers[0]
                data_headers.append(data_headers.pop(data_headers.index(topop)))
                header = 1
            else:
                line = line.strip()
                data = line.split(',')
                topop = data[0]
                data.append(data.pop(data.index(topop)))
                data_list.append(data)
        
    if len(data_list) > 0:
        description = ''
        report = ArtifactHtmlReport('Google Returns - Activities')
        report.start_artifact_report(report_folder, 'Google Returns - Activities', description)
        report.add_script()
        #data_headers = ('')

        report.write_artifact_data_table(data_headers, data_list, file_found)
        report.end_artifact_report()
        
        tsvname = f'Google Returns - Activities'
        tsv(report_folder, data_headers, data_list, tsvname)
        
        tlactivity = f'Google Returns - Activities'
        timeline(report_folder, tlactivity, data_list, data_headers)
    else:
        logfunc('No Google Returns - Activities data available')

__artifacts__ = {
        "gooReturnsact": (
            "Google Returns",
            ('*/Access Log Activity/Activities*.csv'),
            get_gooReturnsact)
}
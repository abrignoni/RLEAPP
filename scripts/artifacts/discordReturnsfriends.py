import os
import datetime
import csv
import calendar

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html, kmlgen

def get_discordReturnsfriends(files_found, report_folder, seeker, wrap_text):


    for file_found in files_found:
        file_found = str(file_found)
    
        filename = os.path.basename(file_found)
        csvname = filename
        
        if file_found.endswith('.csv'):
            data_list_dm =[]
            with open(file_found, 'r', errors='backslashreplace') as f:
                for line in f:
                    delimited = csv.reader(f, delimiter=',')
                    for item in delimited:
                        userid = item[0]
                        username = item[1]
                        relationship = item[2]
                        
                        data_list_dm.append((userid,username,relationship))
                        
        
            if data_list_dm:
                report = ArtifactHtmlReport(f'Discord - Friendships ')
                report.start_artifact_report(report_folder, f'Discord - Friendships - {csvname}')
                report.add_script()
                data_headers = ('User ID','Username','Relationship')
                report.write_artifact_data_table(data_headers, data_list_dm, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Discord - Friendships - {csvname}'
                tsv(report_folder, data_headers, data_list_dm, tsvname)
                
            else:
                logfunc(f'Discord - Friendships - {csvname}')
                
__artifacts__ = {
        "discordReturnsfriends": (
            "Discord Returns",
            ('*/relationships_*.csv'),
            get_discordReturnsfriends)
}
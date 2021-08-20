import os
import datetime
import json

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_instagramAccinfo(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('account_information.json'):
            data_list =[]
            data_list_timeline = []
            with open(file_found, "rb") as fp:
                deserialized = json.load(fp)
            for x in deserialized['profile_account_insights']:
                for key, values in x.items():
                    if values:
                        for a, b in values.items():
                            insightsCat = a
                            for c, d in b.items():
                                if c == 'href':
                                    href = d
                                if c == 'value':
                                    value = d
                                if c == 'timestamp':
                                    timestamp = d
                                    if timestamp > 0:
                                        timestamp = (datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
                            data_list.append((insightsCat,timestamp,value,href))
                            data_list_timeline.append((timestamp, insightsCat, href, value))
                    
                
            if data_list:
                report = ArtifactHtmlReport('Instagram Archive - Account Info')
                report.start_artifact_report(report_folder, 'Instagram Archive - Account Info')
                report.add_script()
                data_headers = ('Insights Category', 'Timestamp', 'Value', 'Href')
                data_headers_timeline = ( 'Timestamp','Insights Category', 'Href', 'Value')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Instagram Archive - Account Info'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                tlactivity = f'Instagram Archive - Account Info'
                timeline(report_folder, tlactivity, data_list_timeline, data_headers_timeline)
            else:
                logfunc('No Instagram Archive - Account Info data available')
                
        
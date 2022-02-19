import os
import datetime
import csv

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_youtubeSubscriptions(files_found, report_folder, seeker, wrap_text):

    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('subscriptions.csv'):
            data_list = []

            has_header = True
            with open(file_found, 'r', encoding='utf-8') as f:
                delimited = csv.reader(f, delimiter=',')
                
                next(delimited)
                for item in delimited:
                    if len(item) == 0:
                        continue
                    else:
                        channel_id = item[0]
                        channel_url = item[1]
                        channel_title = item[2]
                       
                        data_list.append((channel_id,channel_url,channel_title))
                    
            if data_list:
                description = 'User channel subscriptions for YouTube.'
                report = ArtifactHtmlReport('YouTube Subscriptions')
                report.start_artifact_report(report_folder, 'YouTube Subscriptions', description)
                html_report = report.get_report_file_path()
                report.add_script()
                data_headers = ('Channel ID','Channel URL','Channel Title')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'YouTube Subscriptions'
                tsv(report_folder, data_headers, data_list, tsvname)

                tlactivity = f'YouTube Subscriptions'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No YouTube Subscriptions data available')
                
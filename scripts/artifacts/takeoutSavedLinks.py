import os
import datetime
import csv

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_takeoutSavedLinks(files_found, report_folder, seeker, wrap_text):

    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('Default list.csv'):
            data_list = []

            has_header = True
            with open(file_found, 'r', encoding='utf-8') as f:
                delimited = csv.reader(f, delimiter=',')
                
                next(delimited)
                for item in delimited:
                    if len(item) == 0:
                        continue
                    else:
                        title = item[0]
                        note = item[1]
                        url = item[2]
                        comment = item[3]
                       
                        data_list.append((title,note,url,comment))
                    
            if data_list:
                description = 'Collections of saved links (images, places, web pages, etc.) from Google Search and Maps.'
                report = ArtifactHtmlReport('Saved Links - Default List')
                report.start_artifact_report(report_folder, 'Saved Links - Default List', description)
                html_report = report.get_report_file_path()
                report.add_script()
                data_headers = ('Title','Note','URL','Comment')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Saved Links - Default List'
                tsv(report_folder, data_headers, data_list, tsvname)

                tlactivity = f'Saved Links - Default List'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Saved Links - Default List data available')
                
        if filename.startswith('Favorite images.csv'):
            data_list = []

            has_header = True
            with open(file_found, 'r', encoding='utf-8') as f:
                delimited = csv.reader(f, delimiter=',')
                
                next(delimited)
                for item in delimited:
                    if len(item) == 0:
                        continue
                    else:
                        title = item[0]
                        note = item[1]
                        url = item[2]
                        comment = item[3]
                       
                        data_list.append((title,note,url,comment))
                    
            if data_list:
                description = 'Collections of saved links (images, places, web pages, etc.) from Google Search and Maps.'
                report = ArtifactHtmlReport('Saved Links - Favorite Images')
                report.start_artifact_report(report_folder, 'Saved Links - Favorite Images', description)
                html_report = report.get_report_file_path()
                report.add_script()
                data_headers = ('Title','Note','URL','Comment')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Saved Links - Favorite Images'
                tsv(report_folder, data_headers, data_list, tsvname)

                tlactivity = f'Saved Links - Favorite Images'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Saved Links - Favorite Images data available')
                
        if filename.startswith('Favorite pages.csv'):
            data_list = []

            has_header = True
            with open(file_found, 'r', encoding='utf-8') as f:
                delimited = csv.reader(f, delimiter=',')
                
                next(delimited)
                for item in delimited:
                    if len(item) == 0:
                        continue
                    else:
                        title = item[0]
                        note = item[1]
                        url = item[2]
                        comment = item[3]
                       
                        data_list.append((title,note,url,comment))
                    
            if data_list:
                description = 'Collections of saved links (images, places, web pages, etc.) from Google Search and Maps.'
                report = ArtifactHtmlReport('Saved Links - Favorite Pages')
                report.start_artifact_report(report_folder, 'Saved Links - Favorite Pages', description)
                report.add_script()
                data_headers = ('Title','Note','URL','Comment')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Saved Links - Favorite Pages'
                tsv(report_folder, data_headers, data_list, tsvname)

                tlactivity = f'Saved Links - Favorite Pages'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Saved Links - Favorite Pages data available')
                
        if filename.startswith('Want to go.csv'):
            data_list = []

            has_header = True
            with open(file_found, 'r', encoding='utf-8') as f:
                delimited = csv.reader(f, delimiter=',')
                
                next(delimited)
                for item in delimited:
                    if len(item) == 0:
                        continue
                    else:
                        title = item[0]
                        note = item[1]
                        url = item[2]
                        comment = item[3]
                       
                        data_list.append((title,note,url,comment))
                    
            if data_list:
                description = 'Collections of saved links (images, places, web pages, etc.) from Google Search and Maps.'
                report = ArtifactHtmlReport('Saved Links - Want To Go')
                report.start_artifact_report(report_folder, 'Saved Links - Want To Go', description)
                html_report = report.get_report_file_path()
                report.add_script()
                data_headers = ('Title','Note','URL','Comment')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Saved Links - Want To Go'
                tsv(report_folder, data_headers, data_list, tsvname)

                tlactivity = f'Saved Links - Want To Go'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Saved Links - Want To Go data available')

__artifacts__ = {
        "takeoutSavedLinks": (
            "Google Takeout Archive",
            ('*/Saved/*.csv'),
            get_takeoutSavedLinks)
}
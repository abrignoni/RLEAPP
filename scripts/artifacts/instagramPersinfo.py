import os
import datetime
import json
import shutil
from pathlib import Path
from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_instagramPersinfo(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('personal_information.json'):
            data_list = []
            data_list_timeline = []
            with open(file_found, "rb") as fp:
                deserialized = json.load(fp)
                
            for x in deserialized['profile_user']:
                for key, values in x.items():
                    if key == 'media_map_data':
                        for a, b in values.items():
                            if a == 'Profile Photo':
                                photo = (b.get('uri', ''))
                                
                                value = (b.get('title', ''))
                                timestamp = (b.get('creation_timestamp', ''))
                                if timestamp > 0:
                                    timestamp = (datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
                                #create folders media/other/ if they dont exist. If they do move the photo there and add <img> for reporting.
                                for match in files_found:
                                    if photo in match:
                                        locationfiles = f'{report_folder}/media/other'
                                        filename = os.path.basename(match)
                                        Path(f'{locationfiles}').mkdir(parents=True, exist_ok=True)
                                        shutil.copy2(match, locationfiles)
                                        thumb = f'<img src="{locationfiles}/{filename}" width="300"></img>'
                                        break
                                data_list.append((a, timestamp, value, thumb))
                                data_list_timeline.append((timestamp, a, value, thumb))
                    if key == 'string_map_data':
                        for a, b in values.items():
                            if a == 'Email':
                                href = (b.get('href', ''))
                                value = (b.get('value', ''))
                                timestamp = (b.get('timestamp', ''))
                                if timestamp > 0:
                                    timestamp = (datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
                                data_list.append((a, timestamp, value, href ))
                                data_list_timeline.append((timestamp, a, value, href))
                            if a == 'Phone Number':
                                href = (b.get('href', ''))
                                value = (b.get('value', ''))
                                timestamp = (b.get('timestamp', ''))
                                if timestamp > 0:
                                    timestamp = (datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
                                data_list.append((a, timestamp, value, href ))
                                data_list_timeline.append((timestamp, a, value, href))
                            if a == 'Gender':
                                href = (b.get('href', ''))
                                value = (b.get('value', ''))
                                timestamp = (b.get('timestamp', ''))
                                if timestamp > 0:
                                    timestamp = (datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
                                data_list.append((a, timestamp, value, href ))
                                data_list_timeline.append((timestamp, a, value, href))
                            if a == 'Private Account':
                                href = (b.get('href', ''))
                                value = (b.get('value', ''))
                                timestamp = (b.get('timestamp', ''))
                                if timestamp > 0:
                                    timestamp = (datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
                                data_list.append((a, timestamp, value, href ))
                                data_list_timeline.append((timestamp, a, value, href))
                                
            if data_list:
                report = ArtifactHtmlReport('Instagram Archive - Personal Info')
                report.start_artifact_report(report_folder, 'Instagram Archive - Personal Info')
                report.add_script()
                data_headers = ('Key', 'Timestamp', 'Value', 'Href/Uri')
                data_headers_timeline = ( 'Timestamp','Key', 'Value', 'Href/Uri')
                report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Href/Uri'])
                report.end_artifact_report()
                
                tsvname = f'Instagram Archive - Personal Info'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                tlactivity = f'Instagram Archive - Personal Info'
                timeline(report_folder, tlactivity, data_list_timeline, data_headers_timeline)
            else:
                logfunc('No Instagram Archive - Personal Info data available')
                
__artifacts__ = {
        "instagramPersinfo": (
            "Instagram Archive",
            ('*/account_information/personal_information.json', '*/media/other/*.jpg'),
            get_instagramPersinfo)
}
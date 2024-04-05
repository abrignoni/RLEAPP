import os
import datetime
import csv
import calendar
from pathlib import Path
import requests
import urllib.parse

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html, kmlgen

def get_discordReturnsdmsOnline(files_found, report_folder, seeker, wrap_text, time_offset):

    counter = 0
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
                        timestamp = item[3]
                        username = item[4]
                        contents = item[5]
                        media = item[6]
                        id = item[0]
                        channelid = item[1]
                        authorid = item[2]
                        thumb = ''
                        if media.startswith('https'):
                            url = urllib.parse.unquote(media)
                            dlpath = Path(report_folder, f'media{counter}')
                            response = requests.get(url, stream=True)
                            if not response.ok:
                                logfunc(f'{response} on {csvname}')
                            else:
                                with open(dlpath, 'wb') as handle:
                                    for block in response.iter_content(1024):
                                        if not block:
                                            break
                                        
                                        handle.write(block)
                                datalist_temp =[]
                                datalist_temp.append(str(dlpath))
                                thumb = media_to_html(f'media{counter}', datalist_temp, report_folder)
                                counter = counter + 1
                        
                        if ('cdn.discordapp.com' or 'media.discordapp.net') in contents and (contents.startswith('http')):
                            url = urllib.parse.unquote(contents)
                            dlpath = Path(report_folder, f'media{counter}')
                            response = requests.get(url, stream=True)
                            if not response.ok:
                                logfunc(f'{response} on {csvname}')
                            else:
                                with open(dlpath, 'wb') as handle:
                                    for block in response.iter_content(1024):
                                        if not block:
                                            break
                                        
                                        handle.write(block)
                                datalist_temp =[]
                                datalist_temp.append(str(dlpath))
                                contents = media_to_html(f'media{counter}', datalist_temp, report_folder)
                                counter = counter + 1
                                
                        data_list_dm.append((timestamp,username,contents,thumb,id,channelid,authorid))
                            
        
        if len(data_list_dm) > 0:
            report = ArtifactHtmlReport(f'Discord - Direct Messages ')
            report.start_artifact_report(report_folder, f'Discord - Direct Messages - {csvname}')
            report.add_script()
            data_headers = ('Timestamp','Username','Contents','Attachment','ID','Channel ID','Author ID')
            report.write_artifact_data_table(data_headers, data_list_dm, file_found, html_no_escape=['Attachment','Contents'])
            report.end_artifact_report()
            
            tsvname = f'Discord - Direct Messages - {csvname}'
            tsv(report_folder, data_headers, data_list_dm, tsvname)
            
            tlactivity = f'Discord -Direct Messages - {csvname}'
            timeline(report_folder, tlactivity, data_list_dm, data_headers)
        else:
            logfunc(f'No Discord - Direct Messages in {csvname}')
                
__artifacts__ = {
        "discordReturnsdmsOnline": (
            "Discord Returns Online",
            ('*/messages/dms/*.csv'),
            get_discordReturnsdmsOnline)
}
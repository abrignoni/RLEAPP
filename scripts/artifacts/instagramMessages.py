import os
import datetime
import json
import magic
import shutil
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows, utf8_in_extended_ascii, media_to_html

def get_instagramMessages(files_found, report_folder, seeker, wrap_text):
    data_list = []
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('message_1.json'):
            
            with open(file_found, "r") as fp:
                deserialized = json.load(fp)
        
            participants = deserialized.get('participants')
            names = ''
            for name in participants:
                names = names + f'{name["name"]}, '
            names = names.strip()[:-1]
            names = utf8_in_extended_ascii(names)[1]
            
            for x in deserialized['messages']:
                sender_name = x.get('sender_name', '')
                sender_name = utf8_in_extended_ascii(sender_name)[1]
                timestamp = x.get('timestamp_ms', '')
                if timestamp > 0:
                    timestamp = (datetime.datetime.fromtimestamp(int(timestamp)/1000).strftime('%Y-%m-%d %H:%M:%S'))
                content = x.get('content', '' )
                content = utf8_in_extended_ascii(content)[1]
                type = x.get('type', '')
                is_unsent = x.get('is_unsent', '')
                agregator = ''
                photos = x.get('photos', '')
                if photos:
                    counter = 0
                    agregator = agregator + ('<table>')
                    for pics in photos:
                        if counter == 0:
                            agregator = agregator +('<tr>')
                        pictures = pics.get('uri', '')
                        time = pics.get('creation_timestamp', '')
                        if time > 0:
                            time= (datetime.datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S'))
                        
                        thumb = media_to_html(pictures, files_found, report_folder)
                        
                        counter = counter + 1
                        agregator = agregator + f'<td>{thumb}<br>{time}</td>'
                        #hacer uno que no tenga html
                        if counter == 2:
                            counter = 0
                            agregator = agregator + ('</tr>')
                    if counter == 1:
                        agregator = agregator + ('</tr>')
                    agregator = agregator + ('</table><br>')
                
                videos = x.get('videos', '')
                if videos:
                    counter = 0
                    agregator = agregator + ('<table>')
                    for vids in videos:
                        if counter == 0:
                            agregator = agregator + ('<tr>')
                        movie = vids.get('uri', '')
                        time = vids.get('creation_timestamp', '')
                        if time > 0:
                            time= (datetime.datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S'))
                        
                        thumb = media_to_html(movie, files_found, report_folder)
                        
                        counter = counter + 1
                        agregator = agregator + f'<td>{thumb}<br>{time}</td>'
                        #hacer uno que no tenga html
                        if counter == 2:
                            counter = 0
                            agregator = agregator + ('</tr>')
                    if counter == 1:
                        agregator = agregator + ('</tr>')
                    agregator = agregator + ('</table><br>')
                        
                data_list.append((timestamp, names, sender_name, content, agregator, is_unsent, type ))
    
                
    if data_list:
        file_found = os.path.dirname(file_found)
        file_found = os.path.dirname(file_found)
        report = ArtifactHtmlReport('Instagram Archive - Messages')
        report.start_artifact_report(report_folder, 'Instagram Archive - Messages')
        report.add_script()
        data_headers = ('Timestamp', 'Participants', 'Sender', 'Content', 'Media', 'Is unsent', 'Type')
        report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Media'])
        report.end_artifact_report()
        
        tsvname = f'Instagram Archive - Messages'
        tsv(report_folder, data_headers, data_list, tsvname)
        
        tlactivity = f'Instagram Archive - Messages'
        timeline(report_folder, tlactivity, data_list, data_headers)

    else:
        logfunc('No Instagram Archive - Messages data available')
                
        
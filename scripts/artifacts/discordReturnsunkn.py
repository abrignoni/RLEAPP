import os
import datetime
import csv
import calendar

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html, kmlgen

def get_discordReturnsunkn(files_found, report_folder, seeker, wrap_text, time_offset):

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
                        
                        if media == '':
                            agregator = ' '
                        else:
                            if '\n' in media:
                                media = media.split('\n')
                                agregator = '<table>'
                                counter = 0
                                for x in media:
                                    if counter == 0:
                                        agregator = agregator + ('<tr>')
                                    media = x.split('/')
                                    originalfilename = media[-1]
                                    attachmentidentifier = f"{media[-2]}"
                                    thumb = media_to_html(attachmentidentifier, files_found, report_folder)
                                    counter = counter + 1
                                    agregator = agregator + f'<td>{thumb}</td>'
                                    #hacer uno que no tenga html
                                    if counter == 2:
                                        counter = 0
                                        agregator = agregator + ('</tr>')
                                if counter == 1:
                                    agregator = agregator + ('</tr>')
                                agregator = agregator + ('</table><br>')
                            else:
                                media = media.split('/')
                                originalfilename = media[-1]
                                attachmentidentifier = f"{media[-2]}"
                                agregator = media_to_html(attachmentidentifier, files_found, report_folder)
                        
                        data_list_dm.append((timestamp,username,contents,agregator,id,channelid,authorid))
                        
        
            if data_list_dm:
                report = ArtifactHtmlReport(f'Discord - Unknown Messages ')
                report.start_artifact_report(report_folder, f'Discord - Unknown Messages - {csvname}')
                report.add_script()
                data_headers = ('Timestamp','Username','Contents','Media','ID','Channel ID','Author ID')
                report.write_artifact_data_table(data_headers, data_list_dm, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Discord - Unknown Messages - {csvname}'
                tsv(report_folder, data_headers, data_list_dm, tsvname)
                
                tlactivity = f'Discord - Unknown Messages - {csvname}'
                timeline(report_folder, tlactivity, data_list_dm, data_headers)
            else:
                logfunc(f'Discord - Unknown Messages - {csvname}')
                
__artifacts__ = {
        "discordReturnsunkn": (
            "Discord Returns",
            ('*/attachments/*.*', '*/messages/unknown/*.csv'),
            get_discordReturnsunkn)
}
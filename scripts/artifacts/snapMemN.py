import os
import datetime
import csv
import traceback

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html, kmlgen

def monthletter(month):
    monthdict = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    return monthdict[month]

def read_multiline_csv(file_path):
    rows = []
    start_adding = False
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for row in reader:
            if start_adding:
                rows.append(row)
            elif '===========================' in row:
                start_adding = True
    return rows


def get_snapMemN(files_found, report_folder, seeker, wrap_text, time_offset):

    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        one = (os.path.split(file_found))
        username = (os.path.basename(one[0]))
        
        
        if filename.startswith('memories.csv'):
            csv_rows = read_multiline_csv(file_found)

            data_list_f = []
            try:
                header = csv_rows[0]
            
                timestamp = header[7]
                header.insert(0,timestamp)
                del header[8]
    
                data_list = csv_rows[1:]
                for entry in data_list:
                    
                    #Change timestamp format
                    timestamp = entry[7]
                    timestamp = timestamp.split(' ')
                    year = timestamp[5]
                    day = timestamp[2]
                    time = timestamp[3]
                    month = monthletter(timestamp[1])
                    timestampfinal = (f'{year}-{month}-{day} {time}')
                    
                    #Move timestamp to the front of the list and delete the original positon
                    entry.insert(0, timestampfinal)
                    del entry[8]
                    
                    
                    #Look for media and substitute it in the list
                    
                    media = entry[2]
                    if media == '':
                        agregator = ''
                    else:
                        if ';' in media:
                            media = media.split(';')
                            agregator = '<table>'
                            counter = 0
                            for x in media:
                                if counter == 0:
                                    agregator = agregator + ('<tr>')
                                thumb = media_to_html(x, files_found, report_folder)        
                                
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
                            agregator = media_to_html(media, files_found, report_folder)
                    entry[2] = agregator
                    #Add to the final list for reporting
                    
                    data_list_f.append(entry)
            except:
                pass
                    
                    
            if data_list_f:
                report = ArtifactHtmlReport(f'Snapchat - Memories')
                report.start_artifact_report(report_folder, f'Snapchat -  Memories - {username}')
                report.add_script()
                data_headers = ('Timestamp', 'Id', 'Media_id', 'Encrypted', 'Source_type', 'Latitude', 'Longitude', 'Duration')
                report.write_artifact_data_table(data_headers, data_list_f, file_found, html_no_escape=['Media_id'])#
                report.end_artifact_report()
                
                tsvname = f'Snapchat -  Memories - {username}'
                tsv(report_folder, data_headers, data_list_f, tsvname)
                
                tlactivity = f'Snapchat -  Memories - {username}'
                timeline(report_folder, tlactivity, data_list_f, data_headers)
                
                kmlactivity = f'Snapchat - Memories - {username}'
                kmlgen(report_folder, kmlactivity, data_list_f, data_headers) 
                
                
            else:
                logfunc(f'No Snapchat - Memories - {username}')
        
        
__artifacts__ = {
        "snapMemN": (
            "Snapchat Returns",
            ('*/memories.csv','*/*.*'),
            get_snapMemN)
}
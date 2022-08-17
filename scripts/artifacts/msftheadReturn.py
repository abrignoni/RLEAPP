import os
import datetime
import email
import csv
import sqlite3
from email.parser import HeaderParser


from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html

def recdetail(val):
    cleandata = val.split('by')[0].split('from')[1].replace('\n', '').strip()
    return cleandata

def get_msftheadReturn(files_found, report_folder, seeker, wrap_text):

    data_list = []
    data_list_tsv = []
    
    #Start full data SQLite
    dbtowrite = os.path.join(report_folder, 'EMLHeader.db')
    db = sqlite3.connect(dbtowrite)
    cursor = db.cursor()
    cursor.execute(
        """
        CREATE TABLE data(time_stamp TEXT, xorigip TEXT, fromm text, too text, received TEXT, paths TEXT)
        """
    )
    db.commit()
    
    
    #Start full data CSV
    csvtowrite = os.path.join(report_folder, 'EML_Header_Data.csv')
    csvtowritesmall = os.path.join(report_folder, 'EML_Header_Data_Small.csv')
    with open(csvtowrite, 'w', encoding='UTF8') as f, open(csvtowritesmall, 'w', encoding='UTF8') as g:
        writer = csv.writer(f)
        writerg = csv.writer(g)
        headers = ['Timestamp', 'X Originating IP', 'From', 'To', 'Received', 'Path']
        headersg = ['Timestamp', 'X Originating IP', 'From', 'To', 'Received Last', 'Received Middle', 'Received First', 'Path']
        writer.writerow(headers)
        writerg.writerow(headersg)
        
        
        for file_found in files_found:
            file_found = str(file_found)
            
            filename = os.path.basename(file_found)
            
            with open(file_found, 'r') as f:
                msg = email.message_from_file(f)
            
            parser = email.parser.HeaderParser()
            headers = parser.parsestr(msg.as_string())
            
            fecha = orip = to = de = aggregator = fortsv = ''
            receivedlast = receivedmiddle = receivedfirst = ''
            count = 0
            
            for key, value in headers.items():
                if key == 'Date':
                    fecha = value
                if key == 'x-originating-ip':
                    orip = value
                if key == 'To':
                    to = value
                if key == 'From':
                    de = value
                if key == 'Received':
                    aggregator = aggregator + value
                    if count == 0:
                        receivedlast = recdetail(value)
                    elif count == 1:
                        receivedmiddle = recdetail(value)
                    elif count == 2:
                        receivedfirst = recdetail(value)
                    count = count + 1
            
            data_list.append((fecha, orip, de, to, file_found))
            data = [fecha, orip, de, to, aggregator, file_found]
            datag = [fecha, orip, de, to, receivedlast, receivedmiddle, receivedfirst, file_found]
            writer.writerow(data)
            writerg.writerow(datag)
            cursor.execute("INSERT INTO data VALUES(?,?,?,?,?,?)", (fecha, orip, de, to, aggregator, file_found))
    db.commit()
    db.close()
            
    if data_list:
        report = ArtifactHtmlReport('Microsoft Returns - Headers')
        report.start_artifact_report(report_folder, 'Microsoft Returns - Headers')
        report.add_script()
        data_headers = ('Timestamp', 'X Originating IP', 'From', 'To', 'Filename')
        report.write_artifact_data_table(data_headers, data_list, file_found)
        report.end_artifact_report()
        
        tlactivity = f'Microsoft Returns - Headers'
        timeline(report_folder, tlactivity, data_list, data_headers)
    else:
        logfunc('No Microsoft Returns - Headers data available')
    
__artifacts__ = {
        "msftheadReturn": (
            "Microsoft Returns",
            ('*.eml_hdr.eml'),
            get_msftheadReturn)
}    
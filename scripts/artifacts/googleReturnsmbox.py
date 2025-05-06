import os
import datetime
import csv
import mailbox
import email

from scripts.filetype import guess_extension
from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html

def getbody(message): #getting plain text 'email body'
    body = None
    if message.is_multipart():
        for part in message.walk():
            if part.is_multipart():
                for subpart in part.walk():
                    if subpart.get_content_type() == 'text/plain':
                        body = subpart.get_payload(decode=True).decode('Latin_1')
            elif part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True).decode('Latin_1')
    elif message.get_content_type() == 'text/plain':
        body = message.get_payload(decode=True).decode('Latin_1')
    return body
    
def get_googleReturnsmbox(files_found, report_folder, seeker, wrap_text):
    
    platform = is_platform_windows()
    if platform:
        splitter = '\\'
    else:
        splitter = '/'
    
    for a, file_found in enumerate(files_found):
        file_found = str(file_found)
        
        mailboxid = str(a + 1)
        data_list = []
        
        mbox = mailbox.mbox(file_found)
        
        for i, message in enumerate(mbox):
            emailid = str(i)
            mfrom = message['from']
            mto = message['to']
            msubject = str(message['Subject'])
            msentdate = message['date']
            msgtype = message.get_content_type()
            thebody = getbody(message)
            if thebody is None:
                thebody = 'Check source data.'
            
            attachmentnumber = 0
            attachments = ''
            filename = None
            if message.is_multipart():
                for part in message.walk():
                    if part.get_content_maintype() == 'multipart': continue
                    if part.get('Content-Disposition') is None: continue
                    if part.get_content_disposition() == 'attachment':
                        filename = part.get_filename()
                    if filename is None:
                        attachmentnumber = attachmentnumber + 1
                        filename = str(attachmentnumber)
                            
                    foldernumber = str(i)
                    
                        #join(report_folder, basename(file_found))
                    pathfile = f'{report_folder}{mailboxid}_attachments_data{splitter}{foldernumber}{splitter}{filename}'
                    os.makedirs(os.path.dirname(pathfile), exist_ok=True)
                    
                    with open(pathfile, "wb") as f:
                        f.write(part.get_payload(decode=True))
                        
                    extension = guess_extension(pathfile)
                        
                    renamed = f'{pathfile}.{extension}' if extension else pathfile
                    try:
                        os.rename(pathfile, renamed)
                    except:
                        pass
                    
                    tolink = []
                    tolink.append(renamed)
                    thumb = media_to_html(renamed, tolink, f'{report_folder}{mailboxid}_attachments_report{splitter}')
                    attachments = attachments + '<table><tr><td>' + thumb + '</td></tr></table><p>'
            
        
            data_list.append((msentdate, mfrom, mto, msubject, thebody, attachments))
            
        if data_list:
            description = f'Google Returns - Mbox'
            report = ArtifactHtmlReport(f'Google Returns - Mbox - {a}')
            report.start_artifact_report(report_folder, f'Google Returns - Mbox - {a}', description)
            report.add_script()
            data_headers = ('Date','From','To','Subject','Body','Attachments')
            report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Attachments'])
            report.end_artifact_report()
            
            tsvname = f'Google Returns - Mbox - {a}'
            tsv(report_folder, data_headers, data_list, tsvname)
            
            tlactivity = f'Google Returns - Mbox'
            timeline(report_folder, tlactivity, data_list, data_headers)

        else:
            logfunc(f'No Google Returns - Mbox - {a} data available')
                
__artifacts__ = {
        "googleReturnsmbox": (
            "Google Returns MBOXes",
            ('*/*.Mail.MessageContent_*/Mail/All mail Including Spam and Trash.mbox','*/Mail/All mail Including Spam and Trash.mbox'),
            get_googleReturnsmbox)
}
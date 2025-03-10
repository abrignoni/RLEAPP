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
    
def get_takeoutGoogleMail(files_found, report_folder, seeker, wrap_text, time_offset):
    
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
            if msentdate:
                msentdate = msentdate.replace('Sun, ','').replace('Mon, ','').replace('Tue, ','').replace('Wed, ','').replace('Thu, ','').replace('Fri, ','').replace('Sat, ','')
                msentdate_split = msentdate.split(' ')
            
            day = msentdate_split[0]
            if len(day) < 2:
                day = "0" + day
            
            month = msentdate_split[1]
            year = msentdate_split[2]
            time = msentdate_split[3]
            
            offset = msentdate_split[4]
            if offset == 'GMT':
                offset = '+0000'

            if month == 'Jan':
                month = '01'
            elif month == 'Feb':
                month = '02'
            elif month == 'Mar':
                month = '03'
            elif month == 'Apr':
                month = '04'
            elif month == 'May':
                month = '05'
            elif month == 'Jun':
                month = '06'
            elif month == 'Jul':
                month = '07'
            elif month == 'Aug':
                month = '08'
            elif month == 'Sep':
                month = '09'
            elif month == 'Oct':
                month = '10'
            elif month == 'Nov':
                month = '11'
            elif month == 'Dec':
                month = '12'
                
            msentdate_formatted = year + "-" + month + "-" + day + " " + time + " " + offset
            
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
        
            data_list.append((msentdate_formatted, mfrom, mto, msubject, thebody, attachments))
        
        if data_list:
            description = f'Google Takeout - MBOX'
            report = ArtifactHtmlReport(f'Google Takeout - MBOX - {a}')
            report.start_artifact_report(report_folder, f'Google Takeout - MBOX - {a}', description)
            report.add_script()
            data_headers = ('Date','From','To','Subject','Body','Attachments')
            report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Attachments'])
            report.end_artifact_report()
            
            tsvname = f'Google Takeout - MBOX - {a}'
            tsv(report_folder, data_headers, data_list, tsvname)
    
        else:
            logfunc(f'No Google Takeout - MBOX - {a} data available')
                
__artifacts__ = {
        "takeoutGoogleMail": (
            "Google Takeout Archive",
            ('*/Mail/All mail Including Spam and Trash.mbox','*/Deleted.mbox'),
            get_takeoutGoogleMail)
}
import os
import json

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html

def get_snapchatAccounthist(files_found, report_folder, seeker, wrap_text, time_offset):

    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        one = (os.path.split(file_found))
        username = (os.path.basename(one[0]))
        
        if filename.startswith('account_history.json'):
            data_list =[]
            with open(file_found, 'r') as fp:
                deserialized = json.load(fp)
            
            for key, value in deserialized.items():
                
                if key == 'Display Name Change':
                    data_list_dn = []
                    for items in value:
                        data_list_dn.append((items['Date'],items['Display Name']))
                        
                if key == 'Email Change':
                    data_list_ec = []
                    if len(value) > 0:
                        data_list_ec.append((value,))
                    
                if key == 'Mobile Number Change':
                    data_list_mn = []
                    for items in value:
                        data_list_mn.append((items['Date'],items['Mobile Number']))
                        
                if key == 'Password Change':
                    data_list_pc = []
                    for items in value:
                        data_list_pc.append((items['Date'],))
                        
                if key == 'Snapchat Linked to Bitmoji':
                    data_list_lb = []
                    for items in value:
                        data_list_lb.append((items['Date'],))
                        
                if key == 'Spectacles':
                    data_list_spec = []
                    if len(value) > 0:
                        data_list_spec.append((value,))
                    
                if key == 'Two-Factor Authentication':
                    data_list_2f = []
                    if len(value) > 0:
                        data_list_2f.append((value,))
                    
                if key == 'Account deactivated / reactivated':
                    data_list_adr = []
                    if len(value) > 0:
                        data_list_adr.append((value,))
                    
                if key == 'Download My Data Reports':
                    data_list_dd = []
                    for items in value:
                        data_list_dd.append((items['Date'],items['Status'],items['Email Address']))
            
            if data_list_dd:
                report = ArtifactHtmlReport(f'Snapchat - Download My Data Reports')
                report.start_artifact_report(report_folder, f'Snapchat - Download My Data Reports')
                report.add_script()
                data_headers = ('Timestamp','Status','Email Address')
                report.write_artifact_data_table(data_headers, data_list_dd, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Download My Data Reports'
                tsv(report_folder, data_headers, data_list_dd, tsvname)
                
                tlactivity = f'Snapchat - Download My Data Reports'
                timeline(report_folder, tlactivity, data_list_dd, data_headers)
                
            else:
                logfunc(f'No Snapchat - Display Name Change')
            
            if data_list_adr:
                report = ArtifactHtmlReport(f'Snapchat - Account Deactivated - Reactivated')
                report.start_artifact_report(report_folder, f'Snapchat - Account Deactivated - Reactivated')
                report.add_script()
                data_headers = ('Data',)
                report.write_artifact_data_table(data_headers, data_list_adr, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Account Deactivated - Reactivated'
                tsv(report_folder, data_headers, data_list_adr, tsvname)
                
            else:
                logfunc(f'No Snapchat - Account Deactivated - Reactivated')
            
            if data_list_2f:
                report = ArtifactHtmlReport(f'Snapchat - Two-Factor Authentication')
                report.start_artifact_report(report_folder, f'Snapchat - Two-Factor Authentication')
                report.add_script()
                data_headers = ('Data',)
                report.write_artifact_data_table(data_headers, data_list_2f, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Two-Factor Authentication'
                tsv(report_folder, data_headers, data_list_2f, tsvname)
                
            else:
                logfunc(f'No Snapchat - Two-Factor Authentication')
            
            if data_list_spec:
                report = ArtifactHtmlReport(f'Snapchat - Spectacles')
                report.start_artifact_report(report_folder, f'Snapchat - Spectacles')
                report.add_script()
                data_headers = ('Data',)
                report.write_artifact_data_table(data_headers, data_list_spec, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Linked to Spectacles'
                tsv(report_folder, data_headers, data_list_spec, tsvname)
                
            else:
                logfunc(f'No Snapchat - Linked to Spectacles')
            
            if data_list_lb:
                report = ArtifactHtmlReport(f'Snapchat - Linked to Bitmoji')
                report.start_artifact_report(report_folder, f'Snapchat - Linked to Bitmoji')
                report.add_script()
                data_headers = ('Timestamp',)
                report.write_artifact_data_table(data_headers, data_list_lb, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Linked to Bitmoji'
                tsv(report_folder, data_headers, data_list_lb, tsvname)
                
                tlactivity = f'Snapchat - Linked to Bitmoji'
                timeline(report_folder, tlactivity, data_list_lb, data_headers)
                
            else:
                logfunc(f'No Snapchat - Linked to Bitmoji')
            
            if data_list_pc:
                report = ArtifactHtmlReport(f'Snapchat - Password Change')
                report.start_artifact_report(report_folder, f'Snapchat - Password Change')
                report.add_script()
                data_headers = ('Timestamp',)
                report.write_artifact_data_table(data_headers, data_list_pc, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Password Change'
                tsv(report_folder, data_headers, data_list_pc, tsvname)
                
                tlactivity = f'Snapchat - Password Change'
                timeline(report_folder, tlactivity, data_list_pc, data_headers)
                
            else:
                logfunc(f'No Snapchat - Password Change')
            
            if data_list_mn:
                report = ArtifactHtmlReport(f'Snapchat - Mobile Number Change')
                report.start_artifact_report(report_folder, f'Snapchat - Mobile Number Change')
                report.add_script()
                data_headers = ('Timestamp','Mobile Number')
                report.write_artifact_data_table(data_headers, data_list_mn, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Mobile Number Change'
                tsv(report_folder, data_headers, data_list_mn, tsvname)
                
                tlactivity = f'Snapchat - Mobile Number Change'
                timeline(report_folder, tlactivity, data_list_mn, data_headers)
                
            else:
                logfunc(f'No Snapchat - Mobile Number Change')
                
            
            if data_list_ec:
                report = ArtifactHtmlReport(f'Snapchat - Email Change')
                report.start_artifact_report(report_folder, f'Snapchat - Email Change')
                report.add_script()
                data_headers = ('Data',)
                report.write_artifact_data_table(data_headers, data_list_ec, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Email Change'
                tsv(report_folder, data_headers, data_list_ec, tsvname)
                
            else:
                logfunc(f'No Snapchat - Email Change')
            
            if data_list_dn:
                report = ArtifactHtmlReport(f'Snapchat - Display Name Change')
                report.start_artifact_report(report_folder, f'Snapchat - Display Name Change')
                report.add_script()
                data_headers = ('Timestamp','Display Name')
                report.write_artifact_data_table(data_headers, data_list_dn, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Display Name Change'
                tsv(report_folder, data_headers, data_list_dn, tsvname)
                
                tlactivity = f'Snapchat - Display Name Change'
                timeline(report_folder, tlactivity, data_list_dn, data_headers)
                
            else:
                logfunc(f'No Snapchat - Display Name Change')
            
        
            
    
__artifacts__ = {
        "snapchatAccounthist": (
            "Snapchat Archive",
            ('*/account_history.json'),
            get_snapchatAccounthist)
}
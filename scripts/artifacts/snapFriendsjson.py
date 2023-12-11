import os
import json

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html

def get_snapFriendsjson(files_found, report_folder, seeker, wrap_text, time_offset):

    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        one = (os.path.split(file_found))
        username = (os.path.basename(one[0]))
        
        if filename.startswith('friends.json'):
            data_list =[]
            with open(file_found, 'r') as fp:
                deserialized = json.load(fp)
            
            for key, value in deserialized.items():
                if key == 'Friends':
                    data_list_f = []
                    for items in value:
                        data_list_f.append((items['Creation Timestamp'],items['Last Modified Timestamp'],items['Username'],items['Display Name'],items['Source']))
                        
                if key == 'Friend Requests Sent':
                    data_list_fr = []
                    for items in value:
                        data_list_fr.append((items['Creation Timestamp'],items['Last Modified Timestamp'],items['Username'],items['Display Name'],items['Source']))
                        
                if key == 'Blocked Users':
                    data_list_bu = []
                    for items in value:
                        data_list_bu.append((items['Creation Timestamp'],items['Last Modified Timestamp'],items['Username'],items['Display Name'],items['Source']))
                        
                if key == 'Deleted Friends':
                    data_list_df = []
                    for items in value:
                        data_list_df.append((items['Creation Timestamp'],items['Last Modified Timestamp'],items['Username'],items['Display Name'],items['Source']))
                        
                if key == 'Hidden Friend Suggestions':
                    data_list_hf = []
                    for items in value:
                        data_list_hf.append((items['Creation Timestamp'],items['Last Modified Timestamp'],items['Username'],items['Display Name'],items['Source']))
                        
                if key == 'Ignored Snapchatters':
                    data_list_ig = []
                    for items in value:
                        data_list_ig.append((items['Creation Timestamp'],items['Last Modified Timestamp'],items['Username'],items['Display Name'],items['Source']))
                        
                if key == 'Pending Requests':
                    data_list_pr = []
                    for items in value:
                        data_list_pr.append((items['Creation Timestamp'],items['Last Modified Timestamp'],items['Username'],items['Display Name'],items['Source']))
                        
                if key == 'Shortcuts':
                    data_list_sc = []
                    for items in value:
                        data_list_sc.append((items['Creation Timestamp'],items['Last Modified Timestamp'],items['Username'],items['Display Name'],items['Source']))
                    
            if data_list_f:
                report = ArtifactHtmlReport(f'Snapchat - Friends')
                report.start_artifact_report(report_folder, f'Snapchat - Friends')
                report.add_script()
                data_headers = ('Timestamp','Last Modified Timestamp','Username','Display Name','Source')
                report.write_artifact_data_table(data_headers, data_list_f, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Friends'
                tsv(report_folder, data_headers, data_list_f, tsvname)
                
                tlactivity = f'Snapchat - Friends'
                timeline(report_folder, tlactivity, data_list_f, data_headers)
                
            else:
                logfunc(f'No Snapchat - Friends')
            
            if data_list_fr:
                report = ArtifactHtmlReport(f'Snapchat - Friends Request Sent')
                report.start_artifact_report(report_folder, f'Snapchat - Friends Request Sent')
                report.add_script()
                data_headers = ('Timestamp','Last Modified Timestamp','Username','Display Name','Source')
                report.write_artifact_data_table(data_headers, data_list_fr, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Friends Request Sent'
                tsv(report_folder, data_headers, data_list_fr, tsvname)
                
                tlactivity = f'Snapchat - Friends Request Sent'
                timeline(report_folder, tlactivity, data_list_fr, data_headers)
                
            else:
                logfunc(f'No Snapchat - Friends Request Sent')
            
            if data_list_bu:
                report = ArtifactHtmlReport(f'Snapchat - Blocked Users')
                report.start_artifact_report(report_folder, f'Snapchat - Blocked Users')
                report.add_script()
                data_headers = ('Timestamp','Last Modified Timestamp','Username','Display Name','Source')
                report.write_artifact_data_table(data_headers, data_list_bu, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Blocked Users'
                tsv(report_folder, data_headers, data_list_bu, tsvname)
                
                tlactivity = f'Snapchat - Blocked Users'
                timeline(report_folder, tlactivity, data_list_bu, data_headers)
                
            else:
                logfunc(f'No Snapchat - Blocked Users')
            
            if data_list_df:
                report = ArtifactHtmlReport(f'Snapchat - Deleted Friends')
                report.start_artifact_report(report_folder, f'Snapchat - Deleted Friends')
                report.add_script()
                data_headers = ('Timestamp','Last Modified Timestamp','Username','Display Name','Source')
                report.write_artifact_data_table(data_headers, data_list_df, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Deleted Friends'
                tsv(report_folder, data_headers, data_list_df, tsvname)
                
                tlactivity = f'Snapchat - Deleted Friends'
                timeline(report_folder, tlactivity, data_list_df, data_headers)
                
            else:
                logfunc(f'No Snapchat - Deleted Friends')
                
            if data_list_hf:
                report = ArtifactHtmlReport(f'Snapchat - Hidden Friends Suggestions')
                report.start_artifact_report(report_folder, f'Snapchat - Hidden Friends Suggestions')
                report.add_script()
                data_headers = ('Timestamp','Last Modified Timestamp','Username','Display Name','Source')
                report.write_artifact_data_table(data_headers, data_list_hf, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Hidden Friends Suggestions'
                tsv(report_folder, data_headers, data_list_hf, tsvname)
                
                tlactivity = f'Snapchat - Hidden Friends Suggestions'
                timeline(report_folder, tlactivity, data_list_hf, data_headers)
                
            else:
                logfunc(f'No Snapchat - Hidden Friends Suggestions')
                
            if data_list_ig:
                report = ArtifactHtmlReport(f'Snapchat - Ignored Snapchatters')
                report.start_artifact_report(report_folder, f'Snapchat - Ignored Snapchatters')
                report.add_script()
                data_headers = ('Timestamp','Last Modified Timestamp','Username','Display Name','Source')
                report.write_artifact_data_table(data_headers, data_list_ig, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Ignored Snapchatters'
                tsv(report_folder, data_headers, data_list_ig, tsvname)
                
                tlactivity = f'Snapchat - Ignored Snapchatters'
                timeline(report_folder, tlactivity, data_list_ig, data_headers)
                
            else:
                logfunc(f'No Snapchat - Ignored Snapchatters')
                
            if data_list_pr:
                report = ArtifactHtmlReport(f'Snapchat - Pending Requests')
                report.start_artifact_report(report_folder, f'Snapchat - Pending Requests')
                report.add_script()
                data_headers = ('Timestamp','Last Modified Timestamp','Username','Display Name','Source')
                report.write_artifact_data_table(data_headers, data_list_pr, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Pending Requests'
                tsv(report_folder, data_headers, data_list_pr, tsvname)
                
                tlactivity = f'Snapchat - Pending Requests'
                timeline(report_folder, tlactivity, data_list_pr, data_headers)
                
            else:
                logfunc(f'No Snapchat - Pending Requests')
                
            if data_list_sc:
                report = ArtifactHtmlReport(f'Snapchat - Shortcuts')
                report.start_artifact_report(report_folder, f'Snapchat - Shortcuts')
                report.add_script()
                data_headers = ('Timestamp','Last Modified Timestamp','Username','Display Name','Source')
                report.write_artifact_data_table(data_headers, data_list_sc, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Snapchat - Shortcuts'
                tsv(report_folder, data_headers, data_list_sc, tsvname)
                
                tlactivity = f'Snapchat - Shortcuts'
                timeline(report_folder, tlactivity, data_list_sc, data_headers)
                
            else:
                logfunc(f'No Snapchat - Shorcuts')
    
__artifacts__ = {
        "snapFriendsjson": (
            "Snapchat Archive",
            ('*/friends.json'),
            get_snapFriendsjson)
}
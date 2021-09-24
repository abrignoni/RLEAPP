import os
import datetime
import csv

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, ipgen

def get_takeoutAccessLogActivity(files_found, report_folder, seeker, wrap_text):

    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('Activities - '):
            data_list = []
            ipaddress_list = []
            
            has_header = True
            with open(file_found, 'r', encoding='utf-8') as f:
                delimited = csv.reader(f, delimiter=',')
                next(delimited)
                for item in delimited:
                    gaia_id = item[0]
                    timestamp = item[1]
                    ip_address = item[2]
                    proxied_host_ip = item[3]
                    is_nonroutable = item[4]
                    activity_country = item[5]
                    activity_region = item[6]
                    activity_city = item[7]
                    user_agent_str = item[8]
                    product = item[9]
                    sub_product = item[10]
                    referer_product = item[11]
                    referer_sub_product = item[12]
                    activity_type = item[13]
                    gmail_access_channel = item[14]
                    android_webview_package = item[15]
                    data_list.append((timestamp,gaia_id,ip_address,proxied_host_ip,is_nonroutable,activity_country,activity_region,activity_city,user_agent_str,product,sub_product,referer_product,referer_sub_product,activity_type,gmail_access_channel,android_webview_package))
                    if ip_address != None:
                        ipaddress_list.append((ip_address, 'Google Access Log Activities', 'Takeout_Ipaddress_logins', html_report, None))
            
            if data_list:
                description = 'A list of Google services accessed by your devices (for example every time your phone synchronizes with your Gmail)'
                report = ArtifactHtmlReport('Google Access Log Activities')
                report.start_artifact_report(report_folder, 'Google Access Log Activities', description)
                html_report = report.get_report_file_path()
                report.add_script()
                
                data_headers = ('Timestamp','GAIA ID','IP Address','Proxied Host IP Address','Is Non-routable IP Address','Activity Country','Activity Region','Activity City','User Agent String','Product Name','Sub-Product Name','Referer Product Name','Referer Sub-Product Name','Activity Type','Gmail Access Channel','Android Webview Package Name')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Google Access Log Activities'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                ipgen(report_folder,ipaddress_list)

                tlactivity = f'Google Access Log Activities'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Google Access Log Activities data available')
                
        if filename.startswith('Devices - '):
            data_list = []
            
            has_header = True
            with open(file_found, 'r', encoding='utf-8') as f:
                delimited = csv.reader(f, delimiter=',')
                next(delimited)
                for item in delimited:
                    gaia_id = item[0]
                    device_type = item[1]
                    brand_name = item[2]
                    device_model = item[3]
                    device_os = item[4]
                    device_last_country = item[5]
                    device_last_location_ts = item[6]
                    device_first_activity_ts = item[7]
                    device_last_activity_ts = item[8]

                    data_list.append((device_first_activity_ts,device_last_activity_ts,gaia_id,device_type,brand_name,device_model,device_os,device_last_country,device_last_location_ts))
            
            if data_list:
                description = 'A list of devices (i.e. Nest, Pixel, iPhone, Galaxy, etc) which have accessed your Google account over the last 30 days'
                report = ArtifactHtmlReport('Google Access Log Devices')
                report.start_artifact_report(report_folder, 'Google Access Log Devices', description)
                html_report = report.get_report_file_path()
                report.add_script()
                
                data_headers = ('First Activity Timestamp','Last Activity Timestamp','GAIA ID','Device Type','Device Brand','Device Model','Device OS','Device Last Country','Device Last Location Timestamp')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Google Access Log Devices'
                tsv(report_folder, data_headers, data_list, tsvname)

                tlactivity = f'Google Access Log Devices'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Google Access Log Devices data available')
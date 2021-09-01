import os
import datetime
import csv
import codecs
import shutil
import magic

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, usergen, ipgen

def get_netflixArchive(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('Profiles.csv'):
            data_list =[]
            user_list = []
            report = ArtifactHtmlReport('Netflix - Profiles')
            report.start_artifact_report(report_folder, 'Netflix - Profiles')
            html_report = report.get_report_file_path()
            report.add_script()
            has_header = True
            with open(file_found, 'r', encoding='utf-8') as f:
                delimited = csv.reader(f, delimiter=',')
                for item in delimited:
                    if has_header:
                        has_header = False
                    else:
                        user = item[0]
                        email_address = item[1]
                        profile_creation_time = item[2]
                        data_list.append((user, email_address, profile_creation_time))
                        if email_address != "":
                            user_list.append((email_address, 'Netflix', 'Netflix_Profiles', html_report, None))

            if data_list:
                data_headers = ('Profile_Name', 'Email_Address', 'Profile_Creation_Time')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Netflix - Profiles'
                tsv(report_folder, data_headers, data_list, tsvname)

                usergen(report_folder, user_list)

                tlactivity = f'Netflix - Profiles'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Netflix - Profiles data available')

        if filename.startswith('BillingHistory.csv'):
            data_list = []
            header_list = []
            report = ArtifactHtmlReport('Netflix - Billing History')
            report.start_artifact_report(report_folder, 'Netflix - Billing History')
            report.add_script()
            has_header = True
            with open(file_found, 'r', encoding='utf-8') as f:
                delimited = csv.reader(f, delimiter=',')
                for item in delimited:
                    if has_header:
                        has_header = False
                        header_list = item
                    else:
                        data_list.append(item)

            if data_list:
                data_headers = header_list
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()

                tsvname = f'Netflix - Billing History'
                tsv(report_folder, data_headers, data_list, tsvname)

                tlactivity = f'Netflix - Billing History'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Netflix - Billing History data available')

        if filename.startswith('IpAddressesLogin.csv'):
            data_list = []
            ipaddress_list = []
            report = ArtifactHtmlReport('Netflix - IP Address Login')
            report.start_artifact_report(report_folder, 'Netflix - IP Address Login')
            html_report = report.get_report_file_path()
            report.add_script()
            has_header = True
            with open(file_found, 'r', encoding='utf-8') as f:
                delimited = csv.reader(f, delimiter=',')
                for item in delimited:
                    if has_header:
                        has_header = False
                    else:
                        esn = item[0]
                        country = item[1]
                        region_code = item[2]
                        device_desc = item[3]
                        ipaddress = item[4]
                        timestamp = item[5]
                        data_list.append((timestamp, ipaddress, esn, country, region_code, device_desc))
                        if ipaddress != None:
                            ipaddress_list.append(
                                (ipaddress, 'Netflix', 'Netflix_Ipaddress_logins', html_report, None))

            if data_list:
                data_headers = ('Timestamp', 'Ip Address', 'Esn', 'Country', 'Region code', 'Device description')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()

                tsvname = f'Netflix - IP Address Login'
                tsv(report_folder, data_headers, data_list, tsvname)

                ipgen(report_folder, ipaddress_list)

                tlactivity = f'Netflix - IP Address Login'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Netflix - Ipaddress Logins data available')

        if filename.startswith('IpAddressesStreaming.csv'):
            data_list = []
            ipaddress_list = []
            report = ArtifactHtmlReport('Netflix - IP Address Streaming')
            report.start_artifact_report(report_folder, 'Netflix - IP Address Streaming')
            html_report = report.get_report_file_path()
            report.add_script()
            has_header = True
            with open(file_found, 'r', encoding='utf-8') as f:
                delimited = csv.reader(f, delimiter=',')
                for item in delimited:
                    if has_header:
                        has_header = False
                    else:
                        esn = item[0]
                        country = item[1]
                        localized_device_desc = item[2]
                        device_desc = item[3]
                        ipaddress = item[4]
                        region_code_display_name = item[5]
                        timestamp = item[6]
                        data_list.append((timestamp, ipaddress, device_desc, localized_device_desc, region_code_display_name, esn, country))
                        if ipaddress != None:
                            ipaddress_list.append(
                                (ipaddress, 'Netflix', 'Netflix_Ipaddress_streaming', html_report, None))

            if data_list:
                data_headers = ('Timestamp', 'Ip Address', 'Device Description', 'Localized Device Description', 'Region Code Display Name', 'esn', 'Country')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()

                tsvname = f'Netflix - IP Address Streaming'
                tsv(report_folder, data_headers, data_list, tsvname)

                ipgen(report_folder, ipaddress_list)

                tlactivity = f'Netflix - IP Address Streaming'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Netflix - Ipaddress Streaming data available')

        if filename.startswith('Devices.csv'):
            data_list = []
            header_list = []
            report = ArtifactHtmlReport('Netflix - Devices')
            report.start_artifact_report(report_folder, 'Netflix - Devices')
            report.add_script()
            has_header = True
            with open(file_found, 'r', encoding='utf-8') as f:
                delimited = csv.reader(f, delimiter=',')
                for item in delimited:
                    if has_header:
                        has_header = False
                        header_list = item
                    else:
                        data_list.append(item)

            if data_list:
                data_headers = header_list
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()

                tsvname = f'Netflix - Devices'
                tsv(report_folder, data_headers, data_list, tsvname)

                tlactivity = f'Netflix - Devices'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Netflix - Devices data available')

        if filename.startswith('ViewingActivity.csv'):
            data_list = []
            header_list = []
            report = ArtifactHtmlReport('Netflix - Viewing Activity')
            report.start_artifact_report(report_folder, 'Netflix - Viewing Activity')
            report.add_script()
            has_header = True
            with open(file_found, 'r', encoding='utf-8') as f:
                delimited = csv.reader(f, delimiter=',')
                for item in delimited:
                    if has_header:
                        has_header = False
                        header_list = item
                    else:
                        data_list.append(item)

            if data_list:
                data_headers = header_list
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()

                tsvname = f'Netflix - Viewing Activity'
                tsv(report_folder, data_headers, data_list, tsvname)

                tlactivity = f'Netflix - Viewing Activity'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Netflix - Viewing Activity data available')

        if filename.startswith('SearchHistory.csv'):
            data_list = []
            header_list = []
            report = ArtifactHtmlReport('Netflix - Search History')
            report.start_artifact_report(report_folder, 'Netflix - Search History')
            report.add_script()
            has_header = True
            with open(file_found, 'r', encoding='utf-8') as f:
                delimited = csv.reader(f, delimiter=',')
                for item in delimited:
                    if has_header:
                        has_header = False
                        header_list = item
                    else:
                        data_list.append(item)

            if data_list:
                data_headers = header_list
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()

                tsvname = f'Netflix - Search History'
                tsv(report_folder, data_headers, data_list, tsvname)

                tlactivity = f'Netflix - Search History'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Netflix - Search History data available')

        if filename.startswith('AccountDetails.csv'):
            data_list = []
            user_list = []
            header_list = []
            report = ArtifactHtmlReport('Netflix - Account Details')
            report.start_artifact_report(report_folder, 'Netflix - Account Details')
            html_report = report.get_report_file_path()
            report.add_script()
            has_header = True
            with open(file_found, 'r', encoding='utf-8') as f:
                delimited = csv.reader(f, delimiter=',')
                for item in delimited:
                    if has_header:
                        has_header = False
                        header_list = item
                    else:
                        data_list.append(item)
                        if item[2] != "":
                            user_list.append((item[2], 'Netflix', 'Netflix_Account_Details', html_report, None))

            if data_list:
                data_headers = header_list
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()

                tsvname = f'Netflix - Account Details'
                tsv(report_folder, data_headers, data_list, tsvname)

                usergen(report_folder, user_list)

                tlactivity = f'Netflix - Account Details'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Netflix - Account Details data available')

        if filename.startswith('MessagesSentByNetflix.csv'):
            data_list = []
            header_list = []
            report = ArtifactHtmlReport('Netflix - Messages Sent By Netflix')
            report.start_artifact_report(report_folder, 'Netflix - Messages Sent By Netflix')
            report.add_script()
            has_header = True
            with open(file_found, 'r', encoding='utf-8') as f:
                delimited = csv.reader(f, delimiter=',')
                for item in delimited:
                    if has_header:
                        has_header = False
                        header_list = item
                    else:
                        data_list.append(item)

            if data_list:
                data_headers = header_list
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()

                tsvname = f'Netflix - Messages Sent By Netflix'
                tsv(report_folder, data_headers, data_list, tsvname)

                tlactivity = f'Netflix - Messages Sent By Netflix'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Netflix - Messages Sent By Netflix data available')



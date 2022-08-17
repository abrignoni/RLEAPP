import os
import json

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, usergen, ipgen

transaction_history_columns = ["Account_name", "Amount", "Balance", "Coinbase_id",
                               "Crypto_hash", "Currency", "Instantly_exchanged",
                               "Notes", "Timestamp", "To", "Transfer_id", "Transfer_payment_method"]
card_payment_columns = ["Customer_name", "Expiration_month", "Expiration_year", "First6", "Issue_country",
                        "Issuer", "Last4", "Postal_code", "Type"]

confirmed_devices_columns = ["Confirmed", "Ip_address", "User_agent"]

devices_used_columns = ["Accept", "Accept_encoding", "Accept_language", "Ip_address", "Platform", "Platform_version",
                        "Timezone_locale", "Timezone_string", "User_agent"]

site_activity_columns = ["Action", "Ip_address", "Source", "Time"]

third_party_columns = ["Access_granted", "Access_revoked", "Name"]


def get_coinbaseArchive(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)

        if filename.lower().startswith('coinbase_data.json'):
            transaction_data_list = []
            card_payment_data_list = []
            confirmed_data_list = []
            devices_used_data_list = []
            site_activity_data_list = []
            third_party_data_list = []
            personal_data_list = []
            with open(file_found, 'r', encoding='utf-8') as f:
                coinbaseData = json.load(f)
                for allData in coinbaseData:
                    if 'Financial' in allData:
                        for financialData in coinbaseData[allData]:
                            if 'transaction' in financialData:
                                user_list = []
                                report = ArtifactHtmlReport('Coinbase - Transactions')
                                report.start_artifact_report(report_folder, 'Coinbase - Transactions')
                                html_report = report.get_report_file_path()
                                transaction_history = coinbaseData['Financial Data'][financialData]
                                for trans_history in transaction_history:
                                    temp_list = []
                                    for column_name in transaction_history_columns:
                                        if column_name == 'To' and trans_history[column_name] != None and '@' in trans_history[column_name]:
                                            user_list.append(
                                                (trans_history[column_name], 'Coinbase Archive', 'Coinbase - Transactions', html_report, None))
                                        temp_list.append(trans_history[column_name])
                                    transaction_data_list.append(temp_list)

                                if transaction_data_list:
                                    report.add_script()
                                    data_headers = transaction_history_columns
                                    report.write_artifact_data_table(data_headers, transaction_data_list, file_found)
                                    report.end_artifact_report()

                                    tsvname = f'Coinbase - Transactions'
                                    tsv(report_folder, data_headers, transaction_data_list, tsvname)

                                    usergen(report_folder, user_list)

                                    tlactivity = f'Coinbase - Transactions'
                                    timeline(report_folder, tlactivity, transaction_data_list, data_headers)
                                else:
                                    logfunc('No Coinbase Transactions data available')

                            elif 'cards' in financialData.lower():
                                card_payment = coinbaseData['Financial Data'][financialData]
                                for card in card_payment:
                                    temp_list = []
                                    for column_name in card_payment_columns:
                                        temp_list.append(card[column_name])
                                    card_payment_data_list.append(temp_list)

                                if card_payment_data_list:
                                    report = ArtifactHtmlReport('Coinbase - Card Payment')
                                    report.start_artifact_report(report_folder, 'Coinbase - Card Payment')
                                    report.add_script()
                                    data_headers = card_payment_columns
                                    report.write_artifact_data_table(data_headers, card_payment_data_list, file_found)
                                    report.end_artifact_report()

                                    tsvname = f'Coinbase - Card Payment'
                                    tsv(report_folder, data_headers, card_payment_data_list, tsvname)

                                else:
                                    logfunc('No Card Payment data available')

                    elif 'Interactions' in allData:
                        interactionData = coinbaseData[allData]
                        for interactions in interactionData:
                            if 'Confirmed' in interactions:
                                ipaddress_list = []
                                report = ArtifactHtmlReport('Coinbase - Confirmed Devices')
                                report.start_artifact_report(report_folder, 'Coinbase - Confirmed Devices')
                                html_report = report.get_report_file_path()
                                confirmed_history = interactionData[interactions]
                                for conf_history in confirmed_history:
                                    temp_list = []
                                    for column_name in confirmed_devices_columns:
                                        if "Ip_address" in column_name and conf_history[column_name] != None:
                                            ipaddress_list.append(
                                                (conf_history[column_name], 'Coinbase Archive', 'Coinbase Confirmed Devices', html_report, None))
                                        temp_list.append(conf_history[column_name])
                                    confirmed_data_list.append(temp_list)

                                if confirmed_data_list:
                                    report.add_script()
                                    data_headers = confirmed_devices_columns
                                    report.write_artifact_data_table(data_headers, confirmed_data_list, file_found)
                                    report.end_artifact_report()

                                    tsvname = f'Coinbase - Confirmed Devices'
                                    tsv(report_folder, data_headers, confirmed_data_list, tsvname)

                                    ipgen(report_folder, ipaddress_list)

                                else:
                                    logfunc('No Coinbase Confirmed Device data available')
                            elif 'Devices' in interactions:
                                ipaddress_list = []
                                report = ArtifactHtmlReport('Coinbase - Devices Used')
                                report.start_artifact_report(report_folder, 'Coinbase - Devices Used')
                                html_report = report.get_report_file_path()
                                devices_used_history = interactionData[interactions]
                                for devices_history in devices_used_history:
                                    temp_list = []
                                    for column_name in devices_used_columns:
                                        if "Ip_address" in column_name and devices_history[column_name] != None:
                                            ipaddress_list.append(
                                                (devices_history[column_name], 'Coinbase Archive', 'Coinbase Devices Used', html_report, None))
                                        temp_list.append(devices_history[column_name])
                                    devices_used_data_list.append(temp_list)

                                if devices_used_data_list:
                                    report.add_script()
                                    data_headers = devices_used_columns
                                    report.write_artifact_data_table(data_headers, devices_used_data_list, file_found)
                                    report.end_artifact_report()

                                    tsvname = f'Coinbase - Devices Used'
                                    tsv(report_folder, data_headers, devices_used_data_list, tsvname)

                                    ipgen(report_folder, ipaddress_list)

                                    tlactivity = f'Coinbase - Devices Used'
                                    timeline(report_folder, tlactivity, devices_used_data_list, data_headers)
                                else:
                                    logfunc('No Coinbase Confirmed Device data available')
                            elif 'Site' in interactions:
                                ipaddress_list = []
                                report = ArtifactHtmlReport('Coinbase - Site Activity')
                                report.start_artifact_report(report_folder, 'Coinbase - Site Activity')
                                html_report = report.get_report_file_path()
                                site_activity_history = interactionData[interactions]
                                for site_history in site_activity_history:
                                    temp_list = []
                                    for column_name in site_activity_columns:
                                        if "Ip_address" in column_name and site_history[column_name] != None:
                                            ipaddress_list.append(
                                                (site_history[column_name], 'Coinbase Archive', 'Coinbase Site Activity', html_report, None))
                                        temp_list.append(site_history[column_name])
                                    site_activity_data_list.append(temp_list)

                                if site_activity_data_list:
                                    report.add_script()
                                    data_headers = site_activity_columns
                                    report.write_artifact_data_table(data_headers, site_activity_data_list, file_found)
                                    report.end_artifact_report()

                                    tsvname = f'Coinbase - Site Activity'
                                    tsv(report_folder, data_headers, site_activity_data_list, tsvname)

                                    ipgen(report_folder, ipaddress_list)

                                    tlactivity = f'Coinbase - Site Activity'
                                    timeline(report_folder, tlactivity, site_activity_data_list, data_headers)
                                else:
                                    logfunc('No Coinbase Site Activity data available')
                            elif 'Third' in interactions:
                                third_party_activity_history = interactionData[interactions]
                                for third_party_history in third_party_activity_history:
                                    temp_list = []
                                    for column_name in third_party_columns:
                                        temp_list.append(third_party_history[column_name])
                                    third_party_data_list.append(temp_list)

                                if third_party_data_list:
                                    report = ArtifactHtmlReport('Coinbase - 3rd party authorizations')
                                    report.start_artifact_report(report_folder, 'Coinbase - 3rd party authorizations')
                                    report.add_script()
                                    data_headers = third_party_columns
                                    report.write_artifact_data_table(data_headers, third_party_data_list, file_found)
                                    report.end_artifact_report()

                                    tsvname = f'Coinbase - 3rd party authorizations'
                                    tsv(report_folder, data_headers, third_party_data_list, tsvname)

                                else:
                                    logfunc('No Coinbase 3rd party auths data available')
                    elif 'Personal' in allData:
                        report = ArtifactHtmlReport('Coinbase - Personal Data')
                        report.start_artifact_report(report_folder, 'Coinbase - Personal Data')
                        html_report = report.get_report_file_path()
                        personalData = coinbaseData[allData]
                        for personal in personalData:
                            if 'Addresses' in personal:
                                address_history = personalData[personal]
                                for addr_history in address_history:
                                    temp_list = []
                                    temp_list.append("Address")
                                    address_string = ""
                                    for column_name in addr_history.keys():
                                        if addr_history[column_name] != None:
                                            address_string = address_string + addr_history[column_name] + "\n"
                                    temp_list.append(address_string)
                                    personal_data_list.append(temp_list)
                            elif 'Employers' in personal:
                                employer_history = personalData[personal]
                                for emp_history in employer_history:
                                    for column_name in emp_history.keys():
                                        temp_list = []
                                        temp_list.append(column_name)
                                        temp_list.append(emp_history[column_name])
                                        personal_data_list.append(temp_list)
                            else:
                                if 'Section' in personal:
                                    pass
                                elif 'Emails' in personal:
                                    temp_list = []
                                    temp_list.append(personal)
                                    temp_list.append(personalData[personal])
                                    personal_data_list.append(temp_list)
                                    user_list.append(
                                        (personalData[personal], 'Coinbase Archive', 'Coinbase - Personal Data',
                                         html_report, None))

                                else:
                                    temp_list = []
                                    temp_list.append(personal)
                                    temp_list.append(personalData[personal])
                                    personal_data_list.append(temp_list)

                        if personal_data_list:
                            report.add_script()
                            data_headers = ('Name', 'Value')
                            report.write_artifact_data_table(data_headers, personal_data_list, file_found)
                            report.end_artifact_report()

                            tsvname = f'Coinbase - Personal Data'
                            tsv(report_folder, data_headers, personal_data_list, tsvname)

                            usergen(report_folder, user_list)

                        else:
                            logfunc('No Coinbase Personal data available')

__artifacts__ = {
        "coinbaseArchive": (
            "Coinbase Archive",
            ('**/coinbase_data.json'),
            get_coinbaseArchive)
}
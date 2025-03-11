#Author: Shawn Ramsey
#Date: 
#Description:   Parse a Cash App Search Warrant return and produce reports
#               with information deemed important for follow-up investigations as well as proper analysis
#               At the completion of this module, multiple datasets will be extracted, counted, and compared
#               in order to identify overlapping information and associated accounts previously difficult to map.

import os
import datetime
import hashlib
import json
import re
from openpyxl import workbook
from openpyxl import load_workbook
from pathlib import Path

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html, kmlgen, gather_hashes_in_file, ipgen

# Class to hold all of the information for an account
# Potentially build this out for persistent tracking across cases?
class AccountInfo:
    def __init__(self, account_token, name = "", dob = "0000-00-00", ssn = 0):
        self.account_token = account_token
        self.name = name
        self.dob = dob
        self.ssn = ssn
        self.display_names = []
        self.emails = []
        self.phone_numbers = []
        self.cashtags = []
        self.ipv4_list = []
        self.ipv6_list = []
        self.cards = []
        self.banks = []
        self.issued_virtual_cards = []
        self.issued_physical_cards = []
        self.issued_bank_accounts = []

    def add_display_name(self, display_name):
        self.display_names.append(display_name)
    
    def add_email(self, email, date):
        self.emails.append((email, date))
    
    def add_phone_number(self, phone_number, date):
        self.phone_numbers.append((phone_number, date))
    
    def add_cashtag(self, cashtag, date):
        self.cashtags.append((cashtag, date))
    
    def add_ipv4(self, ipaddress):
        self.ipv4_list.append(ipaddress)
    
    def add_ipv6(self, ipaddress):
        self.ipv6_list.append(ipaddress)
    
    def add_card(self, card_number, brand, zipcode):
        self.cards.append((card_number, brand, zipcode))

    def add_bank_account(self, bank_account, routing_number):
        self.banks.append((bank_account, routing_number))
    
    def add_issued_virtual_card(self, card_number, issued_date = "N/A"):
        self.issued_virtual_cards.append((card_number, issued_date))

    def add_issued_physical_card(self, card_number, issued_date = "N/A", address = "N/A"):
        self.issued_physical_cards.append((card_number, issued_date, address))

    def add_issued_bank_account(self, bank_account, routing_number):
        self.issued_bank_accounts.append((bank_account, routing_number))

def get_cashappReturns(files_found, report_folder, seeker, wrap_text):
    # log show ./system_logs.logarchive --style ndjson --predicate 'category = "CashApp"' > cashapp.ndjson

    # Probably needs to be deleted
    emailslist = []
    
    # List for information associated to an account token
    #account_information_list
    master_email_list = []
    master_ipv4_list = []
    master_ipv6_list = []
    master_phone_list = []

    # This is the same for every search warrant return that I have obtained and is just before the account token, we can use this to split
    account_token_substr = "-for-subject-SQ_CASH-"

    # These are the regex's for currently obtained information
    # These are compiled as they are used often
    email_regex = re.compile(r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")
    ipv4_regex = re.compile("^(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
    ipv6_regex = re.compile("^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$")
    phone_regex = re.compile("^\\+?[1-9][0-9]{7,14}$")

    #found_emails = {}


    for file_found in files_found:
        file_found = str(file_found)

        if file_found.endswith('.xlsx'):
            # Lists that we'll be using in each section
            email_list = []
            ipv4_list = []
            ipv6_list = []
            phone_list = []

            # List to pass on IP's to ipgen()
            ipaddress_list = []
            ipaddress_gen = []
            #Lets go ahead ahead and pull our Account token to be used for generating page specific reports and tagging IP's, emails, phone numbers, etc to individual accounts
            account = AccountInfo((file_found[file_found.index(account_token_substr) + len(account_token_substr):]).removesuffix('.xlsx'))
            account_token = (file_found[file_found.index(account_token_substr) + len(account_token_substr):]).removesuffix('.xlsx')
            logfunc("Proccessing Cash App Account Token: " + account_token)

            # Lets load our workbook
            workbook = load_workbook(file_found)
            sheets = workbook.sheetnames
            for sheet in sheets:
                current_sheet = workbook[sheet]
                for i in range(1, current_sheet.max_row+1):
                    for j in range(1, current_sheet.max_column+1):
                        cell_obj = current_sheet.cell(row=i, column=j)  
                        if re.match(email_regex, str(cell_obj.value)):
                            email_match = str(cell_obj.value)
                            date = current_sheet.cell(row=i, column=j-1).value

                            # Lets add this email to our Account Object
                            account.add_email(email_match, date)
                            email_list.append((account_token, date, email_match))
                            #master_email_list.append()
                            logfunc("I have located an email: " + email_match)
                        
                        # Lets look if this is an IPv4
                        if re.match(ipv4_regex, str(cell_obj.value)):
                            ipv4_match = str(cell_obj.value)
                            # Lets add this IPv4 to our Account Object
                            account.add_ipv4(ipv4_match)
                            ipaddress_list.append(ipv4_match)
                            ipv4_list.append((account_token, ipv4_match))
                            logfunc("I have located an IPv4: " + ipv4_match)

                        # Lets look if this is an IPv6
                        if re.match(ipv6_regex, str(cell_obj.value)):
                            ipv6_match = str(cell_obj.value)
                            # Lets add this IPv6 to our Account Object
                            account.add_ipv6(ipv6_match)
                            ipv6_list.append((account_token, ipv6_match))
                            logfunc("I have located an IPv6: " + ipv6_match)
                        
                        # Lets look if this is a Phone Number
                        if re.match(phone_regex, str(cell_obj.value)):
                            phone_match = str(cell_obj.value)
                            if "Full SSN" not in str(current_sheet.cell(row=i-1, column=j).value):
                                try:
                                    date = current_sheet.cell(row=i, column=j-1).value
                                    # Lets add this phone number to our Account Object
                                    account.add_phone_number(phone_match, date)
                                    phone_list.append((account_token, date, phone_match))
                                    logfunc("I have located a phone number: " + phone_match)
                                except:
                                    logfunc("Errored out with: " + str(current_sheet.cell(row=1, column=j).value))
                        
                        if str(current_sheet.cell(row=i, column=j).value) == "Display Name History":
                            a = 1
                            while (current_sheet.cell(row=i+a, column=j).value is not None):
                                account.add_display_name(str(current_sheet.cell(row=i+a, column=j).value))
                                logfunc("Added Display name: " + (str(current_sheet.cell(row=i+a, column=j).value)))
                                a += 1

                        if str(current_sheet.cell(row=i, column=j).value) == "Payment Source History":
                            # We're going to skip the Card header for this
                            a = 2
                            while (current_sheet.cell(row=i+a, column=j).value is not None):
                                # Lets add these card details to our Account Object
                                account.add_card(
                                    (current_sheet.cell(row=i+a, column=j).value),
                                    str(current_sheet.cell(row=i+a, column=j+1).value),
                                    (current_sheet.cell(row=i+a, column=j+2).value)
                                    )
                                a += 1

                            # We'll increase our a by 1 to skip the white space and go to Bank Account Number
                            # (It looks like there is always a single blank space after the last card number
                            # and before the Bank Account Number header)
                            a += 1
                            if str(current_sheet.cell(row=i+a, column=j).value) == "Bank Account Number":
                                a += 1
                                while (current_sheet.cell(row=i+a, column=j).value is not None):
                                    # Lets add these card details to our Account Object
                                    account.add_bank_account(
                                        (current_sheet.cell(row=i+a, column=j).value),
                                        (current_sheet.cell(row=i+a, column=j+1).value)
                                        )
                                    a += 1

                        if str(current_sheet.cell(row=i, column=j).value) == "Issued Instruments":
                            # We're going to skip the Virtual Card Number header for this
                            a = 2
                            while (current_sheet.cell(row=i+a, column=j).value is not None):
                                # Lets add these card details to our Account Object
                                account.add_issued_virtual_card(
                                    (current_sheet.cell(row=i+a, column=j).value),
                                    (current_sheet.cell(row=i+a, column=j+1).value)
                                    )
                                a += 1

                            # We'll increase our a by 1 to skip the white space and go to Physical Card Number
                            # (It looks like there is always a single blank space after the last card number
                            # and before the Physical Card Number header)
                            a += 1
                            if str(current_sheet.cell(row=i+a, column=j).value) == "Physical Card Number":
                                a += 1
                                while (current_sheet.cell(row=i+a, column=j).value is not None):
                                    # Lets add these card details to our Account Object
                                    account.add_issued_physical_card(
                                        (current_sheet.cell(row=i+a, column=j).value),
                                        (current_sheet.cell(row=i+a, column=j+1).value),
                                        (current_sheet.cell(row=i+a, column=j+2).value)
                                        )
                                    a += 1

                            # We'll increase our a by 1 to skip the white space and go to Bank Account Number
                            # (It looks like there is always a single blank space after the last card number
                            # and before the Bank Account Number header)
                            a += 1
                            if str(current_sheet.cell(row=i+a, column=j).value) == "Bank Account Number":
                                a += 1
                                while (current_sheet.cell(row=i+a, column=j).value is not None):
                                    # Lets add these card details to our Account Object
                                    account.add_issued_bank_account(
                                        (current_sheet.cell(row=i+a, column=j).value),
                                        (current_sheet.cell(row=i+a, column=j+1).value)
                                        )
                                    a += 1
            if email_list:
                report = ArtifactHtmlReport(f'CashApp - Emails')
                report.start_artifact_report(report_folder, f'CashApp - Emails - {account_token}')
                report.add_script()
                email_headers = ('Account Token', 'UTC Date Time', 'Email')
                report.write_artifact_data_table(email_headers, email_list, file_found, html_no_escape=['Media'])
                report.end_artifact_report()

                tsvname = f'CashApp - Emails - {account_token}'
                tsv(report_folder, email_headers, email_list, tsvname)

                tlactivity = f'CashApp - Emails - {account_token}'
                timeline(report_folder, tlactivity, email_list, email_headers)
            else:
                logfunc(f'No CashApp - Emails - {account_token}')

            if ipv4_list:
                report = ArtifactHtmlReport(f'CashApp - IPv4')
                report.start_artifact_report(report_folder, f'CashApp - IPv4 - {account_token}')
                html_report = report.get_report_file_path()
                report.add_script()
                ipv4_headers = ('Account Token', 'IPv4')
                report.write_artifact_data_table(ipv4_headers, ipv4_list, file_found, html_no_escape=['Media'])
                report.end_artifact_report()

                # Loop through the list and build the IP Address Database
                a = 0
                length = len(ipaddress_list)
                while a < length:
                    ipaddress_gen.append((ipaddress_list[a], 'CashApp', 'CashApp IPv4 Return - ' + account_token, html_report, None))
                    a += 1

                ipgen(report_folder, ipaddress_gen)

                tsvname = f'CashApp - IPv4 - {account_token}'
                tsv(report_folder, ipv4_headers, ipv4_list, tsvname)

                tlactivity = f'CashApp - IPv4 - {account_token}'
                timeline(report_folder, tlactivity, ipv4_list, ipv4_headers)
            else:
                logfunc(f'No CashApp - IPv4 - {account_token}')

            if ipv6_list:
                report = ArtifactHtmlReport(f'CashApp - IPv6')
                report.start_artifact_report(report_folder, f'CashApp - IPv6 - {account_token}')
                report.add_script()
                ipv6_headers = ('Account Token', 'IPv6')
                report.write_artifact_data_table(ipv6_headers, ipv6_list, file_found, html_no_escape=['Media'])
                report.end_artifact_report()

                ipgen(report_folder, ipaddress_list)

                tsvname = f'CashApp - IPv6 - {account_token}'
                tsv(report_folder, ipv6_headers, ipv6_list, tsvname)

                tlactivity = f'CashApp - IPv6 - {account_token}'
                timeline(report_folder, tlactivity, ipv6_list, ipv6_headers)
            else:
                logfunc(f'No CashApp - IPv6 - {account_token}')

            if phone_list:
                report = ArtifactHtmlReport(f'CashApp - Phone Numbers')
                report.start_artifact_report(report_folder, f'CashApp - Phone Numbers - {account_token}')
                report.add_script()
                phone_headers = ('Account Token', 'UTC Date Time', 'Phone Numbers')
                report.write_artifact_data_table(phone_headers, phone_list, file_found, html_no_escape=['Media'])
                report.end_artifact_report()

                tsvname = f'CashApp - Phone Numbers - {account_token}'
                tsv(report_folder, phone_headers, phone_list, tsvname)

                tlactivity = f'CashApp - Phone Numbers - {account_token}'
                timeline(report_folder, tlactivity, phone_list, phone_headers)
            else:
                logfunc(f'No CashApp - Phone Numbers - {account_token}')

__artifacts__ = {
    "cashappReturns": (
        "Cash App Returns",
        ('*/*-for-subject-SQ_CASH-*.xlsx'),
        get_cashappReturns)
}

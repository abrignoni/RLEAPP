# Module Description: Parses Google Pay transactions from Takeout
# Author: @KevinPagano3
# Date: 2021-09-25
# Artifact version: 0.0.1
# Requirements: none

import os
import datetime
import csv

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_googlePayTransactions(files_found, report_folder, seeker, wrap_text):

    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('transactions'):
            data_list = []

            has_header = True
            with open(file_found, 'r', encoding='utf-8') as f:
                delimited = csv.reader(f, delimiter=',')
                
                next(delimited)
                for item in delimited:
                    if len(item) == 0:
                        continue
                    else:
                        trans_time = item[0]
                        trans_id = item[1]
                        description = item[2]
                        product = item[3]
                        payment_method = item[4]
                        payment_status = item[5]
                        payment_amount = item[6]
                       
                        data_list.append((trans_time,trans_id,description,product,payment_method,payment_status,payment_amount))
                    
            if data_list:
                description = 'Purchases on Google like Play and YouTube, and purchases made using Google Pay balance.'
                report = ArtifactHtmlReport('Google Pay Transactions')
                report.start_artifact_report(report_folder, 'Google Pay Transactions', description)
                html_report = report.get_report_file_path()
                report.add_script()
                data_headers = ('Transaction Timestamp','Transaction ID','Description','Product','Payment Method','Payment Status','Amount')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Google Pay Transactions'
                tsv(report_folder, data_headers, data_list, tsvname)

                tlactivity = f'Google Pay Transactions'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Google Pay Transactions data available')
                
__artifacts__ = {
        "googlePayTransactions": (
            "Google Takeout Archive",
            ('*/Google Pay/Google transactions/transactions_*.csv'),
            get_googlePayTransactions)
}
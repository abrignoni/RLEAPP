# Module Description: Parses Google Play Store purchase history from Takeout
# Author: @KevinPagano3
# Date: 2021-08-20
# Artifact version: 0.0.1
# Requirements: none

import datetime
import json
import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_playStorePurchaseHistory(files_found, report_folder, seeker, wrap_text, time_offset):
    
    for file_found in files_found:
        file_found = str(file_found)
        if not os.path.basename(file_found) == 'Purchase History.json': # skip -journal and other files
            continue

        with open(file_found, encoding = 'utf-8', mode = 'r') as f:
            data = json.loads(f.read())
        data_list = []

        for x in data:
            invoicePrice = x['purchaseHistory'].get('invoicePrice','')
            paymentMethod = x['purchaseHistory'].get('paymentMethodTitle','')
            userCountry = x['purchaseHistory'].get('userCountry','')
            documentType = x['purchaseHistory']['doc'].get('documentType','')

            itemTitle = x['purchaseHistory']['doc'].get('title','')
            purchaseTime = x['purchaseHistory'].get('purchaseTime','')
            purchaseTime = purchaseTime.replace('T', ' ').replace('Z', '')
           
            data_list.append((purchaseTime, itemTitle, documentType, invoicePrice, paymentMethod, userCountry))

        num_entries = len(data_list)
        if num_entries > 0:
            description = 'List of your Google Play purchases.'
            report = ArtifactHtmlReport('Google Play Store Purchase History')
            report.start_artifact_report(report_folder, 'Google Play Store Purchase History', description)
            report.add_script()
            data_headers = ('Purchase Timestamp','Item Title','Document Type','Price','Payment Method','User Country') 

            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()
            
            tsvname = f'Google Play Store Purchase History'
            tsv(report_folder, data_headers, data_list, tsvname)
            
            tlactivity = f'Google Play Store Purchase History'
            timeline(report_folder, tlactivity, data_list, data_headers)
        else:
            logfunc('No Google Play Store Purchase History data available')

__artifacts__ = {
        "playStorePurchaseHistory": (
            "Google Takeout Archive",
            ('*/Google Play Store/Purchase History.json'),
            get_playStorePurchaseHistory)
}
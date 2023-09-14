# Module Description: Parses Fitbit oxygen saturation details from Google Takeout
# Author: @KevinPagano3
# Date: 2023-09-14
# Artifact version: 0.0.1
# Requirements: none

import os
import datetime
import csv

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, ipgen

def get_fitbit_SPO2(files_found, report_folder, seeker, wrap_text):

    data_list = []

    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        source_file = os.path.dirname(file_found) + '\\Daily SpO2 - *.csv'
            
        description = 'Oxygen saturation reports for a Fitbit account'
        report = ArtifactHtmlReport('Fitbit Oxygen Saturation (SpO2)')
        report.start_artifact_report(report_folder, 'Fitbit Oxygen Saturation (SpO2)', description)
        html_report = report.get_report_file_path()
        report.add_script()
        has_header = True
        
        with open(file_found, 'r', encoding='utf-8') as f:
            delimited = csv.reader(f, delimiter=',')
            next(delimited)
            for item in delimited:
                timestamp = item[0].replace('T',' ').replace('Z','')
                average_value = item[1]
                lower_bound = item[2]
                upper_bound = item[3]
                
                data_list.append((timestamp,average_value,lower_bound,upper_bound,filename))
                    

    if len(data_list) > 0:
        data_headers = ('Timestamp','Average Value','Lower Bound','Upper Bound','Source File')
        report.write_artifact_data_table(data_headers, data_list, source_file)
        report.end_artifact_report()
        
        tsvname = f'Fitbit Oxygen Saturation (SpO2)'
        tsv(report_folder, data_headers, data_list, tsvname)

        tlactivity = f'Fitbit Oxygen Saturation (SpO2)'
        timeline(report_folder, tlactivity, data_list, data_headers)
    else:
        logfunc('No Fitbit Oxygen Saturation (SpO2) data available')

__artifacts__ = {
        "fitbit_SPO2": (
            "Google Takeout Archive",
            ('*/Fitbit/Oxygen Saturation (SpO2)/Daily SpO2 - *.csv'),
            get_fitbit_SPO2)
}
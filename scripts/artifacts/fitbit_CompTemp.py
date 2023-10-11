# Module Description: Parses Fitbit computed temperatures from Google Takeout
# Author: @KevinPagano3
# Date: 2023-09-14
# Artifact version: 0.0.1
# Requirements: none

import os
import datetime
import csv

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, ipgen

def get_fitbit_CompTemp(files_found, report_folder, seeker, wrap_text, time_offset):

    data_list = []

    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        source_file = os.path.dirname(file_found) + '\\Computed Temperature - *.csv'
            
        description = 'Computed temperatures for a Fitbit account'
        report = ArtifactHtmlReport('Fitbit Computed Temperature')
        report.start_artifact_report(report_folder, 'Fitbit Computed Temperature', description)
        html_report = report.get_report_file_path()
        report.add_script()
        has_header = True
        
        with open(file_found, 'r', encoding='utf-8') as f:
            delimited = csv.reader(f, delimiter=',')
            next(delimited)
            for item in delimited:
                comp_type = item[0]
                sleep_start = item[1].replace('T',' ')
                sleep_end = item[2].replace('T',' ')
                temp_samples = item[3]
                nightly_temp = item[4]
                base_rel_sample_sum = item[5]
                base_rel_sample_sum_square = item[6]
                base_rel_nightly_stand_dev = item[7]
                base_rel_sample_stand_dev = item[8]
                
                data_list.append((sleep_start,sleep_end,comp_type,temp_samples,nightly_temp,base_rel_sample_sum,base_rel_sample_sum_square,base_rel_nightly_stand_dev,base_rel_sample_stand_dev,filename))

    if len(data_list) > 0:
        data_headers = ('Sleep Start Timestamp','Sleep End Timestamp','Type','Temperature Sample Count','Nightly Temperature (C)','Baseline Relative Sample Sum','Baseline Relative Sample (Sum of Squares)','Baseline Relative Nightly Standard Deviation','Baseline Relative Sample Standard Deviation','Source File')
        report.write_artifact_data_table(data_headers, data_list, source_file)
        report.end_artifact_report()
        
        tsvname = f'Fitbit Computed Temperature'
        tsv(report_folder, data_headers, data_list, tsvname)

        tlactivity = f'Fitbit Computed Temperature'
        timeline(report_folder, tlactivity, data_list, data_headers)
    else:
        logfunc('No Fitbit Computed Temperature data available')

__artifacts__ = {
        "fitbit_CompTemp": (
            "Google Takeout Archive",
            ('*/Fitbit/Temperature/Computed Temperature - *.csv'),
            get_fitbit_CompTemp)
}
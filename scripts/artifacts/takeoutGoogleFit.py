import os
import datetime
import csv

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_takeoutGoogleFit(files_found, report_folder, seeker, wrap_text):

    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('Daily activity metrics.csv'):
            data_list = []

            has_header = True
            with open(file_found, 'r', encoding='utf-8') as f:
                delimited = csv.reader(f, delimiter=',')
                for item in delimited:
                    if has_header:
                        has_header = False
                    else:
                        day_date = item[0]
                        move_minutes = item[1]
                        calories = item[2]
                        distance = item[3]
                        heart_points = item[4]
                        heart_minutes = item[5]
                        avg_bpm = item[6]
                        max_bpm = item[7]
                        min_bpm = item[8]
                        low_lat = item[9]
                        low_long = item[10]
                        high_lat = item[11]
                        high_long = item[12]
                        data_list.append((day_date,move_minutes,calories,distance,heart_points,heart_minutes,avg_bpm,max_bpm,min_bpm,low_lat,low_long,high_lat,high_long))
            
            if data_list:
                description = 'Daily totals for each activity metric, like steps and distance.'
                report = ArtifactHtmlReport('Google Fit - Daily Activity Metrics')
                report.start_artifact_report(report_folder, 'Google Fit - Daily Activity Metrics', description)
                html_report = report.get_report_file_path()
                report.add_script()
                data_headers = ('Date','Move Minutes','Calories (kcal)','Distance (m)','Heart Points','Heart Minutes','Average Heart Rate (BPM)','Max Heart Rate (BPM)','Min Heart Rate (BPM)','Low Latitude','Low Longitude','High Latitude','High Longitude')
                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Google Fit - Daily Activity Metrics'
                tsv(report_folder, data_headers, data_list, tsvname)

                tlactivity = f'Google Fit - Daily Activity Metrics'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Google Fit - Daily Activity Metrics data available')
                
__artifacts_v2__ = {
    "takeout_google_fit": {
        "name": "Google Fit - Daily Activity Metrics",
        "description": "Parses Google Fit daily metrics from Takeout archive",
        "author": "@stark4n6",
        "creation_date": "2021-09-25",
        "last_update_date": "2026-06-19",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": ('*/Fit/Daily activity metrics/Daily activity metrics.csv',),
        "output_types": "standard",  # or ["html", "tsv", "timeline", "lava"]
        "artifact_icon": "activity",
    }
}

import csv

from scripts.ilapfuncs import artifact_processor, get_file_path

@artifact_processor
def takeout_google_fit(context):
    files_found = context.get_files_found()
    data_list = []
    file_found = get_file_path(files_found, 'Daily activity metrics.csv')
        
    with open(file_found, 'r', encoding='utf-8') as f:
        delimited = csv.reader(f, delimiter=',')
        
        next(delimited)
        for item in delimited:
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

    data_headers = ('Date','Move Minutes','Calories (kcal)','Distance (m)','Heart Points','Heart Minutes','Average Heart Rate (BPM)','Max Heart Rate (BPM)','Min Heart Rate (BPM)','Low Latitude','Low Longitude','High Latitude','High Longitude')
    
    return data_headers, data_list, file_found

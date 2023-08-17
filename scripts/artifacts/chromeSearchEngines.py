# Module Description: Parses Google Chrome Search Engines from Takeout
# Author: @upintheairsheep
# Date: 2023-07-13
# Artifact version: 0.0.0
# Requirements: none

import datetime
import json
import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_chromeSearchEngines(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        if not os.path.basename(file_found) == 'SearchEngines.json': # skip -journal and other files
            continue

        with open(file_found, encoding = 'utf-8', mode = 'r') as f:
            data = json.loads(f.read())
        data_list = []
        
        sEng_suggestions_url = ''
        sEng_favicon_url = ''
        sEng_safeAreplace = ''
        sEng_date = ''
        sEng_url = ''
        sEng_ntpurl = ''
        sEng_originUrl = ''
        sEng_syncGUID = ''
        sEng_shortName = ''
        sEng_kWord = ''
        sEng_inputEnc = ''
        sEng_prePopID = ''
        sEng_lastModified = ''
        sEng_imageurlpostparams = ''
        sEng_isActive = ''
        sEng_imageurl = ''
        sEng_starterpackID = ''





        for site in data['Search Extensions']:
            
            sEng_suggestions_url = site['suggestions_url']
            sEng_favicon_url = site['favicon_url']
            sEng_safeAreplace = site['safe_for_autoreplace']
            sEng_date = site['date_created']
            sEng_url = site['url']
            sEng_ntpurl = site['new_tab_url']
            sEng_originUrl = site['originating_url']
            sEng_syncGUID = site['sync_guid']
            sEng_shortName = site['short_name']
            sEng_kWord = site['keyword']
            sEng_inputEnc = site['input_encodings']
            sEng_prePopID = site['prepopulate_id']
            sEng_lastModified = site['last_modified']
            sEng_imageurlpostparams = site['image_url_post_params']
            sEng_isActive = site['is_active']
            sEng_imageurl = site['image_url']
            sEng_starterpackID = site['starter_pack_id']
               
            data_list.append((sEng_shortName, sEng_kWord, sEng_date, sEng_lastModified, url, sEng_originUrl, sEng_syncGUID, sEng_favicon_url, sEng_suggestions_url, sEng_ntpurl, sEng_inputEnc, sEng_safeAreplace, sEng_prePopID, sEng_imageurlpostparams, sEng_isActive, sEng_imageurl, sEng_starterpackID))

        num_entries = len(data_list)
        if num_entries > 0:
            report = ArtifactHtmlReport('Chrome Search Engines')
            report.start_artifact_report(report_folder, 'Chrome Search Engines')
            report.add_script()
            data_headers = ('(Short) Name','Keyword','Date Created','Last Modified','URL Syntax','API URL', 'Sync GUID', 'Favicon URL', 'Suggestions URL', 'New Tab URL', 'Input Encodings', 'Safe Autoreplace?', 'Pre-populate ID', 'Image URL Post Parameters', 'Is Active?', 'Image URL', 'Starter Pack ID')

            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()
            
            tsvname = f'Chrome Search Engines'
            tsv(report_folder, data_headers, data_list, tsvname)
            
            tlactivity = f'Chrome Search Engines'
            timeline(report_folder, tlactivity, data_list, data_headers)
        else:
            logfunc('No Chrome Search Engines data available')

__artifacts__ = {
        "chromeSearchEngines": (
            "Google Takeout Archive",
            ('*/Chrome/SearchEngines.json'),
            get_chromeExtensions)
}

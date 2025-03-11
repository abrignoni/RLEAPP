# Module Description: Parses Google Chrome Search Engines from Takeout
# Author: @upintheairsheep & @KevinPagano3
# Date: 2023-08-17
# Artifact version: 0.0.1
# Requirements: none

import datetime
import json
import os
import textwrap

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_chromeSearchEngines(files_found, report_folder, seeker, wrap_text):

    for file_found in files_found:
        file_found = str(file_found)

        with open(file_found, encoding = 'utf-8', mode = 'r') as f:
            data = json.loads(f.read())
        data_list = []

        for site in data['Search Engines']:
            sEng_date = site.get('date_created','')
            if sEng_date == 0:
                sEng_date = ''
            else:
                sEng_date = datetime.datetime.fromtimestamp(int(sEng_date)/1000000).strftime('%Y-%m-%d %H:%M:%S.%f')
            sEng_lastModified = site.get('last_modified','')
            if sEng_lastModified == 0:
                sEng_lastModified = ''
            else:
                sEng_lastModified = datetime.datetime.fromtimestamp(int(sEng_lastModified)/1000000).strftime('%Y-%m-%d %H:%M:%S.%f')
            sEng_suggestions_url = site.get('suggestions_url','')
            sEng_favicon_url = site.get('favicon_url','')
            sEng_safeAreplace = site.get('safe_for_autoreplace','')
            sEng_url = site.get('url','')
            sEng_ntpurl = site.get('new_tab_url','')
            sEng_originUrl = site.get('originating_url','')
            sEng_syncGUID = site.get('sync_guid','')
            sEng_shortName = site.get('short_name','')
            sEng_kWord = site.get('keyword','')
            sEng_inputEnc = site.get('input_encodings','')
            sEng_prePopID = site.get('prepopulate_id','')
            sEng_imageurlpostparams = site.get('image_url_post_params','')
            sEng_isActive = site.get('is_active','')
            sEng_imageurl = site.get('image_url','')
            sEng_starterpackID = site.get('starter_pack_id','')

            data_list.append((sEng_date, sEng_lastModified, sEng_shortName, sEng_kWord, textwrap.fill(sEng_url, width=100), sEng_originUrl, sEng_syncGUID, sEng_favicon_url, sEng_suggestions_url, sEng_ntpurl, sEng_inputEnc, sEng_safeAreplace, sEng_prePopID, sEng_imageurlpostparams, sEng_isActive, sEng_imageurl, sEng_starterpackID))

        num_entries = len(data_list)
        if num_entries > 0:
            report = ArtifactHtmlReport('Chrome Search Engines')
            report.start_artifact_report(report_folder, 'Chrome Search Engines')
            report.add_script()
            data_headers = ('Date Created','Date Last Modified','(Short) Name','Keyword','URL Syntax','API URL', 'Sync GUID', 'Favicon URL', 'Suggestions URL', 'New Tab URL', 'Input Encodings', 'Safe Autoreplace?', 'Pre-populate ID', 'Image URL Post Parameters', 'Is Active?', 'Image URL', 'Starter Pack ID')

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
            get_chromeSearchEngines)
}
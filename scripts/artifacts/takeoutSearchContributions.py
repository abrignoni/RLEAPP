# Module Description: Parses Google Search Contributions from Takeout
# Author: Gemini (tested on real Takeouts)
# Date: 2025-07-21
# Artifact version: 1.0
# Requirements: none

import datetime
import json
import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_takeoutSearchContributions(files_found, report_folder, seeker, wrap_text):
    
    streaming_providers = []
    reviews = []
    watched = []
    thumbs = []

    for file_found in files_found:
        file_found = str(file_found)
        filename = os.path.basename(file_found)

        with open(file_found, encoding='utf-8', mode='r') as f:
            try:
                data = json.loads(f.read())
            except json.JSONDecodeError:
                logfunc(f'Error decoding JSON from file: {filename}')
                continue

        if filename == 'Streaming video providers.json':
            for item in data:
                provider_name = item.get('Provider Name', '')
                published = item.get('Published', '').replace('T', ' ').replace('Z', '')
                streaming_providers.append((published, provider_name))

        elif filename == 'Reviews.json':
            for item in data:
                published = item.get('Published', '').replace('T', ' ').replace('Z', '')
                updated = item.get('Updated', '').replace('T', ' ').replace('Z', '')
                comment = item.get('Review Comment', '')
                rating = item.get('Review Star Rating', '')
                query = item.get('Search Query', '')
                reviews.append((published, updated, query, rating, comment))

        elif filename == 'Watched.json':
            for item in data:
                published = item.get('Published', '').replace('T', ' ').replace('Z', '')
                query = item.get('Search Query', '')
                watched.append((published, query))

        elif filename == 'Thumbs.json':
            for item in data:
                published = item.get('Published', '').replace('T', ' ').replace('Z', '')
                updated = item.get('Updated', '').replace('T', ' ').replace('Z', '')
                query = item.get('Search Query', '')
                rating = item.get('Thumbs Rating', '')
                thumbs.append((published, updated, query, rating))

    if streaming_providers:
        description = 'User-reported information about streaming providers that the user is subscribed to.'
        report = ArtifactHtmlReport('Google Search Contributions - Streaming Providers')
        report.start_artifact_report(report_folder, 'Google Search Contributions - Streaming Providers', description)
        report.add_script()
        data_headers = ('Published Timestamp', 'Provider Name')
        report.write_artifact_data_table(data_headers, streaming_providers, files_found[0])
        report.end_artifact_report()
        
        tsvname = 'Google Search Contributions - Streaming Providers'
        tsv(report_folder, data_headers, streaming_providers, tsvname)
        
        tlactivity = 'Google Search Contributions - Streaming Providers'
        timeline(report_folder, tlactivity, streaming_providers, data_headers)
    else:
        logfunc('No Google Search Contributions - Streaming Providers data available')

    if reviews:
        description = 'Reviews for movies, TV shows, music albums, etc.'
        report = ArtifactHtmlReport('Google Search Contributions - Reviews')
        report.start_artifact_report(report_folder, 'Google Search Contributions - Reviews', description)
        report.add_script()
        data_headers = ('Published Timestamp', 'Updated Timestamp', 'Search Query', 'Star Rating', 'Comment')
        report.write_artifact_data_table(data_headers, reviews, files_found[0])
        report.end_artifact_report()
        
        tsvname = 'Google Search Contributions - Reviews'
        tsv(report_folder, data_headers, reviews, tsvname)
        
        tlactivity = 'Google Search Contributions - Reviews'
        timeline(report_folder, tlactivity, reviews, data_headers)
    else:
        logfunc('No Google Search Contributions - Reviews data available')

    if watched:
        description = 'Movies and TV shows that the user reported as already watched.'
        report = ArtifactHtmlReport('Google Search Contributions - Watched')
        report.start_artifact_report(report_folder, 'Google Search Contributions - Watched', description)
        report.add_script()
        data_headers = ('Published Timestamp', 'Search Query')
        report.write_artifact_data_table(data_headers, watched, files_found[0])
        report.end_artifact_report()
        
        tsvname = 'Google Search Contributions - Watched'
        tsv(report_folder, data_headers, watched, tsvname)
        
        tlactivity = 'Google Search Contributions - Watched'
        timeline(report_folder, tlactivity, watched, data_headers)
    else:
        logfunc('No Google Search Contributions - Watched data available')

    if thumbs:
        description = 'Thumb ratings for movies, TV shows, music albums, etc.'
        report = ArtifactHtmlReport('Google Search Contributions - Thumbs')
        report.start_artifact_report(report_folder, 'Google Search Contributions - Thumbs', description)
        report.add_script()
        data_headers = ('Published Timestamp', 'Updated Timestamp', 'Search Query', 'Thumbs Rating')
        report.write_artifact_data_table(data_headers, thumbs, files_found[0])
        report.end_artifact_report()
        
        tsvname = 'Google Search Contributions - Thumbs'
        tsv(report_folder, data_headers, thumbs, tsvname)
        
        tlactivity = 'Google Search Contributions - Thumbs'
        timeline(report_folder, tlactivity, thumbs, data_headers)
    else:
        logfunc('No Google Search Contributions - Thumbs data available')

__artifacts_v2__ = {
    "takeoutSearchContributions": {
        "name": "Google Search Contributions",
        "description": "Parses Google Search Contributions from Takeout for reviews, watched content, streaming providers, and thumb ratings.",
        "author": "Gemini",
        "version": "1.0",
        "date": "2025-07-21",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": ('*/Search Contributions/*.json',),
        "function": "get_takeoutSearchContributions"
    }
}
import os
import datetime
import json
import magic
import shutil
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows, media_to_html

def get_instagramPosts(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('posts_1.json'):
            data_list =[]
            with open(file_found, "rb") as fp:
                deserialized = json.load(fp)
                
            for x in deserialized:
                timestamp = title = uri = latitude = longitude = deviceid = sourcetype = scenecapturetype = software = datatimeexif = ''
                for a, b in x.items():
                    if a == 'media':
                        for y in b:
                            #print(y)
                            
                            for c, d in y.items():
                                if c == 'media_metadata':
                                    #print(c, d)
                                    
                                    for f, g in d.items():
                                        metadata_type = (f) #string video_metadata o photo_metadata
                                        deviceid = (g['exif_data'][0].get('device_id', ''))
                                        sourcetype = (g['exif_data'][0].get('source_type', ''))
                                        scenecapturetype = (g['exif_data'][0].get('scene_capture_type', ''))
                                        software = (g['exif_data'][0].get('software', ''))
                                        datatimeexif =(g['exif_data'][0].get('date_time_original', ''))
                                        latitude = (g['exif_data'][0].get('latitude', ''))
                                        longitude = (g['exif_data'][0].get('longitude', ''))
                                if c == 'title':
                                    title = d
                                if c == 'uri':
                                    uri = d
                                    thumb = media_to_html(uri, files_found, report_folder)
                                    
                                if c == 'creation_timestamp':
                                    if d > 0:
                                        timestamp = (datetime.datetime.fromtimestamp(int(d)).strftime('%Y-%m-%d %H:%M:%S'))
                                        
                            data_list.append((timestamp, title, thumb, uri, latitude, longitude, deviceid, sourcetype, scenecapturetype, software, datatimeexif))
                    
                
            if data_list:
                report = ArtifactHtmlReport('Instagram Archive - Posts')
                report.start_artifact_report(report_folder, 'Instagram Archive - Posts')
                report.add_script()
                data_headers = ('Timestamp', 'Title', 'Content', 'URI', 'Latitude', 'Longitude', 'Device ID', 'Source Type', 'Scene Capture type', 'Software', 'Date Time EXIF')
                report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Content'])
                report.end_artifact_report()
                
                tsvname = f'Instagram Archive - Posts'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                tlactivity = f'Instagram Archive - Posts'
                timeline(report_folder, tlactivity, data_list, data_headers)
                
                kmlactivity = 'Instagram Archive - Posts'
                kmlgen(report_folder, kmlactivity, data_list, data_headers)
            else:
                logfunc('No Instagram Archive - Posts data available')
                
        
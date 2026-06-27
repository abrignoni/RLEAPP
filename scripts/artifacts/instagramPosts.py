__artifacts_v2__ = {
    "instagramPosts": {
        "name": "Instagram Archive - Posts",
        "description": "Parses posts, post media, and EXIF/GPS metadata from an Instagram data archive (posts_1.json)",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-21",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Instagram Archive",
        "notes": "",
        "paths": ('*/content/posts_1.json', '*/media/*'),
        "output_types": ['html', 'tsv', 'timeline', 'lava', 'kml'],
        "artifact_icon": "instagram",
    }
}

import os
import json

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc, check_in_media


@artifact_processor
def instagramPosts(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found).startswith('posts_1.json'):
            source_path = file_found
            with open(file_found, 'r', encoding='utf-8') as fp:
                deserialized = json.load(fp)

            for post in deserialized:
                for media_item in post.get('media', []):
                    title = media_item.get('title', '')
                    uri = media_item.get('uri', '')
                    timestamp = media_item.get('creation_timestamp', '')
                    timestamp = convert_unix_ts_to_utc(timestamp) if timestamp else ''
                    media_ref = check_in_media(uri, title) if uri else None

                    deviceid = sourcetype = scenecapturetype = ''
                    software = datetimeexif = latitude = longitude = ''
                    metadata = media_item.get('media_metadata') or {}
                    for meta in metadata.values():
                        exif_list = meta.get('exif_data') or []
                        if exif_list:
                            exif = exif_list[0]
                            deviceid = exif.get('device_id', '')
                            sourcetype = exif.get('source_type', '')
                            scenecapturetype = exif.get('scene_capture_type', '')
                            software = exif.get('software', '')
                            datetimeexif = exif.get('date_time_original', '')
                            latitude = exif.get('latitude', '')
                            longitude = exif.get('longitude', '')

                    data_list.append((timestamp, title, media_ref, uri, latitude, longitude,
                                      deviceid, sourcetype, scenecapturetype, software, datetimeexif))

    data_headers = (('Timestamp', 'datetime'), 'Title', ('Content', 'media'), 'URI',
                    'Latitude', 'Longitude', 'Device ID', 'Source Type',
                    'Scene Capture type', 'Software', 'Date Time EXIF')
    return data_headers, data_list, context.get_relative_path(source_path)

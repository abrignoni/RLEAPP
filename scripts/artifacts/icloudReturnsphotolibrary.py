__artifacts_v2__ = {
    "icloudReturnsphotolibrary": {
        "name": "iCloud Returns - Photo Library",
        "description": "Photo library (Metadata.txt) from an iCloud law enforcement return, with media, EXIF and GPS.",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-09-16",
        "last_update_date": "2026-06-28",
        "requirements": "Pillow, pillow-heif",
        "category": "iCloud Returns",
        "notes": "",
        "paths": ('*/*/cloudphotolibrary/*',),
        "output_types": ['html', 'tsv', 'timeline', 'lava', 'kml'],
        "html_columns": ["Exif"],
        "artifact_icon": "photo",
    }
}

import base64
import io
import json
import os

from PIL import Image
from pillow_heif import register_heif_opener

from scripts.ilapfuncs import (artifact_processor, check_in_media, check_in_embedded_media,
                               convert_unix_ts_to_utc)
from scripts.html_safe import esc

_EXIF_TAGS = {271: 'Manufacturer', 272: 'Model', 305: 'Software', 274: 'Orientation',
              306: 'Creation/Changed', 282: 'Resolution X', 283: 'Resolution Y', 316: 'Host device'}
_GPS_KEYS = ['GPSVersionID', 'GPSLatitudeRef', 'GPSLatitude', 'GPSLongitudeRef', 'GPSLongitude',
             'GPSAltitudeRef', 'GPSAltitude', 'GPSTimeStamp', 'GPSSatellites', 'GPSStatus',
             'GPSMeasureMode', 'GPSDOP', 'GPSSpeedRef', 'GPSSpeed', 'GPSTrackRef', 'GPSTrack',
             'GPSImgDirectionRef', 'GPSImgDirection', 'GPSMapDatum', 'GPSDestLatitudeRef',
             'GPSDestLatitude', 'GPSDestLongitudeRef', 'GPSDestLongitude', 'GPSDestBearingRef',
             'GPSDestBearing', 'GPSDestDistanceRef', 'GPSDestDistance', 'GPSProcessingMethod',
             'GPSAreaInformation', 'GPSDateStamp', 'GPSDifferential']


def _geotagging(gps_ifd):
    info = {}
    for k, v in (gps_ifd or {}).items():
        try:
            info[_GPS_KEYS[k]] = str(v)
        except IndexError:
            pass
    return info


def _gps_decimal(info):
    try:
        def dms(ref_key, val_key):
            ref = info[ref_key]
            parts = info[val_key].replace('(', '').replace(')', '').split(', ')
            dec = float(parts[0]) + float(parts[1]) / 60 + float(parts[2]) / 3600
            return dec * (-1 if ref in ('W', 'S') else 1)
        return dms('GPSLatitudeRef', 'GPSLatitude'), dms('GPSLongitudeRef', 'GPSLongitude')
    except (KeyError, IndexError, ValueError):
        return '', ''


def _exif_summary(image_path):
    """Return (lat, lon, exif_html) for an image, or ('', '', '') on failure."""
    try:
        exif = Image.open(image_path).getexif()
    except Exception:  # pylint: disable=broad-except
        return '', '', ''
    lat, lon = _gps_decimal(_geotagging(exif.get_ifd(0x8825)))
    summary = ''.join(f'{esc(_EXIF_TAGS.get(tag, tag))}: {esc(value)}<br>' for tag, value in exif.items())
    return lat, lon, summary


@artifact_processor
def icloudReturnsphotolibrary(context):
    register_heif_opener()
    media_lookup = {os.path.basename(str(f)): str(f) for f in context.get_files_found()}

    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found) != 'Metadata.txt':
            continue
        source_path = file_found
        with open(file_found, 'rb') as fp:
            data = json.load(fp)

        for record in data:
            fields = record.get('fields')
            if not fields:
                continue
            filename_enc = fields.get('filenameEnc')
            if isinstance(filename_enc, dict):
                filename_enc = filename_enc.get('value')
            if not filename_enc:
                continue
            try:
                filename = base64.b64decode(filename_enc).decode('ascii')
            except (ValueError, UnicodeDecodeError):
                continue
            if filename.endswith('txt'):
                continue

            creation = fields.get('originalCreationDate')
            if isinstance(creation, dict):
                creation = creation.get('value')
            timestamp = convert_unix_ts_to_utc(creation) if creation else ''
            is_deleted = fields.get('isDeleted')
            is_expunged = fields.get('isExpunged')

            latitude = longitude = exifdata = ''
            media_path = media_lookup.get(filename)
            if filename.upper().endswith('HEIC') and media_path:
                try:
                    buf = io.BytesIO()
                    Image.open(media_path).convert('RGB').save(buf, format='JPEG')
                    media_ref = check_in_embedded_media(media_path, buf.getvalue(), f'{filename}.jpg')
                except Exception:  # pylint: disable=broad-except
                    media_ref = check_in_media(filename, filename)
                latitude, longitude, exifdata = _exif_summary(media_path)
            else:
                media_ref = check_in_media(filename, filename)

            data_list.append((timestamp, media_ref, filename, latitude, longitude, exifdata,
                              filename_enc, is_deleted, is_expunged))

    data_headers = (('Timestamp', 'datetime'), ('Media', 'media'), 'Filename', 'Latitude',
                    'Longitude', 'Exif', 'Filename base64', 'Is Deleted', 'Is Expunged')
    return data_headers, data_list, context.get_relative_path(source_path)

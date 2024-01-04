import os
import datetime
import json
import shutil
import base64
from PIL import Image
from pillow_heif import register_heif_opener

from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows, media_to_html

def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image.getexif().get_ifd(0x8825)

def get_geotagging(exif):
    geo_tagging_info = {}
    if not exif:
        #raise ValueError("No EXIF metadata found")
        return None
    else:
        gps_keys = ['GPSVersionID', 'GPSLatitudeRef', 'GPSLatitude', 'GPSLongitudeRef', 'GPSLongitude',
                    'GPSAltitudeRef', 'GPSAltitude', 'GPSTimeStamp', 'GPSSatellites', 'GPSStatus', 'GPSMeasureMode',
                    'GPSDOP', 'GPSSpeedRef', 'GPSSpeed', 'GPSTrackRef', 'GPSTrack', 'GPSImgDirectionRef',
                    'GPSImgDirection', 'GPSMapDatum', 'GPSDestLatitudeRef', 'GPSDestLatitude', 'GPSDestLongitudeRef',
                    'GPSDestLongitude', 'GPSDestBearingRef', 'GPSDestBearing', 'GPSDestDistanceRef', 'GPSDestDistance',
                    'GPSProcessingMethod', 'GPSAreaInformation', 'GPSDateStamp', 'GPSDifferential']
        
        for k, v in exif.items():
            try:
                geo_tagging_info[gps_keys[k]] = str(v)
            except IndexError:
                pass
        return geo_tagging_info
    
def get_all_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image.getexif()

def get_icloudReturnsphotolibrary(files_found, report_folder, seeker, wrap_text, time_offset):
    
    for file_found in files_found:
        file_found = str(file_found)
        
        if is_platform_windows():
            separator = '\\'
        else:
            separator = '/'
            
        split_path = file_found.split(separator)
        account = (split_path[-3])
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('Metadata.txt'):
            #print(file_found)
            data_list =[]
            with open(file_found, "rb") as fp:
                data = json.load(fp)
            
            for deserialized in data:
                isfields = deserialized.get('fields','Negative')
                if isfields == 'Negative':
                    continue
                else:
                    filenameEnc = deserialized['fields'].get('filenameEnc','Negative')
                    isdeleted = deserialized['fields'].get('isDeleted')
                    isexpunged = deserialized['fields'].get('isExpunged')
                    originalcreationdate = deserialized['fields'].get('originalCreationDate')
            
                    
                    if (filenameEnc != 'Negative') and (filenameEnc is not None):
                        if isinstance(filenameEnc, dict):
                            filenameEnc = filenameEnc['value']
                        
                        filenamedec = (base64.b64decode(filenameEnc).decode('ascii'))
                        
                        if isinstance(originalcreationdate, dict):
                            originalcreationdate = originalcreationdate['value']
                            
                        originalcreationdatedec = (datetime.datetime.fromtimestamp(int(originalcreationdate)/1000).strftime('%Y-%m-%d %H:%M:%S'))
                        
                        if filenamedec.endswith('HEIC'):
                            register_heif_opener()
                            
                            for search in files_found:
                                searchbase = os.path.basename(search)
                                if filenamedec == searchbase:
                                    image = Image.open(search)
                                    convertedfilepath = os.path.join(report_folder, f'{filenamedec}.jpg')
                                    image.save(convertedfilepath)
                                    convertedlist = []
                                    convertedlist.append(convertedfilepath)
                                    thumb = media_to_html(f'{filenamedec}.jpg', convertedlist, report_folder)
                                    convertedlist = []
                                    
                                    image_info = get_exif(search)
                                    results = get_geotagging(image_info)
                                    
                                    if results is None:
                                        latitude = ''
                                        longitude = ''
                                    else:
                                        directionlat = results['GPSLatitudeRef']
                                        latitude = results['GPSLatitude']
                                        latitude = (latitude.replace('(','').replace(')','').split(', '))
                                        latitude = (float(latitude[0]) + float(latitude[1])/60 + float(latitude[2])/(60*60)) * (-1 if directionlat in ['W', 'S'] else 1)
                                        
                                        
                                        directionlon = results['GPSLongitudeRef']
                                        longitude = results['GPSLongitude']
                                        longitude = (longitude.replace('(','').replace(')','').split(', '))
                                        longitude = (float(longitude[0]) + float(longitude[1])/60 + float(longitude[2])/(60*60)) * (-1 if directionlon in ['W', 'S'] else 1)
                                        
                                        #datamap = []
                                        #datamap.append((originalcreationdate,latitude,longitude))
                                        #kmlactivity = f'{search}'
                                        #data_headers = ('Timestamp','Latitude','Longitude')
                                        #print(report_folder)
                                        #kmlgen(report_folder, kmlactivity, datamap, data_headers)
                                        
                                    exifall = get_all_exif(search)
                                    exifdata = ''
                                    
                                    for x, y in exifall.items():
                                        if x == 271:
                                            exifdata = exifdata + f'Manufacturer: {y}<br>'
                                        elif x == 272:
                                            exifdata = exifdata + f'Model: {y}<br>'
                                        elif x == 305:
                                            exifdata = exifdata + f'Software: {y}<br>'
                                        elif x == 274:
                                            exifdata = exifdata + f'Orientation: {y}<br>'
                                        elif x == 306:
                                            exifdata = exifdata + f'Creation/Changed: {y}<br>'
                                        elif x == 282:
                                            exifdata = exifdata + f'Resolution X: {y}<br>'
                                        elif x == 283:
                                            exifdata = exifdata + f'Resolution Y: {y}<br>'
                                        elif x == 316:
                                            exifdata = exifdata + f'Host device: {y}<br>'
                                        else:
                                            exifdata = exifdata + f'{x}: {y}<br>'
                            
                            data_list.append((originalcreationdatedec, thumb, filenamedec, latitude, longitude, exifdata, filenameEnc, isdeleted, isexpunged))
                        elif filenamedec.endswith('txt'):
                            pass
                        else:
                            #print(filenamedec)
                            thumb = media_to_html(filenamedec, files_found, report_folder)
                            latitude = ''
                            longitude = ''
                            exifdata = ''
                            
                            data_list.append((originalcreationdatedec, thumb, filenamedec, latitude, longitude, exifdata, filenameEnc, isdeleted, isexpunged))
                    
                
            if data_list:
                report = ArtifactHtmlReport(f'iCloud Returns - Photo Library - {account}')
                report.start_artifact_report(report_folder, f'iCloud Returns - Photo Library - {account}')
                report.add_script()
                data_headers = ('Timestamp','Media','Filename','Latitude','Longitude','Exif','Filename base64','Is Deleted','Is Expunged')
                report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Media','Exif'])
                report.end_artifact_report()
                
                tsvname = f'iCloud Returns - Photo Library - {account}'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                tlactivity = f'iCloud Returns - Photo Library - {account}'
                timeline(report_folder, tlactivity, data_list, data_headers)
                
                kmlactivity = f'iCloud Returns - Photo Library - {account}'
                kmlgen(report_folder, kmlactivity, data_list, data_headers)
                
            else:
                logfunc(f'No iCloud Returns - Photo Library - {account} data available')
                
__artifacts__ = {
        "icloudReturnsphotolibrary": (
            "iCloud Returns",
            ('*/*/cloudphotolibrary/*'),
            get_icloudReturnsphotolibrary)
}
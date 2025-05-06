# common standard imports
import codecs
import csv
import hashlib
import json
import os
import re
import shutil
import sqlite3
import sys

from datetime import *
from functools import lru_cache
from pathlib import Path
from urllib.parse import quote
import scripts.artifact_report as artifact_report

# common third party imports
import pytz
import simplekml
from bs4 import BeautifulSoup
from scripts.filetype import guess_mime, guess_extension
from functools import wraps

# LEAPP version unique imports
from typing import Pattern
from scripts.lavafuncs import lava_process_artifact, lava_insert_sqlite_data, lava_get_media_item, \
    lava_insert_sqlite_media_item, lava_insert_sqlite_media_references, lava_get_media_references, \
    lava_get_full_media_info

os.path.basename = lru_cache(maxsize=None)(os.path.basename)

icons = {}

class OutputParameters:
    '''Defines the parameters that are common for '''
    # static parameters
    nl = '\n'
    screen_output_file_path = ''

    def __init__(self, output_folder, custom_folder_name=None):
        now = datetime.now()
        currenttime = str(now.strftime('%Y-%m-%d_%A_%H%M%S'))
        if custom_folder_name:
            folder_name = custom_folder_name
        else:
            folder_name = 'RLEAPP_Reports_' + currenttime
        self.report_folder_base = os.path.join(output_folder, folder_name)
        self.data_folder = os.path.join(self.report_folder_base, 'data')
        OutputParameters.screen_output_file_path = os.path.join(
            self.report_folder_base, 'Script Logs', 'Screen Output.html')

        os.makedirs(os.path.join(self.report_folder_base, 'Script Logs'))
        os.makedirs(self.data_folder)
        
class GuiWindow:
    '''This only exists to hold window handle if script is run from GUI'''
    window_handle = None  # static variable

    @staticmethod
    def SetProgressBar(n, total):
        if GuiWindow.window_handle:
            progress_bar = GuiWindow.window_handle.nametowidget('!progressbar')
            progress_bar.config(value=n)

class MediaItem():
    def __init__(self, id):
        self.id = id
        self.source_path = ""
        self.extraction_path = ""
        self.mimetype = ""
        self.metadata = ""
        self.created_at = 0
        self.updated_at = 0
    
    def set_values(self, media_info):
        self.id = media_info[0]
        self.source_path = media_info[1]
        self.extraction_path = media_info[2]
        self.mimetype = media_info[3]
        self.metadata = media_info[4]
        self.created_at = media_info[5]
        self.updated_at = media_info[6]

class MediaReferences():
    def __init__(self, id):
        self.id = id
        self.media_item_id = ""
        self.module_name = ""
        self.artifact_name = ""
        self.name = ""
    
    def set_values(self, media_ref_info):
        self.id = media_ref_info[0]
        self.media_item_id = media_ref_info[1]
        self.module_name = media_ref_info[2]
        self.artifact_name = media_ref_info[3]
        self.name = media_ref_info[4]


def logfunc(message=""):
    def redirect_logs(string):
        log_text.insert('end', string)
        log_text.see('end')
        log_text.update()

    if GuiWindow.window_handle:
        log_text = GuiWindow.window_handle.nametowidget('logs_frame.log_text')
        sys.stdout.write = redirect_logs

    with open(OutputParameters.screen_output_file_path, 'a', encoding='utf8') as a:
        print(message)
        a.write(message + '<br>' + OutputParameters.nl)


def strip_tuple_from_headers(data_headers):
    return [header[0] if isinstance(header, tuple) else header for header in data_headers]

def get_media_header_position(data_headers):
    return [i for i, header in enumerate(data_headers) if isinstance(header, tuple) and header[1] == 'media']

def check_output_types(type, output_types):
    if type in output_types or type == output_types or 'all' in output_types or 'all' == output_types:
        return True
    elif type != 'kml' and ('standard' in output_types or 'standard' == output_types):
        return True
    else:
        return False

def get_media_references_id(media_id, artifact_info, name):
    artifact_name = artifact_info.function
    return hashlib.sha1(f"{media_id}-{artifact_name}-{name}".encode()).hexdigest()

def set_media_references(media_ref_id, media_id, artifact_info, name):
    module_name = Path(artifact_info.filename).stem
    artifact_name = artifact_info.function
    media_references = MediaReferences(media_ref_id)
    media_references.set_values((
        media_ref_id, media_id, module_name, artifact_name, name
    ))
    lava_insert_sqlite_media_references(media_references)

def check_in_media(seeker, file_path, artifact_info, name="", already_extracted=False, converted_file_path=False):
    if already_extracted:
        file_info_key = file_path
    else:
        file_info_key = seeker.search(file_path, return_on_first_hit=True)
    file_info = seeker.file_infos.get(file_info_key) if file_info_key else None
    if file_info:
        if converted_file_path:
            extraction_path = Path(converted_file_path)
        else:
            extraction_path = Path(file_info_key)
        if extraction_path.is_file():
            media_id = hashlib.sha1(f"{extraction_path}".encode()).hexdigest()
            lava_media_item = lava_get_media_item(media_id)
            if lava_media_item:
                return media_id
            else:
                media_item = MediaItem(media_id)
                media_item.source_path = file_info.source_path
                media_item.extraction_path = extraction_path
                media_item.mimetype = guess_mime(extraction_path)
                media_item.metadata = "not implemented yet"
                media_item.created_at = file_info.creation_date
                media_item.updated_at = file_info.modification_date
                lava_insert_sqlite_media_item(media_item)
                media_ref_id = get_media_references_id(media_id, artifact_info, name)
                set_media_references(media_ref_id, media_id, artifact_info, name)
            return media_id
        else:
            logfunc(f"{extraction_path} was not found")
            return None            
    else:
        logfunc(f'No matching file found for "{file_path}"')
        return None

def check_in_embedded_media(seeker, source_file, data, artifact_info, name="", media_updated_at=0):
    file_info = seeker.file_infos.get(source_file)
    if data and file_info:
        media_id = hashlib.sha1(data).hexdigest()
        media_ref_id = get_media_references_id(media_id, artifact_info, name)
        lava_media_ref = lava_get_media_references(media_ref_id)
        if lava_media_ref:
            return media_ref_id
        lava_media_item = lava_get_media_item(media_id)
        if not lava_media_item:
            media_item = MediaItem(media_id)
            media_item.mimetype = guess_mime(data)
            media_item.source_path = file_info.source_path
            media_item.metadata = "not implemented yet"
            media_item.created_at = 0
            media_item.updated_at = 0
            target_folder_name = f"{Path(source_file).stem}_embedded_media"
            target_path = Path(source_file).parent.joinpath(target_folder_name)
            media_extension = guess_extension(data)
            media_item.extraction_path = Path(target_path).joinpath(f"{media_id}.{media_extension}")
            try:
                target_path.mkdir(parents=True, exist_ok=True)
                with open(media_item.extraction_path, "wb") as file:
                    file.write(data)
            except Exception as ex:
                logfunc(f'Could not copy embedded media into {target_path} ' + str(ex))
            lava_insert_sqlite_media_item(media_item)
        set_media_references(media_ref_id, media_id, artifact_info, name)
        return media_ref_id
    else:
        return None

def html_media_tag(media_path, mimetype, style, title=''):
    def relative_paths(source):
        splitter = '\\' if is_platform_windows() else '/'
        first_split = source.split(splitter)
        for x in first_split:
            if 'data' in x:
                index = first_split.index(x)
                last_split = source.split(first_split[index - 1])
                return '..' + last_split[1].replace('\\', '/')
            elif '_HTML' in x:
                index = first_split.index(x)
                last_split = source.split(first_split[index])
                return '.' + last_split[1].replace('\\', '/')
        return source

    filename = Path(media_path).name
    media_path = quote(relative_paths(media_path))

    if mimetype == None:
        mimetype = ''
    if 'video' in mimetype:
        thumb = f'<video width="320" height="240" controls="controls"><source src="{media_path}" type="video/mp4" preload="none">Your browser does not support the video tag.</video>'
    elif 'image' in mimetype:
        image_style = style if style else "max-height:300px; max-width:400px;"
        thumb = f'<a href="{media_path}" target="_blank"><img title="{title}"  src="{media_path}" style="{image_style}"></img></a>'
    elif 'audio' in mimetype:
        thumb = f'<audio controls><source src="{media_path}" type="audio/ogg"><source src="{media_path}" type="audio/mpeg">Your browser does not support the audio element.</audio>'
    else:
        thumb = f'<a href="{media_path}" target="_blank"> Link to {filename} file</>'
    return thumb

def get_data_list_with_media(media_header_idx, data_list, media_style):
    ''' 
    For columns with media item:
      - Generate a new data list with HTML code
      - Remove them in a new data list for TSV, KML and Timeline exports  
    '''
    html_data_list = []
    txt_data_list = []
    for data in data_list:
        html_data = list(data)
        media_style_idx = 0
        for idx in media_header_idx:
            if html_data[idx]:
                try:
                    style = media_style[media_style_idx] if isinstance(media_style, tuple) else media_style
                except:
                    style = media_style
                media_ref_id = html_data[idx]
                html_code = ''
                if isinstance(media_ref_id, list):
                    for item in media_ref_id:
                        media_item = lava_get_full_media_info(item)
                        html_code += html_media_tag(media_item[6], media_item[7], style, media_item[4])
                else:
                    media_item = lava_get_full_media_info(media_ref_id)
                    html_code = html_media_tag(media_item[6], media_item[7], style, media_item[4])
                html_data[idx] = html_code
            else:
                html_data[idx] = ''
            media_style_idx += 1
        html_data_list.append(tuple(html_data))
        txt_data = [i for media_idx, i in enumerate(data) if media_idx not in media_header_idx]
        txt_data_list.append(tuple(txt_data))
    return html_data_list, txt_data_list

def artifact_processor(func):
    @wraps(func)
    def wrapper(files_found, report_folder, seeker, wrap_text):
        module_name = func.__module__.split('.')[-1]
        func_name = func.__name__

        func_object = func.__globals__.get(func_name, {})
        artifact_info = func_object.artifact_info #get('artifact_info', {})

        artifact_name = artifact_info.get('name', func_name)
        category = artifact_info.get('category', '')
        description = artifact_info.get('description', '')
        icon = artifact_info.get('artifact_icon', '')
        html_columns = artifact_info.get('html_columns', [])
        media_style = artifact_info.get('media_style', '')

        output_types = artifact_info.get('output_types', ['html', 'tsv', 'timeline', 'lava', 'kml'])

        data_headers, data_list, source_path = func(files_found, report_folder, seeker, wrap_text)
        
        if not source_path:
            logfunc(f"No file found")

        elif len(data_list):
            if isinstance(data_list, tuple):
                data_list, html_data_list = data_list
            else:
                html_data_list = data_list
            logfunc(f"Found {len(data_list)} {'records' if len(data_list)>1 else 'record'} for {artifact_name}")
            icons.setdefault(category, {artifact_name: icon}).update({artifact_name: icon})

            # Strip tuples from headers for HTML, TSV, and timeline
            stripped_headers = strip_tuple_from_headers(data_headers)

            # Check if headers contains a 'media' type
            media_header_idx = get_media_header_position(data_headers)
            if media_header_idx:
                html_columns.extend([data_headers[idx][0] for idx in media_header_idx])
                html_data_list, txt_data_list = get_data_list_with_media(media_header_idx, data_list, media_style)

            txt_headers = [i for media_idx, i in enumerate(stripped_headers) if media_idx not in media_header_idx] if media_header_idx else stripped_headers

            if check_output_types('html', output_types):
                report = artifact_report.ArtifactHtmlReport(artifact_name)
                report.start_artifact_report(report_folder, artifact_name, description)
                report.add_script()
                report.write_artifact_data_table(stripped_headers, html_data_list, source_path, html_no_escape=html_columns)
                report.end_artifact_report()

            if check_output_types('tsv', output_types):
                tsv(report_folder, txt_headers, txt_data_list if media_header_idx else data_list, artifact_name)
            
            if check_output_types('timeline', output_types):
                timeline(report_folder, artifact_name, txt_data_list if media_header_idx else data_list, txt_headers)

            if check_output_types('lava', output_types):
                table_name, object_columns, column_map = lava_process_artifact(category, module_name, artifact_name, data_headers, len(data_list), data_views=artifact_info.get("data_views"))
                lava_insert_sqlite_data(table_name, data_list, object_columns, data_headers, column_map)

            if check_output_types('kml', output_types):
                kmlgen(report_folder, artifact_name, txt_data_list if media_header_idx else data_list, txt_headers)

        else:
            if output_types != 'none':
                logfunc(f"No {artifact_name} data available")
        
        return data_headers, data_list, source_path
    return wrapper


def is_platform_linux():
    '''Returns True if running on Linux'''
    return sys.platform == 'linux'

def is_platform_macos():
    '''Returns True if running on macOS'''
    return sys.platform == 'darwin'

def is_platform_windows():
    '''Returns True if running on Windows'''
    return sys.platform == 'win32'

def sanitize_file_path(filename, replacement_char='_'):
    r'''
    Removes illegal characters (for windows) from the string passed. Does not replace \ or /
    '''
    return re.sub(r'[*?:"<>|\'\r\n]', replacement_char, filename)

def sanitize_file_name(filename, replacement_char='_'):
    '''
    Removes illegal characters (for windows) from the string passed.
    '''
    return re.sub(r'[\\/*?:"<>|\'\r\n]', replacement_char, filename)

def get_next_unused_name(path):
    '''Checks if path exists, if it does, finds an unused name by appending -xx
       where xx=00-99. Return value is new path.
       If it is a file like abc.txt, then abc-01.txt will be the next
    '''
    folder, basename = os.path.split(path)
    ext = None
    if basename.find('.') > 0:
        basename, ext = os.path.splitext(basename)
    num = 1
    new_name = basename
    if ext != None:
        new_name += f"{ext}"
    while os.path.exists(os.path.join(folder, new_name)):
        new_name = basename + "-{:02}".format(num)
        if ext != None:
            new_name += f"{ext}"
        num += 1
    return os.path.join(folder, new_name)


def get_file_path(files_found, filename, skip=False):
    """Returns the path of the searched filename if exists or returns None"""
    try:
        for file_found in files_found:
            if skip:
                if skip in file_found:
                    continue
            if file_found.endswith(filename):
                return file_found
    except Exception as e:
        logfunc(f"Error: {str(e)}")
    return None        

def get_txt_file_content(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.readlines()
            return file_content
    except FileNotFoundError:
        logfunc(f"Error: File not found at {file_path}")
    except PermissionError:
        logfunc(f"Error: Permission denied when trying to read {file_path}")
    except Exception as e:
        logfunc(f"Unexpected error reading file {file_path}: {str(e)}")
    return []

def get_sqlite_db_path(path):
    if is_platform_windows():
        if str(path).startswith('\\\\?\\UNC\\'): # UNC long path
            return "%5C%5C%3F%5C" + path[4:]
        elif str(path).startswith('\\\\?\\'):    # normal long path
            return "%5C%5C%3F%5C" + path[4:]
        elif str(path).startswith('\\\\'):       # UNC path
            return "%5C%5C%3F%5C\\UNC" + path[1:]
        else:                               # normal path
            return "%5C%5C%3F%5C" + path
    else:
        return path

def open_sqlite_db_readonly(path):
    '''Opens a sqlite db in read-only mode, so original db (and -wal/journal are intact)'''
    try:
        if path:
            path = get_sqlite_db_path(path)
            with sqlite3.connect(f"file:{path}?mode=ro", uri=True) as db:
                return db
    except sqlite3.OperationalError as e:
        logfunc(f"Error with {path}:")
        logfunc(f" - {str(e)}")
    return None

def attach_sqlite_db_readonly(path, db_name):
    '''Return the query to attach a sqlite db in read-only mode.
    path: str --> Path of the SQLite DB to attach
    db_name: str --> Name of the SQLite DB in the query'''
    path = get_sqlite_db_path(path)
    return  f'''ATTACH DATABASE "file:{path}?mode=ro" AS {db_name}'''

def get_sqlite_db_records(path, query, attach_query=None):
    db = open_sqlite_db_readonly(path)
    if db:
        try:
            cursor = db.cursor()
            if attach_query:
                cursor.execute(attach_query)
            cursor.execute(query)
            records = cursor.fetchall()
            return records
        except sqlite3.OperationalError as e:
            logfunc(f"Error with {path}:")
            logfunc(f" - {str(e)}")
        except sqlite3.ProgrammingError as e:
            logfunc(f"Error with {path}:")
            logfunc(f" - {str(e)}")
    return []

def does_column_exist_in_db(path, table_name, col_name):
    '''Checks if a specific col exists'''
    db = open_sqlite_db_readonly(path)
    col_name = col_name.lower()
    try:
        db.row_factory = sqlite3.Row # For fetching columns by name
        query = f"pragma table_info('{table_name}');"
        cursor = db.cursor()
        cursor.execute(query)
        all_rows = cursor.fetchall()
        for row in all_rows:
            if row['name'].lower() == col_name:
                return True
    except sqlite3.Error as ex:
        logfunc(f"Query error, query={query} Error={str(ex)}")
        pass
    return False

def does_table_exist_in_db(path, table_name):
    '''Checks if a table with specified name exists in an sqlite db'''
    db = open_sqlite_db_readonly(path)
    if db:    
        try:
            query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
            cursor = db.execute(query)
            for row in cursor:
                return True
        except sqlite3.Error as ex:
            logfunc(f"Query error, query={query} Error={str(ex)}")
    return False

def does_view_exist(path, table_name):
    '''Checks if a table with specified name exists in an sqlite db'''
    db = open_sqlite_db_readonly(path)
    if db:
        try:
            query = f"SELECT name FROM sqlite_master WHERE type='view' AND name='{table_name}'"
            cursor = db.execute(query)
            for row in cursor:
                return True
        except sqlite3.Error as ex:
            logfunc(f"Query error, query={query} Error={str(ex)}")
    return False


def tsv(report_folder, data_headers, data_list, tsvname, source_file=None):
    report_folder = report_folder.rstrip('/')
    report_folder = report_folder.rstrip('\\')
    report_folder_base = os.path.dirname(os.path.dirname(report_folder))
    tsv_report_folder = os.path.join(report_folder_base, '_TSV Exports')

    if os.path.isdir(tsv_report_folder):
        pass
    else:
        os.makedirs(tsv_report_folder)
    
    with codecs.open(os.path.join(tsv_report_folder, tsvname + '.tsv'), 'a', 'utf-8-sig') as tsvfile:
        tsv_writer = csv.writer(tsvfile, delimiter='\t')
        tsv_writer.writerow(data_headers)
        
        for i in data_list:
            tsv_writer.writerow(i)
            
def timeline(report_folder, tlactivity, data_list, data_headers):
    report_folder = report_folder.rstrip('/')
    report_folder = report_folder.rstrip('\\')
    report_folder_base = os.path.dirname(os.path.dirname(report_folder))
    tl_report_folder = os.path.join(report_folder_base, '_Timeline')

    if os.path.isdir(tl_report_folder):
        tldb = os.path.join(tl_report_folder, 'tl.db')
        db = sqlite3.connect(tldb)
        cursor = db.cursor()
        cursor.execute('''PRAGMA synchronous = EXTRA''')
        cursor.execute('''PRAGMA journal_mode = WAL''')
        db.commit()
    else:
        os.makedirs(tl_report_folder)
        # create database
        tldb = os.path.join(tl_report_folder, 'tl.db')
        db = sqlite3.connect(tldb, isolation_level = 'exclusive')
        cursor = db.cursor()
        cursor.execute(
            """
            CREATE TABLE data(key TEXT, activity TEXT, datalist TEXT)
            """
        )
        db.commit()
    
    for entry in data_list:
        entry = [str(field) for field in entry]
        
        data_dict = dict(zip(data_headers, entry))

        data_str = json.dumps(data_dict)
        cursor.executemany(
            "INSERT INTO data VALUES(?,?,?)", [(str(entry[0]), tlactivity, data_str)])

    db.commit()
    db.close()

def kmlgen(report_folder, kmlactivity, data_list, data_headers):
    if 'Longitude' not in data_headers or 'Latitude' not in data_headers:
        return

    data = []
    kml = simplekml.Kml(open=1)    
    a = 0
    length = len(data_list)
    while a < length:
        modifiedDict = dict(zip(data_headers, data_list[a]))
        lon = modifiedDict['Longitude']
        lat = modifiedDict['Latitude']
        times_header = "Timestamp"
        if lat and lon:
            pnt = kml.newpoint()
            times = modifiedDict.get('Timestamp','N/A')
            if times == 'N/A':
                for key, value in modifiedDict.items():
                    if isinstance(value, datetime):
                        times_header = key
                        times = value
                        break
            pnt.name = times
            pnt.description = f"{times_header}: {times} - {kmlactivity}"
            pnt.coords = [(lon, lat)]
            data.append((times, lat, lon, kmlactivity))
        a += 1

    if len(data) > 0:
        report_folder = report_folder.rstrip('/')
        report_folder = report_folder.rstrip('\\')
        report_folder_base = os.path.dirname(os.path.dirname(report_folder))
        kml_report_folder = os.path.join(report_folder_base, '_KML Exports')
        if os.path.isdir(kml_report_folder):
            latlongdb = os.path.join(kml_report_folder, '_latlong.db')
            db = sqlite3.connect(latlongdb)
            cursor = db.cursor()
            cursor.execute('''PRAGMA synchronous = EXTRA''')
            cursor.execute('''PRAGMA journal_mode = WAL''')
            db.commit()
        else:
            os.makedirs(kml_report_folder)
            latlongdb = os.path.join(kml_report_folder, '_latlong.db')
            db = sqlite3.connect(latlongdb)
            cursor = db.cursor()
            cursor.execute(
            """
            CREATE TABLE data(timestamp TEXT, latitude TEXT, longitude TEXT, activity TEXT)
            """
                )
            db.commit()
        
        cursor.executemany("INSERT INTO data VALUES(?, ?, ?, ?)", data)
        db.commit()
        db.close()
        kml.save(os.path.join(kml_report_folder, f'{kmlactivity}.kml'))

def media_to_html(media_path, files_found, report_folder):

    def media_path_filter(name):
        return media_path in name

    def relative_paths(source, splitter):
        splitted_a = source.split(splitter)
        for x in splitted_a:
            if '_HTML' in x:
                splitted_b = source.split(x)
                return '.' + splitted_b[1]
            elif 'data' in x:
                index = splitted_a.index(x)
                splitted_b = source.split(splitted_a[index - 1])
                return '..' + splitted_b[1]


    platform = is_platform_windows()
    if platform:
        media_path = media_path.replace('/', '\\')
        splitter = '\\'
    else:
        splitter = '/'

    thumb = media_path
    for match in filter(media_path_filter, files_found):
        filename = os.path.basename(match)
        if filename.startswith('~') or filename.startswith('._') or filename != media_path:
            continue

        dirs = os.path.dirname(report_folder)
        dirs = os.path.dirname(dirs)
        env_path = os.path.join(dirs, 'data')
        if env_path in match:
            source = match
            source = relative_paths(source, splitter)
        else:
            path = os.path.dirname(match)
            dirname = os.path.basename(path)
            filename = Path(match)
            filename = filename.name
            locationfiles = Path(report_folder).joinpath(dirname)
            Path(f'{locationfiles}').mkdir(parents=True, exist_ok=True)
            shutil.copy2(match, locationfiles)
            source = Path(locationfiles, filename)
            source = relative_paths(str(source), splitter)

        mimetype = guess_mime(match)
        if mimetype == None:
            mimetype = ''

        if 'video' in mimetype:
            thumb = f'<video width="320" height="240" controls="controls"><source src="{source}" type="video/mp4" preload="none">Your browser does not support the video tag.</video>'
        elif 'image' in mimetype:
            thumb = f'<a href="{source}" target="_blank"><img src="{source}"width="300"></img></a>'
        elif 'audio' in mimetype:
            thumb = f'<audio controls><source src="{source}" type="audio/ogg"><source src="{source}" type="audio/mpeg">Your browser does not support the audio element.</audio>'
        else:
            thumb = f'<a href="{source}" target="_blank"> Link to {filename} file</>'
    return thumb


"""
Copyright 2021, CCL Forensics
Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
def utf8_in_extended_ascii(input_string, *, raise_on_unexpected=False):
    """Returns a tuple of bool (whether mis-encoded utf-8 is present) and str (the converted string)"""
    output = []  # individual characters, join at the end
    is_in_multibyte = False  # True if we're currently inside a utf-8 multibyte character
    multibytes_expected = 0
    multibyte_buffer = []
    mis_encoded_utf8_present = False
    
    def handle_bad_data(index, character):
        if not raise_on_unexpected: # not raising, so we dump the buffer into output and append this character
            output.extend(multibyte_buffer)
            multibyte_buffer.clear()
            output.append(character)
            nonlocal is_in_multibyte
            is_in_multibyte = False
            nonlocal multibytes_expected
            multibytes_expected = 0
        else:
            raise ValueError(f"Expected multibyte continuation at index: {index}")
            
    for idx, c in enumerate(input_string):
        code_point = ord(c)
        if code_point <= 0x7f or code_point > 0xf4:  # ASCII Range data or higher than you get for mis-encoded utf-8:
            if not is_in_multibyte:
                output.append(c)  # not in a multibyte, valid ascii-range data, so we append
            else:
                handle_bad_data(idx, c)
        else:  # potentially utf-8
            if (code_point & 0xc0) == 0x80:  # continuation byte
                if is_in_multibyte:
                    multibyte_buffer.append(c)
                else:
                    handle_bad_data(idx, c)
            else:  # start-byte
                if not is_in_multibyte:
                    assert multibytes_expected == 0
                    assert len(multibyte_buffer) == 0
                    while (code_point & 0x80) != 0:
                        multibytes_expected += 1
                        code_point <<= 1
                    multibyte_buffer.append(c)
                    is_in_multibyte = True
                else:
                    handle_bad_data(idx, c)
                    
        if is_in_multibyte and len(multibyte_buffer) == multibytes_expected:  # output utf-8 character if complete
            utf_8_character = bytes(ord(x) for x in multibyte_buffer).decode("utf-8")
            output.append(utf_8_character)
            multibyte_buffer.clear()
            is_in_multibyte = False
            multibytes_expected = 0
            mis_encoded_utf8_present = True
        
    if multibyte_buffer:  # if we have left-over data
        handle_bad_data(len(input_string), "")
    
    return mis_encoded_utf8_present, "".join(output)

def html2csv(reportfolderbase):
    # List of items that take too long to convert or that shouldn't be converted
    itemstoignore = ['index.html',
                     'Distribution Keys.html',
                     'StrucMetadata.html',
                     'StrucMetadataCombined.html']

    if os.path.isdir(os.path.join(reportfolderbase, '_CSV Exports')):
        pass
    else:
        os.makedirs(os.path.join(reportfolderbase, '_CSV Exports'))
    for root, dirs, files in sorted(os.walk(reportfolderbase)):
        for file in files:
            if file.endswith(".html"):
                fullpath = (os.path.join(root, file))
                head, tail = os.path.split(fullpath)
                if file in itemstoignore:
                    pass
                else:
                    data = open(fullpath, 'r', encoding='utf8')
                    soup = BeautifulSoup(data, 'html.parser')
                    tables = soup.find_all("table")
                    data.close()
                    output_final_rows = []

                    for table in tables:
                        output_rows = []
                        for table_row in table.findAll('tr'):

                            columns = table_row.findAll('td')
                            output_row = []
                            for column in columns:
                                output_row.append(column.text)
                            output_rows.append(output_row)

                        file = (os.path.splitext(file)[0])
                        with codecs.open(os.path.join(reportfolderbase, '_CSV Exports', file + '.csv'), 'a',
                                         'utf-8-sig') as csvfile:
                            writer = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_ALL)
                            writer.writerows(output_rows)


def convert_utc_human_to_timezone(utc_time, time_offset): 
    #fetch the timezone information
    timezone = pytz.timezone(time_offset)
    
    #convert utc to timezone
    timezone_time = utc_time.astimezone(timezone)
    
    #return the converted value
    return timezone_time

def convert_ts_int_to_timezone(time, time_offset):
    #convert ts_int_to_utc_human
    utc_time = convert_ts_int_to_utc(time)

    #fetch the timezone information
    timezone = pytz.timezone(time_offset)
    
    #convert utc to timezone
    timezone_time = utc_time.astimezone(timezone)
    
    #return the converted value
    return timezone_time

def convert_ts_human_to_utc(ts): #This is for timestamp in human form
    if '.' in ts:
        ts = ts.split('.')[0]
        
    dt = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') #Make it a datetime object
    timestamp = dt.replace(tzinfo=datetime.UTC) #Make it UTC
    return timestamp

def convert_ts_int_to_utc(ts): #This int timestamp to human format & utc
    timestamp = datetime.fromtimestamp(ts, tz=datetime.UTC)
    return timestamp

def get_birthdate(date):
    ns_date = date + 978307200
    utc_date = datetime.utcfromtimestamp(ns_date)
    return utc_date.strftime('%d %B %Y') if utc_date.year != 1604 else utc_date.strftime('%d %B')


def usergen(report_folder, data_list_usernames):
    report_folder = report_folder.rstrip('/')
    report_folder = report_folder.rstrip('\\')
    report_folder_base = os.path.dirname(os.path.dirname(report_folder))
    udb_report_folder = os.path.join(report_folder_base, '_Usernames DB')

    if os.path.isdir(udb_report_folder):
        usernames = os.path.join(udb_report_folder, '_usernames.db')
        db = sqlite3.connect(usernames)
        cursor = db.cursor()
        cursor.execute('''PRAGMA synchronous = EXTRA''')
        cursor.execute('''PRAGMA journal_mode = WAL''')
        db.commit()
    else:
        os.makedirs(udb_report_folder)
        usernames = os.path.join(udb_report_folder, '_usernames.db')
        db = sqlite3.connect(usernames)
        cursor = db.cursor()
        cursor.execute(
            """
            CREATE TABLE data(username TEXT, appname TEXT, artifactname text, html_report text, data TEXT)
            """
        )
        db.commit()

    a = 0
    length = (len(data_list_usernames))
    while a < length:
        user = data_list_usernames[a][0]
        app = data_list_usernames[a][1]
        artifact = data_list_usernames[a][2]
        html_report = data_list_usernames[a][3]
        data = data_list_usernames[a][4]
        cursor.execute("INSERT INTO data VALUES(?,?,?,?,?)", (user, app, artifact, html_report, data))
        a += 1
    db.commit()
    db.close()

def ipgen(report_folder, data_list_ipaddress):
    report_folder = report_folder.rstrip('/')
    report_folder = report_folder.rstrip('\\')
    report_folder_base = os.path.dirname(os.path.dirname(report_folder))
    udb_report_folder = os.path.join(report_folder_base, '_IPAddress DB')

    if os.path.isdir(udb_report_folder):
        ipaddress = os.path.join(udb_report_folder, '_ipaddresses.db')
        db = sqlite3.connect(ipaddress)
        cursor = db.cursor()
        cursor.execute('''PRAGMA synchronous = EXTRA''')
        cursor.execute('''PRAGMA journal_mode = WAL''')
        db.commit()
    else:
        os.makedirs(udb_report_folder)
        ipaddress = os.path.join(udb_report_folder, '_ipaddresses.db')
        db = sqlite3.connect(ipaddress)
        cursor = db.cursor()
        cursor.execute(
            """
            CREATE TABLE data(ipaddress TEXT, appname TEXT, artifactname text, html_report text, data TEXT)
            """
        )
        db.commit()

    a = 0
    length = (len(data_list_ipaddress))
    while a < length:
        ip_address = data_list_ipaddress[a][0]
        app = data_list_ipaddress[a][1]
        artifact = data_list_ipaddress[a][2]
        html_report = data_list_ipaddress[a][3]
        data = data_list_ipaddress[a][4]
        cursor.execute("INSERT INTO data VALUES(?,?,?,?,?)", (ip_address, app, artifact, html_report, data))
        a += 1
    db.commit()
    db.close()

def _count_generator(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024 * 1024)

def _get_line_count(file):
    with open(file, 'rb') as fp:
        return sum(buffer.count(b'\n') for buffer in _count_generator(fp.raw.read))

def gather_hashes_in_file(file_found: str, regex: Pattern):
    target_hashes = {}

    factor = int(_get_line_count(file_found) / 100)
    with open(file_found, 'r') as data:
        for i, x in enumerate(data): 
            if i % factor == 0:
                pass
                #GuiWindow.SetProgressBar(int(i / factor))

            result = regex.search(x)
            if not result:
                continue

            for hash in result.group(1).split(", "):
                deserialized = json.loads(x)
                eventmessage = deserialized.get('eventMessage', '')
                targetstart = hash[:5]
                targetend = hash[-5:]
                eventtimestamp = deserialized.get('timestamp', '')[0:25]
                subsystem = deserialized.get('subsystem', '')
                category = deserialized.get('category', '')
                traceid = deserialized.get('traceID', '')

                # We assume same hash equals same phone
                if (targetstart, targetend) not in target_hashes:
                    logfunc(f"Add {targetstart}...{targetend} to target list")
                    target_hashes[(targetstart, targetend)] = [eventtimestamp, None, eventmessage,
                                                               subsystem, category, traceid]
    return target_hashes

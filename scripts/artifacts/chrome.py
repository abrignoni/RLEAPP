__artifacts_v2__ = {
    "chrome_omnibox": {
        "name": "Chrome - Omnibox",
        "description": "Parses Google Chrome Omnibox / typed URL value information from Takeout",
        "author": "@stark4n6",
        "creation_date": "2023-08-24",
        "last_update_date": "2026-06-22",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": "*/Chrome/Omnibox.json",
        "output_types": "standard",
        "artifact_icon": "search",
    },
    "chrome_reading_list": {
        "name": "Chrome - Reading List",
        "description": "Parses Google Chrome reading list from Takeout",
        "author": "@stark4n6",
        "creation_date": "2023-08-24",
        "last_update_date": "2026-06-22",
        "requirements": "beautifulsoup4",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": "*/Chrome/ReadingList.html",
        "output_types": "standard",
        "artifact_icon": "list",
    },
    "chrome_search_engines": {
        "name": "Chrome - Search Engines",
        "description": "Parses Google Chrome Search Engines from Takeout",
        "author": "@stark4n6 & @upintheairsheep",
        "creation_date": "2023-08-17",
        "last_update_date": "2026-06-22",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": "*/Chrome/SearchEngines.json",
        "output_types": "standard",
        "artifact_icon": "search",
    },
    "chrome_bookmarks": {
        "name": "Chrome - Bookmarks",
        "description": "Parses Google Chrome bookmarks from Takeout",
        "author": "@stark4n6",
        "creation_date": "2023-08-21",
        "last_update_date": "2026-06-22",
        "requirements": "beautifulsoup4",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": "*/Chrome/Bookmarks.html",
        "output_types": "standard",
        "artifact_icon": "star",
    },
    "chrome_device_info": {
        "name": "Chrome - Device Info",
        "description": "Parses Google Chrome synced device information from Takeout",
        "author": "@stark4n6",
        "creation_date": "2023-08-24",
        "last_update_date": "2026-06-22",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": "*/Chrome/Device Information.json",
        "output_types": "standard",
        "artifact_icon": "device-mobile",
    },
    "chrome_extensions": {
        "name": "Chrome - Extensions",
        "description": "Parses Google Chrome Extensions from Takeout",
        "author": "@stark4n6",
        "creation_date": "2021-08-24",
        "last_update_date": "2026-06-22",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": "*/Chrome/Extensions.json",
        "output_types": "standard",
        "artifact_icon": "tool",
    },
    "chrome_history": {
        "name": "Chrome - History",
        "description": "Parses Google Chrome History from Takeout",
        "author": "@stark4n6",
        "creation_date": "2021-08-20",
        "last_update_date": "2026-06-22",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": "*/Chrome/BrowserHistory.json",
        "output_types": "standard",
        "artifact_icon": "brand-chrome",
    },
    "chrome_os_settings": {
        "name": "Chrome - OS Settings",
        "description": "Parses OS Settings from Google Takeout",
        "author": "@stark4n6 & @upintheairsheep",
        "creation_date": "2023-08-18",
        "last_update_date": "2026-06-22",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": "*/Chrome/OS Settings.json",
        "output_types": "standard",
        "artifact_icon": "settings",
    },
    "chrome_arc_packages": {
        "name": "Chrome - ARC Packages",
        "description": "Parses OS Settings from Google Takeout",
        "author": "@stark4n6 & @upintheairsheep",
        "creation_date": "2023-08-18",
        "last_update_date": "2026-06-22",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": "*/Chrome/OS Settings.json",
        "output_types": "standard",
        "artifact_icon": "package",
    },
    "chrome_autofill": {
        "name": "Chrome - Autofill",
        "description": "Parses Google Chrome Autofill value information from Takeout",
        "author": "@stark4n6 & @upintheairsheep",
        "creation_date": "2023-08-18",
        "last_update_date": "2026-06-22",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": "*/Chrome/Autofill.json",
        "output_types": "standard",
        "artifact_icon": "pencil-minus",
    },
}

import bs4
import datetime
import json
from scripts.ilapfuncs import artifact_processor, get_file_path

@artifact_processor
def chrome_omnibox(context):
    files_found = context.get_files_found()
    data_list = []
    file_found = get_file_path(files_found, 'Omnibox.json')

    with open(file_found, encoding = 'utf-8', mode = 'r') as f:
        data = json.loads(f.read())
    
    if 'Typed Url' in data:
        for site in data['Typed Url']:
            visit_ts = site['visits']
            hidden = site['hidden']
            title = site['title']
            url = site['url']
            #count = len(visit_ts)

            for stamp in visit_ts:
                timestamp = datetime.datetime.utcfromtimestamp((int(stamp)/1000000)-11644473600).strftime('%Y-%m-%d %H:%M:%S')

                data_list.append((timestamp, title, url, hidden))

    data_headers = (('Visit Timestamp','datetime'),'Title','URL','Hidden')
    return data_headers, data_list, file_found

@artifact_processor    
def chrome_reading_list(context):
    files_found = context.get_files_found()
    data_list = []
    file_found = get_file_path(files_found, 'ReadingList.html')

    with open(file_found, encoding='utf-8') as fp:
        soup = bs4.BeautifulSoup(fp.read(), 'html.parser')
        
    dt = soup.find_all('dt')
    
    for i in dt:
        n = i.find_next()
        url = n.get('href','')
        title = n.text
        add_date = n.get('add_date','')
        add_date = datetime.datetime.utcfromtimestamp((int(add_date)/1000000)).strftime('%Y-%m-%d %H:%M:%S')
            
        data_list.append((add_date,title,url))
        
    data_headers = (('Added Timestamp','datetime'),'Title','URL')
    return data_headers, data_list, file_found
    
@artifact_processor
def chrome_search_engines(context):
    files_found = context.get_files_found()
    data_list = []
    file_found = get_file_path(files_found, 'SearchEngines.json')

    with open(file_found, encoding = 'utf-8', mode = 'r') as f:
        data = json.loads(f.read())

    for site in data['Search Engines']:
        sEng_date = site.get('date_created','')
        if sEng_date == 0:
            sEng_date = ''
        else:
            sEng_date = datetime.datetime.utcfromtimestamp(int(sEng_date)/1000000).strftime('%Y-%m-%d %H:%M:%S.%f')
        sEng_lastModified = site.get('last_modified','')
        if sEng_lastModified == 0:
            sEng_lastModified = ''
        else:
            sEng_lastModified = datetime.datetime.utcfromtimestamp(int(sEng_lastModified)/1000000).strftime('%Y-%m-%d %H:%M:%S.%f')
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

        data_list.append((sEng_date, sEng_lastModified, sEng_shortName, sEng_kWord, sEng_url, sEng_originUrl, sEng_syncGUID, sEng_favicon_url, sEng_suggestions_url, sEng_ntpurl, sEng_inputEnc, sEng_safeAreplace, sEng_prePopID, sEng_imageurlpostparams, sEng_isActive, sEng_imageurl, sEng_starterpackID))

    data_headers = (('Date Created','datetime'),('Date Last Modified','datetime'),'(Short) Name','Keyword','URL Syntax','API URL', 'Sync GUID', 'Favicon URL', 'Suggestions URL', 'New Tab URL', 'Input Encodings', 'Safe Autoreplace?', 'Pre-populate ID', 'Image URL Post Parameters', 'Is Active?', 'Image URL', 'Starter Pack ID')
    return data_headers, data_list, file_found

@artifact_processor
def chrome_bookmarks(context):
    files_found = context.get_files_found()
    data_list = []
    file_found = get_file_path(files_found, 'Bookmarks.html')

    with open(file_found, encoding='utf-8') as fp:
        soup = bs4.BeautifulSoup(fp.read(), 'html.parser')
        
    dt = soup.find_all('dt')
    
    add_date = ''
    last_modified = ''
    title = ''
    url = ''
    folder_name = ''
    
    for i in dt:
        n = i.find_next()
        if n.name == 'h3':
            folder_name = n.text
            title = n.text
            add_date = n.get('add_date','')
            if add_date == '0' or len(add_date) == 0:
                add_date = ''
            else:
                if len(add_date) == 13:
                    add_date = datetime.datetime.utcfromtimestamp(int(add_date)/1000).strftime('%Y-%m-%d %H:%M:%S')  
                else:
                    add_date = datetime.datetime.utcfromtimestamp((int(add_date)/1000000)-11644473600).strftime('%Y-%m-%d %H:%M:%S')
            
            last_modified = n.get('last_modified','')
            if last_modified == '0' or len(last_modified) == 0:
                last_modified = ''
            else:    
                last_modified = datetime.datetime.utcfromtimestamp(int(last_modified)/1000).strftime('%Y-%m-%d %H:%M:%S')
            
            data_list.append((add_date,last_modified,title,'',''))
            add_date = ''
            last_modified = ''
            title = ''
            continue
        else:
            url = n.get('href','')
            title = n.text
            add_date = n.get('add_date','')
            if len(add_date) == 13:
                add_date = datetime.datetime.utcfromtimestamp(int(add_date)/1000).strftime('%Y-%m-%d %H:%M:%S')  
            else:
                add_date = datetime.datetime.utcfromtimestamp((int(add_date)/1000000)-11644473600).strftime('%Y-%m-%d %H:%M:%S')
            last_modified = n.get('last_modified','')
            if last_modified == '0' or len(last_modified) == 0:
                last_modified = ''
            else:    
                last_modified = datetime.datetime.utcfromtimestamp(int(last_modified)/1000).strftime('%Y-%m-%d %H:%M:%S')  
            
            data_list.append((add_date,last_modified,title,url,folder_name))

    data_headers = (('Added Timestamp','datetime'),('Last Modified','datetime'),'Title','URL','Parent Folder Name')
    return data_headers, data_list, file_found

@artifact_processor
def chrome_device_info(context):
    files_found = context.get_files_found()
    data_list = []
    file_found = get_file_path(files_found, 'Device Information.json')

    with open(file_found, encoding = 'utf-8', mode = 'r') as f:
        data = json.loads(f.read())

    if 'Device Info' in data:
        for device in data['Device Info']:
            last_updated_timestamp = device.get('last_updated_timestamp','')
            last_updated_timestamp = datetime.datetime.utcfromtimestamp((int(last_updated_timestamp)/1000)).strftime('%Y-%m-%d %H:%M:%S')
            
            manufacturer = device.get('manufacturer','')
            model = device.get('model','')
            client_name = device.get('client_name','')
            os_type = device.get('os_type','')[8:]
            device_type = device.get('device_type','')[5:]
            chrome_version = device.get('chrome_version','')
            sync_user_agent = device.get('sync_user_agent','')
            signin_scoped_device_id = device.get('signin_scoped_device_id','')
            
            data_list.append((last_updated_timestamp,manufacturer,model,client_name,os_type,device_type,chrome_version,sync_user_agent,signin_scoped_device_id))

    data_headers = (('Last Updated Timestamp','datetime'),'Manufacturer','Model','Client Name','OS Type','Device Type','Chrome Version','User Agent','Device ID')
    return data_headers, data_list, file_found

@artifact_processor
def chrome_extensions(context):
    files_found = context.get_files_found()
    data_list = []
    file_found = get_file_path(files_found, 'Extensions.json')

    with open(file_found, encoding = 'utf-8', mode = 'r') as f:
        data = json.loads(f.read())

    for site in data['Extensions']:
        ext_name = site.get('name','')
        ext_version = site.get('version','')
        ext_ID = site.get('id','')
        ext_enabled = site.get('enabled','')
        incoginito_enabled = site.get('incognito_enabled','')
        remote_install = site.get('remote_install','')
           
        data_list.append((ext_name, ext_version, ext_ID, ext_enabled, incoginito_enabled, remote_install))

    data_headers = ('Name','Version','ID','Enabled','Incognito Enabled','Remote Install')
    return data_headers, data_list, file_found
    
@artifact_processor
def chrome_history(context):
    files_found = context.get_files_found()
    data_list = []
    file_found = get_file_path(files_found, 'BrowserHistory.json')

    with open(file_found, encoding = 'utf-8', mode = 'r') as f:
        data = json.loads(f.read())

    url = ''
    title = ''
    timestamp = ''
    page_transition = ''

    for site in data['Browser History']:
        url = site['url']
        title = site['title']
        timestamp = datetime.datetime.utcfromtimestamp(int(site['time_usec'])/1000000).strftime('%Y-%m-%d %H:%M:%S.%f')
        page_transition = site['page_transition']

        data_list.append((timestamp, title, url, page_transition))

    data_headers = (('Timestamp','datetime'),'Webpage Title','URL','Page Transition')
    return data_headers, data_list, file_found
    
@artifact_processor
def chrome_arc_packages(context):
    files_found = context.get_files_found()
    data_list = []
    file_found = get_file_path(files_found, 'OS Settings.json')

    with open(file_found, encoding = 'utf-8', mode = 'r') as f:
        data = json.loads(f.read())

    for package in data['Arc Package']:
        chromeARC_lastBack = package['last_backup_time']
        if chromeARC_lastBack == 0:
            chromeARC_lastBack = ''
        else:
            chromeARC_lastBack = datetime.datetime.utcfromtimestamp(int(chromeARC_lastBack)/1000000).strftime('%Y-%m-%d %H:%M:%S.%f')
        chromeARC_name = package.get('package_name','')
        chromeARC_ver = package.get('package_version','')
        chromeARC_bkID = package.get('last_backup_android_id','')

        data_list.append((chromeARC_lastBack, chromeARC_name, chromeARC_ver, chromeARC_bkID))

    data_headers = (('Last Backed Up Timestamp','datetime'),'Package Name','Package Version','Last Backup Android ID')
    return data_headers, data_list, file_found
        
@artifact_processor
def chrome_os_settings(context):
    files_found = context.get_files_found()
    data_list = []
    file_found = get_file_path(files_found, 'OS Settings.json')
    
    with open(file_found, encoding = 'utf-8', mode = 'r') as f:
        data = json.loads(f.read())
    
    for pref in data['OS Priority Preference']:
        pref_name = pref['preference']['name']
        pref_value = pref['preference']['value']
        preference_value = json.loads(pref_value)
        gender = preference_value['gender']
        if gender == 0:
            gender = 'Female'
        elif gender == 1:
            gender = 'Male'
        elif gender == 2:
            gender = 'Rather not say'
        else:
            gender = 'Other'
        birth_year = preference_value['birth_year']

        data_list.append((pref_name,gender,birth_year))

    data_headers = ('Preference Name','User Gender','User Birth Year')
    return data_headers, data_list, file_found
    
@artifact_processor
def chrome_autofill(context):
    files_found = context.get_files_found()
    data_list = []
    file_found = get_file_path(files_found, 'Autofill.json')

    with open(file_found, encoding = 'utf-8', mode = 'r') as f:
        data = json.loads(f.read())

    if 'Autofill' in data:
        for site in data['Autofill']:
            chromeautofill_name = site['name']
            chromeautofill_value = site['value']
            chromeautofill_usage = site['usage_timestamp']

            for stamp in chromeautofill_usage:
                timestamp = datetime.datetime.utcfromtimestamp((int(stamp)/1000000)-11644473600).strftime('%Y-%m-%d %H:%M:%S')
                data_list.append((timestamp, chromeautofill_name, chromeautofill_value))

    data_headers = (('Usage Timestamp','datetime'),'Field Type', 'Typed Value')
    return data_headers, data_list, file_found

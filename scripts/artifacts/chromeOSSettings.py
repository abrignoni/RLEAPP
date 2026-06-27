__artifacts_v2__ = {
    "chromeArcPackages": {
        "name": "Chrome ARC Packages",
        "description": "Parses ARC (Android) package backup info from Google Takeout OS Settings.json",
        "author": "@upintheairsheep & @KevinPagano3",
        "creation_date": "2023-08-18",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": ('*/Chrome/OS Settings.json'),
        "output_types": "standard",
        "artifact_icon": "package",
    },
    "chromeOSSettings": {
        "name": "Chrome OS Settings",
        "description": "Parses user OS priority preferences (gender, birth year) from Google Takeout OS Settings.json",
        "author": "@upintheairsheep & @KevinPagano3",
        "creation_date": "2023-08-18",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": ('*/Chrome/OS Settings.json'),
        "output_types": "standard",
        "artifact_icon": "settings",
    }
}

import json
import os

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


@artifact_processor
def chromeArcPackages(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found) != 'OS Settings.json':
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            data = json.load(f)

        for package in data.get('Arc Package', []):
            last_backup = package.get('last_backup_time', '')
            last_backup = convert_unix_ts_to_utc(last_backup) if last_backup else ''
            data_list.append((last_backup, package.get('package_name', ''),
                              package.get('package_version', ''),
                              package.get('last_backup_android_id', '')))

    data_headers = (('Last Backed Up Timestamp', 'datetime'), 'Package Name',
                    'Package Version', 'Last Backup Android ID')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def chromeOSSettings(context):
    data_list = []
    source_path = ''
    genders = {0: 'Female', 1: 'Male', 2: 'Rather not say'}
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found) != 'OS Settings.json':
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            data = json.load(f)

        for pref in data.get('OS Priority Preference', []):
            pref_name = pref['preference']['name']
            preference_value = json.loads(pref['preference']['value'])
            gender = genders.get(preference_value.get('gender'), 'Other')
            birth_year = preference_value.get('birth_year', '')
            data_list.append((pref_name, gender, birth_year))

    data_headers = ('Preference Name', 'User Gender', 'User Birth Year')
    return data_headers, data_list, context.get_relative_path(source_path)

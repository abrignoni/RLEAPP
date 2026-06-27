__artifacts_v2__ = {
    "takeoutLocationHistorySettings": {
        "name": "Google Location History - Settings",
        "description": "Account and Device Data for Google Location History (Settings.json).",
        "author": "@MetadataForensics by @SQL_McGee",
        "creation_date": "2024-03-21",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "Device Information is also parsed by the Google Location History Data Parser: https://github.com/MetadataForensics/Google-Location-History-Data-Parser",
        "paths": ('*/Location History*/Settings.json',),
        "output_types": "standard",
        "artifact_icon": "settings",
    }
}

import json
import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor

# Lookup table for Android OS versions, values from https://apilevels.com/
android_versions = {
    34: 'Android 14', 33: 'Android 13', 32: 'Android 12', 31: 'Android 12',
    30: 'Android 11', 29: 'Android 10', 28: 'Android 9.0', 27: 'Android 8.1',
    26: 'Android 8.0', 25: 'Android 7.1', 24: 'Android 7.0', 23: 'Android 6',
    22: 'Android 5.1', 21: 'Android 5.0', 20: 'Android 4.4W', 19: 'Android 4.4',
    18: 'Android 4.3', 17: 'Android 4.2', 16: 'Android 4.1',
    15: 'Android 4.0.3 - 4.0.4', 14: 'Android 4.0.1 - 4.0.2', 13: 'Android 3.2',
    12: 'Android 3.1', 11: 'Android 3.0', 10: 'Android 2.3.3 - 2.3.7',
    9: 'Android 2.3.0 - 2.3.2', 8: 'Android 2.2', 7: 'Android 2.1',
    6: 'Android 2.0.1', 5: 'Android 2.0', 4: 'Android 1.6', 3: 'Android 1.5',
    2: 'Android 1.1', 1: 'Android 1.0',
}

iphone_models = {
    'iPhone1,1': 'Original iPhone (1st generation)', 'iPhone1,2': 'iPhone 3G',
    'iPhone2,1': 'iPhone 3GS', 'iPhone3,1': 'iPhone 4', 'iPhone3,2': 'iPhone 4',
    'iPhone3,3': 'iPhone 4', 'iPhone4,1': 'iPhone 4s', 'iPhone5,1': 'iPhone 5',
    'iPhone5,2': 'iPhone 5', 'iPhone5,3': 'iPhone 5c', 'iPhone5,4': 'iPhone 5c',
    'iPhone6,1': 'iPhone 5s', 'iPhone6,2': 'iPhone 5s', 'iPhone7,1': 'iPhone 6 Plus',
    'iPhone7,2': 'iPhone 6', 'iPhone8,1': 'iPhone 6s', 'iPhone8,2': 'iPhone 6s Plus',
    'iPhone8,4': 'iPhone SE (1st generation)', 'iPhone9,1': 'iPhone 7',
    'iPhone9,2': 'iPhone 7 Plus', 'iPhone9,3': 'iPhone 7 (Global)',
    'iPhone9,4': 'iPhone 7 Plus (Global)', 'iPhone10,1': 'iPhone 8',
    'iPhone10,2': 'iPhone 8 Plus', 'iPhone10,3': 'iPhone X',
    'iPhone10,4': 'iPhone 8 (Global)', 'iPhone10,5': 'iPhone 8 Plus (Global)',
    'iPhone10,6': 'iPhone X (Global)', 'iPhone11,2': 'iPhone Xs',
    'iPhone11,4': 'iPhone Xs Max (China)', 'iPhone11,6': 'iPhone Xs Max',
    'iPhone11,8': 'iPhone XR', 'iPhone12,1': 'iPhone 11', 'iPhone12,3': 'iPhone 11 Pro',
    'iPhone12,5': 'iPhone 11 Pro Max', 'iPhone12,8': 'iPhone SE (2nd generation)',
    'iPhone13,1': 'iPhone 12 Mini', 'iPhone13,2': 'iPhone 12',
    'iPhone13,3': 'iPhone 12 Pro', 'iPhone13,4': 'iPhone 12 Pro Max',
    'iPhone14,4': 'iPhone 13 mini', 'iPhone14,5': 'iPhone 13',
    'iPhone14,2': 'iPhone 13 Pro', 'iPhone14,3': 'iPhone 13 Pro Max',
    'iPhone14,6': 'iPhone SE', 'iPhone14,7': 'iPhone 14', 'iPhone14,8': 'iPhone 14 Plus',
    'iPhone15,2': 'iPhone 14 Pro', 'iPhone15,3': 'iPhone 14 Pro Max',
    'iPhone15,4': 'iPhone 15', 'iPhone15,5': 'iPhone 15 Plus',
    'iPhone16,1': 'iPhone 15 Pro', 'iPhone16,2': 'iPhone 15 Pro Max',
}


def _iso_to_utc(value):
    if not value:
        return value
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(timezone.utc)
    except (ValueError, AttributeError):
        return value


@artifact_processor
def takeoutLocationHistorySettings(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found) != 'Settings.json':
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            data = json.load(f)

        # --- account-level fields (same for every device row) ---
        created_time = _iso_to_utc(data.get('createdTime', ''))
        modified_time = _iso_to_utc(data.get('modifiedTime', ''))
        history_enabled = data.get('historyEnabled', data.get('timelineEnabled'))
        deletion_time = _iso_to_utc(data.get('historyDeletionTime',
                                             data.get('timelineDeletionTime', '')))
        history_change = _iso_to_utc(
            data.get('latestLocationHistorySettingChange', {}).get('historyEnabledModificationTime')
            or data.get('latestTimelineSettingChange', {}).get('timelineEnabledModificationTime', ''))
        retention = data.get('retentionWindowDays',
                             data.get('retentionControl', {}).get('retentionWindowDays'))
        encrypted_backups = data.get('encryptedBackupsControls')
        if encrypted_backups:
            encrypted_backups_info = '\n'.join(
                f"Device Tag: {key}, Enabled: {val.get('enabled')}"
                for key, val in encrypted_backups.items())
        else:
            encrypted_backups_info = "New Data Supported in Recent Export Versions"
        has_reported = data.get('hasReportedLocations')
        has_set_retention = data.get('hasSetRetention')

        # --- one row per device ---
        for device in data.get('deviceSettings', []):
            country = device.get('legalCountryCode', '')
            country = country.upper() if country else country
            os_version = (device.get('iosVersion')
                          or android_versions.get(device.get('androidOsLevel'), '') or '')
            spec = device.get('deviceSpec', {}).get('device', '')
            spec = iphone_models.get(spec, spec)
            activeness = device.get('deviceActiveness', {})
            reporting_change = _iso_to_utc(
                device.get('latestLocationReportingSettingChange', {})
                .get('reportingEnabledModificationTime', ''))
            data_list.append((
                created_time, modified_time, history_enabled, deletion_time,
                device.get('deviceTag'), device.get('reportingEnabled'), country,
                device.get('devicePrettyName', ''), device.get('platformType', ''),
                _iso_to_utc(device.get('deviceCreationTime', '')), reporting_change,
                os_version, spec,
                activeness.get('hasSavedTimelineData', "New Data Supported in Recent Export Versions"),
                activeness.get('observedPlaceVisitsFor30PercentOfTheLast7d',
                               "New Data Supported in Recent Export Versions"),
                history_change, retention, encrypted_backups_info,
                has_reported, has_set_retention))

    data_headers = (
        ('Google Account Creation Time', 'datetime'), ('Location History Modified Time', 'datetime'),
        'History Enabled', ('History/Timeline Deletion Time', 'datetime'), 'Device Tag',
        'Device Reporting Enabled', 'Device Country Code', 'Device Pretty Name',
        'Device Platform Type', ('Device Creation Time', 'datetime'),
        ('Device Latest Location History Setting Change', 'datetime'), 'Device OS Version',
        'Device Model', 'Has Saved Timeline Data',
        'ObservedPlace Visits for 30% of the last 7 Days',
        ('Google Account Latest Location History Setting Change', 'datetime'),
        'Google Account Retention Window (in Days)', 'Encrypted Backups Controls',
        'Has Reported Locations', 'Has Set Retention')
    return data_headers, data_list, context.get_relative_path(source_path)

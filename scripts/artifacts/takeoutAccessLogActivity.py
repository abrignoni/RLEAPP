__artifacts_v2__ = {
    "takeoutAccessLogActivities": {
        "name": "Google Access Log Activities",
        "description": "A list of Google services accessed by your devices (e.g. each time a phone syncs with Gmail).",
        "author": "@KevinPagano3",
        "creation_date": "2021-09-25",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": ('*/Access Log Activity/Activities*.csv',),
        "output_types": "standard",
        "artifact_icon": "activity",
    },
    "takeoutAccessLogDevices": {
        "name": "Google Access Log Devices",
        "description": "A list of devices (Nest, Pixel, iPhone, Galaxy, etc.) that accessed your Google account in the last 30 days.",
        "author": "@KevinPagano3",
        "creation_date": "2021-09-25",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "Old-format exports store last country/activity-time inside a free-text field; that legacy string slicing is preserved as-is.",
        "paths": ('*/Access Log Activity/Devices*.csv',),
        "output_types": "standard",
        "artifact_icon": "smartphone",
    }
}

import csv
import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, ipgen


def _iso_to_utc(value):
    if not value:
        return value
    try:
        return datetime.fromisoformat(value.strip().replace('Z', '+00:00')).astimezone(timezone.utc)
    except (ValueError, AttributeError):
        return value


@artifact_processor
def takeoutAccessLogActivities(context):
    data_list = []
    ip_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).startswith('Activities - A list of Google services accessed by'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',')
            header_row = next(reader, [])
            is_new = 'Referer Product Name' in header_row   # was a no-op 'flag == True' in the original
            for item in reader:
                if len(item) < (16 if is_new else 13):
                    continue
                if is_new:
                    referer_product, referer_sub = item[11], item[12]
                    activity_type, gmail_channel, android_webview = item[13], item[14], item[15]
                else:
                    referer_product = referer_sub = android_webview = ''
                    activity_type, gmail_channel = item[11], item[12]
                data_list.append((_iso_to_utc(item[1]), item[2], item[3], item[4], item[5], item[6],
                                  item[7], item[8], item[9], item[10], referer_product, referer_sub,
                                  activity_type, gmail_channel, android_webview, item[0]))
                if item[2]:
                    ip_list.append((item[2], 'Google Access Log Activities',
                                    'Takeout_Ipaddress_logins', '', None))

    if ip_list:
        ipgen(context.get_report_folder(), ip_list)

    data_headers = (('Timestamp', 'datetime'), 'IP Address', 'Proxied Host IP Address',
                    'Is Non-routable IP Address', 'Activity Country', 'Activity Region',
                    'Activity City', 'User Agent String', 'Product Name', 'Sub-Product Name',
                    'Referer Product Name', 'Referer Sub-Product Name', 'Activity Type',
                    'Gmail Access Channel', 'Android Webview Package Name', 'GAIA ID')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def takeoutAccessLogDevices(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).startswith('Devices - A list of devices'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',')
            header_row = next(reader, [])
            is_new = 'Country' in header_row   # was a no-op 'flag == True' in the original
            for item in reader:
                if len(item) < 9:
                    continue
                if is_new:
                    data_list.append((_iso_to_utc(item[7]), _iso_to_utc(item[8]), item[1], item[2],
                                      item[3], item[4], '', item[5], _iso_to_utc(item[6]), item[0]))
                else:
                    last_loc = item[7].replace('\n', ' ')
                    ci = last_loc.find('Country ISO: ')
                    last_country = last_loc[ci + 12:ci + 15].strip() if ci != -1 else ''
                    ai = last_loc.find('Last Activity Time:')
                    last_activity = last_loc[ai + 20:ai + 39].strip() if ai != -1 else ''
                    data_list.append(('', _iso_to_utc(last_activity), item[0], item[1], item[5],
                                      item[3], item[4], last_country, '', item[8]))

    data_headers = (('First Activity Timestamp', 'datetime'), ('Last Activity Timestamp', 'datetime'),
                    'Device Type', 'Device Brand', 'Device Model', 'Device OS', 'OS Version',
                    'Device Last Country', ('Device Last Location Timestamp', 'datetime'), 'GAIA ID')
    return data_headers, data_list, context.get_relative_path(source_path)

def _meta(name, paths, icon):
    return {"name": f"Netflix - {name}",
            "description": f"{name} from a Netflix law enforcement return.",
            "author": "Mark McKinnon", "creation_date": "2021-09-01",
            "last_update_date": "2026-06-28", "requirements": "none",
            "category": "Netflix Archive", "notes": "", "paths": paths,
            "output_types": "standard", "artifact_icon": icon}


__artifacts_v2__ = {
    "netflixProfiles": _meta("Profiles", ('**/Profiles.csv',), "users"),
    "netflixBillingHistory": _meta("Billing History", ('**/BillingHistory.csv',), "credit-card"),
    "netflixIpLogin": _meta("IP Address Login", ('**/IpAddressesLogin.csv',), "log-in"),
    "netflixIpStreaming": _meta("IP Address Streaming", ('**/IpAddressesStreaming.csv',), "cast"),
    "netflixDevices": _meta("Devices", ('**/Devices.csv',), "smartphone"),
    "netflixViewingActivity": _meta("Viewing Activity", ('**/ViewingActivity.csv',), "play"),
    "netflixSearchHistory": _meta("Search History", ('**/SearchHistory.csv',), "search"),
    "netflixAccountDetails": _meta("Account Details", ('**/AccountDetails.csv',), "user"),
    "netflixMessagesSent": _meta("Messages Sent By Netflix", ('**/MessagesSentByNetflix.csv',),
                                 "mail"),
}

import csv
import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc, usergen, ipgen
from scripts.lavafuncs import sanitize_sql_name

_RESERVED = {'from', 'to', 'order', 'group', 'where', 'select', 'index', 'join', 'references',
             'check', 'default', 'add', 'table', 'column', 'create', 'insert', 'update', 'delete',
             'drop', 'values', 'set', 'primary', 'key', 'unique', 'foreign', 'constraint', 'having',
             'distinct', 'union', 'using'}


def _safe_headers(cells):
    seen, out = {}, []
    for i, cell in enumerate(cells):
        name = str(cell).strip() if cell not in (None, '') else f'Column {i + 1}'
        if sanitize_sql_name(name) in _RESERVED:
            name = f'{name} Value'
        key = name.lower()
        seen[key] = seen.get(key, -1) + 1
        if seen[key]:
            name = f'{name} ({seen[key]})'
        out.append(name)
    return out


def _ts(value):
    if value in (None, ''):
        return ''
    text = str(value).strip()
    if text.isdigit():
        return convert_unix_ts_to_utc(int(text))
    try:
        dt = datetime.fromisoformat(text.replace('Z', '+00:00'))
        return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)
    except ValueError:
        return value


def _dynamic(context, basename, user_col=None, user_key=None):
    headers, data_list, source_path = [], [], ''
    user_list = []
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).startswith(basename):
            continue
        source_path = file_found
        file_headers = None
        with open(file_found, encoding='utf-8', errors='backslashreplace') as f:
            for item in csv.reader(f, delimiter=','):
                if not item:
                    continue
                if file_headers is None:
                    file_headers = _safe_headers(item)
                    continue
                if user_col is not None and len(item) > user_col and item[user_col]:
                    user_list.append((item[user_col], 'Netflix', user_key, '', None))
                row = list(item) + [''] * len(file_headers)
                data_list.append(tuple(row[:len(file_headers)]))
        if file_headers:
            headers = file_headers
    if user_list:
        usergen(context.get_report_folder(), user_list)
    return tuple(headers), data_list, context.get_relative_path(source_path)


@artifact_processor
def netflixProfiles(context):
    data_list, user_list, source_path = [], [], ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).startswith('Profiles.csv'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8', errors='backslashreplace') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader, None)
            for item in reader:
                if len(item) < 3:
                    continue
                data_list.append((item[0], item[1], _ts(item[2])))
                if item[1]:
                    user_list.append((item[1], 'Netflix', 'netflixProfiles', '', None))
    if user_list:
        usergen(context.get_report_folder(), user_list)
    data_headers = ('Profile_Name', 'Email_Address', ('Profile_Creation_Time', 'datetime'))
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def netflixIpLogin(context):
    data_list, ip_list, source_path = [], [], ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).startswith('IpAddressesLogin.csv'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8', errors='backslashreplace') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader, None)
            for item in reader:
                if len(item) < 6:
                    continue
                data_list.append((_ts(item[5]), item[4], item[0], item[1], item[2], item[3]))
                if item[4]:
                    ip_list.append((item[4], 'Netflix', 'netflixIpLogin', '', None))
    if ip_list:
        ipgen(context.get_report_folder(), ip_list)
    data_headers = (('Timestamp', 'datetime'), 'Ip Address', 'Esn', 'Country', 'Region code',
                    'Device description')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def netflixIpStreaming(context):
    data_list, ip_list, source_path = [], [], ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).startswith('IpAddressesStreaming.csv'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8', errors='backslashreplace') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader, None)
            for item in reader:
                if len(item) < 7:
                    continue
                data_list.append((_ts(item[6]), item[4], item[3], item[2], item[5], item[0],
                                  item[1]))
                if item[4]:
                    ip_list.append((item[4], 'Netflix', 'netflixIpStreaming', '', None))
    if ip_list:
        ipgen(context.get_report_folder(), ip_list)
    data_headers = (('Timestamp', 'datetime'), 'Ip Address', 'Device Description',
                    'Localized Device Description', 'Region Code Display Name', 'esn', 'Country')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def netflixBillingHistory(context):
    return _dynamic(context, 'BillingHistory.csv')


@artifact_processor
def netflixDevices(context):
    return _dynamic(context, 'Devices.csv')


@artifact_processor
def netflixViewingActivity(context):
    return _dynamic(context, 'ViewingActivity.csv')


@artifact_processor
def netflixSearchHistory(context):
    return _dynamic(context, 'SearchHistory.csv')


@artifact_processor
def netflixMessagesSent(context):
    return _dynamic(context, 'MessagesSentByNetflix.csv')


@artifact_processor
def netflixAccountDetails(context):
    return _dynamic(context, 'AccountDetails.csv', user_col=2, user_key='netflixAccountDetails')

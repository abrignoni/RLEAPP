def _meta(name, icon):
    return {"name": f"Coinbase - {name}",
            "description": f"{name} from a Coinbase law enforcement return (coinbase_data.json).",
            "author": "Mark McKinnon", "creation_date": "2021-11-25",
            "last_update_date": "2026-06-28", "requirements": "none",
            "category": "Coinbase Archive", "notes": "", "paths": ('**/coinbase_data.json',),
            "output_types": "standard", "artifact_icon": icon}


__artifacts_v2__ = {
    "coinbaseTransactions": _meta("Transactions", "dollar-sign"),
    "coinbaseCardPayment": _meta("Card Payment", "credit-card"),
    "coinbaseConfirmedDevices": _meta("Confirmed Devices", "check-circle"),
    "coinbaseDevicesUsed": _meta("Devices Used", "smartphone"),
    "coinbaseSiteActivity": _meta("Site Activity", "activity"),
    "coinbaseThirdParty": _meta("3rd party authorizations", "share-2"),
    "coinbasePersonalData": _meta("Personal Data", "user"),
}

import json
import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc, usergen, ipgen

transaction_history_columns = ["Account_name", "Amount", "Balance", "Coinbase_id", "Crypto_hash",
                               "Currency", "Instantly_exchanged", "Notes", "Timestamp", "To",
                               "Transfer_id", "Transfer_payment_method"]
card_payment_columns = ["Customer_name", "Expiration_month", "Expiration_year", "First6",
                        "Issue_country", "Issuer", "Last4", "Postal_code", "Type"]
confirmed_devices_columns = ["Confirmed", "Ip_address", "User_agent"]
devices_used_columns = ["Accept", "Accept_encoding", "Accept_language", "Ip_address", "Platform",
                        "Platform_version", "Timezone_locale", "Timezone_string", "User_agent"]
site_activity_columns = ["Action", "Ip_address", "Source", "Time"]
third_party_columns = ["Access_granted", "Access_revoked", "Name"]


def _coinbase_json(context):
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found).lower().startswith('coinbase_data.json'):
            with open(file_found, encoding='utf-8') as f:
                return file_found, json.load(f)
    return '', {}


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


def _financial_section(data, which):
    for top_key, top_val in (data or {}).items():
        if 'Financial' in top_key and isinstance(top_val, dict):
            for sub_key, sub_val in top_val.items():
                bucket = 'transaction' if 'transaction' in sub_key.lower() else (
                    'cards' if 'cards' in sub_key.lower() else None)
                if bucket == which:
                    return sub_val
    return None


def _interaction_section(data, which):
    for top_key, top_val in (data or {}).items():
        if 'Interaction' in top_key and isinstance(top_val, dict):
            for sub_key, sub_val in top_val.items():
                if 'Confirmed' in sub_key:
                    bucket = 'confirmed'
                elif 'Devices' in sub_key:
                    bucket = 'devices'
                elif 'Site' in sub_key:
                    bucket = 'site'
                elif 'Third' in sub_key:
                    bucket = 'third'
                else:
                    bucket = None
                if bucket == which:
                    return sub_val
    return None


def _simple_headers(columns):
    return tuple(('Timestamp', 'datetime') if c == 'Timestamp'
                 else ('Time', 'datetime') if c == 'Time'
                 else ('To Address' if c == 'To' else c) for c in columns)


def _ip_rows(section, columns, artifact_key, context):
    data_list, ip_list = [], []
    for item in section or []:
        row = []
        for col in columns:
            val = item.get(col)
            if col == 'Ip_address' and val is not None:
                ip_list.append((val, 'Coinbase Archive', artifact_key, '', None))
            row.append(_ts(val) if col in ('Timestamp', 'Time') else val)
        data_list.append(row)
    if ip_list:
        ipgen(context.get_report_folder(), ip_list)
    return data_list


@artifact_processor
def coinbaseTransactions(context):
    source_path, data = _coinbase_json(context)
    section = _financial_section(data, 'transaction')
    data_list, user_list = [], []
    for item in section or []:
        row = []
        for col in transaction_history_columns:
            val = item.get(col)
            if col == 'To' and val and '@' in str(val):
                user_list.append((val, 'Coinbase Archive', 'coinbaseTransactions', '', None))
            row.append(_ts(val) if col == 'Timestamp' else val)
        data_list.append(row)
    if user_list:
        usergen(context.get_report_folder(), user_list)
    return _simple_headers(transaction_history_columns), data_list, \
        context.get_relative_path(source_path)


@artifact_processor
def coinbaseCardPayment(context):
    source_path, data = _coinbase_json(context)
    section = _financial_section(data, 'cards')
    data_list = [[item.get(col) for col in card_payment_columns] for item in section or []]
    return _simple_headers(card_payment_columns), data_list, context.get_relative_path(source_path)


@artifact_processor
def coinbaseConfirmedDevices(context):
    source_path, data = _coinbase_json(context)
    section = _interaction_section(data, 'confirmed')
    data_list = _ip_rows(section, confirmed_devices_columns, 'coinbaseConfirmedDevices', context)
    return _simple_headers(confirmed_devices_columns), data_list, \
        context.get_relative_path(source_path)


@artifact_processor
def coinbaseDevicesUsed(context):
    source_path, data = _coinbase_json(context)
    section = _interaction_section(data, 'devices')
    data_list = _ip_rows(section, devices_used_columns, 'coinbaseDevicesUsed', context)
    return _simple_headers(devices_used_columns), data_list, context.get_relative_path(source_path)


@artifact_processor
def coinbaseSiteActivity(context):
    source_path, data = _coinbase_json(context)
    section = _interaction_section(data, 'site')
    data_list = _ip_rows(section, site_activity_columns, 'coinbaseSiteActivity', context)
    return _simple_headers(site_activity_columns), data_list, context.get_relative_path(source_path)


@artifact_processor
def coinbaseThirdParty(context):
    source_path, data = _coinbase_json(context)
    section = _interaction_section(data, 'third')
    data_list = [[item.get(col) for col in third_party_columns] for item in section or []]
    return tuple(third_party_columns), data_list, context.get_relative_path(source_path)


@artifact_processor
def coinbasePersonalData(context):
    source_path, data = _coinbase_json(context)
    personal_section = None
    for top_key, top_val in (data or {}).items():
        if 'Personal' in top_key:
            personal_section = top_val
            break

    data_list, user_list = [], []
    for personal in (personal_section or {}):
        value = personal_section[personal]
        if 'Addresses' in personal:
            for addr in value:
                address_string = ''
                for col in addr:
                    if addr[col] is not None:
                        address_string += str(addr[col]) + '\n'
                data_list.append(['Address', address_string])
        elif 'Employers' in personal:
            for emp in value:
                for col in emp:
                    data_list.append([col, emp[col]])
        elif 'Section' in personal:
            continue
        elif 'Emails' in personal:
            data_list.append([personal, value])
            user_list.append((value, 'Coinbase Archive', 'coinbasePersonalData', '', None))
        else:
            data_list.append([personal, value])
    if user_list:
        usergen(context.get_report_folder(), user_list)
    return ('Name', 'Value'), data_list, context.get_relative_path(source_path)

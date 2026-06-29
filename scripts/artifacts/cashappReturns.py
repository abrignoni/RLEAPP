def _meta(name, icon, html_columns=None):
    meta = {"name": f"CashApp - {name}",
            "description": f"{name} extracted from a Cash App law enforcement return "
                           f"(*-for-subject-SQ_CASH-*.xlsx).",
            "author": "Shawn Ramsey", "creation_date": "2024-02-02",
            "last_update_date": "2026-06-28", "requirements": "openpyxl",
            "category": "Cash App Returns",
            "notes": "Scans every cell of the return workbook with regexes; the account token comes "
                     "from the file name. (The original also collected card/bank/display-name data "
                     "into an AccountInfo object that was never reported - that dead parsing is "
                     "omitted here.)",
            "paths": ('*/*-for-subject-SQ_CASH-*.xlsx',), "output_types": "standard",
            "artifact_icon": icon}
    if html_columns:
        meta["html_columns"] = html_columns
    return meta


__artifacts_v2__ = {
    "cashappEmails": _meta("Emails", "mail"),
    "cashappIPv4": _meta("IPv4", "globe"),
    "cashappIPv6": _meta("IPv6", "globe"),
    "cashappPhoneNumbers": _meta("Phone Numbers", "phone"),
}

import os
import re
from datetime import datetime, timezone

from openpyxl import load_workbook

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc, ipgen

_ACCOUNT_TOKEN_SUBSTR = "-for-subject-SQ_CASH-"

_email_re = re.compile(r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@"
                       r"(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")
_ipv4_re = re.compile(r"^(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|"
                      r"[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                      r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
_ipv6_re = re.compile(
    r"^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|"
    r"([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|"
    r"([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}"
    r"(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|"
    r"[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|"
    r"fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}"
    r"((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|"
    r"([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}"
    r"(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$")
_phone_re = re.compile(r"^\+?[1-9][0-9]{7,14}$")


def _token(file_found):
    idx = file_found.find(_ACCOUNT_TOKEN_SUBSTR)
    if idx == -1:
        return os.path.basename(file_found)
    token = file_found[idx + len(_ACCOUNT_TOKEN_SUBSTR):]
    return token[:-5] if token.endswith('.xlsx') else token


def _to_utc(value):
    if value is None or value == '':
        return ''
    if isinstance(value, datetime):
        return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value.astimezone(timezone.utc)
    text = str(value).strip()
    if not text:
        return ''
    if text.isdigit():
        return convert_unix_ts_to_utc(int(text))
    try:
        dt = datetime.fromisoformat(text.replace('Z', '+00:00'))
        return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)
    except ValueError:
        return value


def _scan(file_found, token):
    emails, ipv4s, ipv6s, phones = [], [], [], []
    workbook = load_workbook(file_found, data_only=True)
    try:
        for sheet_name in workbook.sheetnames:
            sheet = workbook[sheet_name]
            for i in range(1, sheet.max_row + 1):
                for j in range(1, sheet.max_column + 1):
                    value = str(sheet.cell(row=i, column=j).value)
                    if _email_re.match(value):
                        date = sheet.cell(row=i, column=j - 1).value if j > 1 else None
                        emails.append((token, _to_utc(date), value))
                    if _ipv4_re.match(value):
                        ipv4s.append((token, value))
                    if _ipv6_re.match(value):
                        ipv6s.append((token, value))
                    if _phone_re.match(value):
                        above = str(sheet.cell(row=i - 1, column=j).value) if i > 1 else ''
                        if "Full SSN" not in above:
                            date = sheet.cell(row=i, column=j - 1).value if j > 1 else None
                            phones.append((token, _to_utc(date), value))
    finally:
        workbook.close()
    return emails, ipv4s, ipv6s, phones


def _xlsx_files(context):
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if file_found.endswith('.xlsx') and not os.path.basename(file_found).startswith('.'):
            yield file_found


@artifact_processor
def cashappEmails(context):
    data_list, source_path = [], ''
    for file_found in _xlsx_files(context):
        source_path = file_found
        emails, _, _, _ = _scan(file_found, _token(file_found))
        data_list.extend(emails)
    data_headers = ('Account Token', ('UTC Date Time', 'datetime'), 'Email')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def cashappIPv4(context):
    data_list, ip_list, source_path = [], [], ''
    for file_found in _xlsx_files(context):
        source_path = file_found
        token = _token(file_found)
        _, ipv4s, _, _ = _scan(file_found, token)
        data_list.extend(ipv4s)
        for _, ipv4 in ipv4s:
            ip_list.append((ipv4, 'CashApp', f'CashApp IPv4 Return - {token}', '', None))
    if ip_list:
        ipgen(context.get_report_folder(), ip_list)
    data_headers = ('Account Token', 'IPv4')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def cashappIPv6(context):
    data_list, ip_list, source_path = [], [], ''
    for file_found in _xlsx_files(context):
        source_path = file_found
        token = _token(file_found)
        _, _, ipv6s, _ = _scan(file_found, token)
        data_list.extend(ipv6s)
        for _, ipv6 in ipv6s:
            ip_list.append((ipv6, 'CashApp', f'CashApp IPv6 Return - {token}', '', None))
    if ip_list:
        ipgen(context.get_report_folder(), ip_list)
    data_headers = ('Account Token', 'IPv6')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def cashappPhoneNumbers(context):
    data_list, source_path = [], ''
    for file_found in _xlsx_files(context):
        source_path = file_found
        _, _, _, phones = _scan(file_found, _token(file_found))
        data_list.extend(phones)
    data_headers = ('Account Token', ('UTC Date Time', 'datetime'), ('Phone Numbers', 'phonenumber'))
    return data_headers, data_list, context.get_relative_path(source_path)

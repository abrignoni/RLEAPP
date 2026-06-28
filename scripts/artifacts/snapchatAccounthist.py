def _m(name, icon):
    return {"name": f"Snapchat Archive - {name}",
            "description": f"{name} from a Snapchat data archive (account_history.json).",
            "author": "@AlexisBrignoni", "creation_date": "2023-12-11",
            "last_update_date": "2026-06-28", "requirements": "none",
            "category": "Snapchat Archive", "notes": "",
            "paths": ('*/account_history.json',), "output_types": "standard", "artifact_icon": icon}


__artifacts_v2__ = {
    "snapHistDisplayNameChange": _m("Display Name Change", "edit-3"),
    "snapHistEmailChange": _m("Email Change", "mail"),
    "snapHistMobileNumberChange": _m("Mobile Number Change", "phone"),
    "snapHistPasswordChange": _m("Password Change", "key"),
    "snapHistLinkedToBitmoji": _m("Linked to Bitmoji", "smile"),
    "snapHistSpectacles": _m("Spectacles", "eye"),
    "snapHistTwoFactorAuth": _m("Two-Factor Authentication", "shield"),
    "snapHistAccountDeactivated": _m("Account Deactivated - Reactivated", "power"),
    "snapHistDownloadReports": _m("Download My Data Reports", "download"),
}

import json
import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc

_MONTHS = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
           'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}


def _snap_ts(value):
    value = (value or '').strip()
    if not value:
        return value
    cleaned = value.replace(' UTC', '').strip()
    if cleaned.isdigit():
        return convert_unix_ts_to_utc(int(cleaned))
    try:
        dt = datetime.fromisoformat(cleaned.replace('Z', '+00:00'))
        return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)
    except ValueError:
        pass
    try:
        parts = value.split(' ')
        return datetime(int(parts[-1]), _MONTHS[parts[1]], int(parts[2]),
                        *(int(x) for x in parts[3].split(':')), tzinfo=timezone.utc)
    except (IndexError, KeyError, ValueError):
        return value


def _account_history(context):
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found).startswith('account_history.json'):
            with open(file_found, encoding='utf-8') as fp:
                return file_found, json.load(fp)
    return '', {}


@artifact_processor
def snapHistDisplayNameChange(context):
    src, data = _account_history(context)
    rows = [(_snap_ts(it.get('Date', '')), it.get('Display Name', ''))
            for it in data.get('Display Name Change', [])]
    return (('Timestamp', 'datetime'), 'Display Name'), rows, context.get_relative_path(src)


@artifact_processor
def snapHistMobileNumberChange(context):
    src, data = _account_history(context)
    rows = [(_snap_ts(it.get('Date', '')), it.get('Mobile Number', ''))
            for it in data.get('Mobile Number Change', [])]
    return (('Timestamp', 'datetime'), ('Mobile Number', 'phonenumber')), rows, context.get_relative_path(src)


@artifact_processor
def snapHistPasswordChange(context):
    src, data = _account_history(context)
    rows = [(_snap_ts(it.get('Date', '')),) for it in data.get('Password Change', [])]
    return (('Timestamp', 'datetime'),), rows, context.get_relative_path(src)


@artifact_processor
def snapHistLinkedToBitmoji(context):
    src, data = _account_history(context)
    rows = [(_snap_ts(it.get('Date', '')),) for it in data.get('Snapchat Linked to Bitmoji', [])]
    return (('Timestamp', 'datetime'),), rows, context.get_relative_path(src)


@artifact_processor
def snapHistDownloadReports(context):
    src, data = _account_history(context)
    rows = [(_snap_ts(it.get('Date', '')), it.get('Status', ''), it.get('Email Address', ''))
            for it in data.get('Download My Data Reports', [])]
    return (('Timestamp', 'datetime'), 'Status', 'Email Address'), rows, context.get_relative_path(src)


def _single_value(context, key):
    src, data = _account_history(context)
    value = data.get(key)
    rows = [(value,)] if value else []
    return ('Data',), rows, context.get_relative_path(src)


@artifact_processor
def snapHistEmailChange(context):
    return _single_value(context, 'Email Change')


@artifact_processor
def snapHistSpectacles(context):
    return _single_value(context, 'Spectacles')


@artifact_processor
def snapHistTwoFactorAuth(context):
    return _single_value(context, 'Two-Factor Authentication')


@artifact_processor
def snapHistAccountDeactivated(context):
    return _single_value(context, 'Account deactivated / reactivated')

import json
import os
import re
import sqlite3
import xml.etree.ElementTree as ET
from html import unescape

from scripts.context import Context
from scripts.ilapfuncs import (
    artifact_processor,
    logfunc,
    open_sqlite_db_readonly,
)

__artifacts_v2__ = {
    "meta_ai_conversations": {
        "name": "Meta AI - AI Conversations (Cloud)",
        "description": "Conversation history from Meta AI cloud data export",
        "author": "Shishir Panta",
        "creation_date": "2026-04-12",
        "last_update_date": "2026-06-15",
        "requirements": "none",
        "category": "Meta AI",
        "notes": "",
        "paths": ("*/meta_ai_app/*.html",),
        "output_types": ["html", "lava", "tsv"],
        "artifact_icon": "message-square",
    },
    "meta_ai_connected_devices_cloud": {
        "name": "Meta AI - Connected Devices (Cloud)",
        "description": "Device connection history from Meta AI cloud data export",
        "author": "Shishir Panta",
        "creation_date": "2026-04-12",
        "last_update_date": "2026-06-15",
        "requirements": "none",
        "category": "Meta AI",
        "notes": "",
        "paths": ("*/meta_ai_profile/*.html",),
        "output_types": ["html", "lava", "tsv"],
        "artifact_icon": "bluetooth",
    },
    "meta_ai_cloud_media": {
        "name": "Meta AI - Cloud Media Library",
        "description": "Media library entries from Meta AI cloud data export",
        "author": "Shishir Panta",
        "creation_date": "2026-04-12",
        "last_update_date": "2026-06-15",
        "requirements": "none",
        "category": "Meta AI",
        "notes": "",
        "paths": ("*/facebook_view/media/*",),
        "output_types": ["html", "lava", "tsv"],
        "artifact_icon": "image",
    },
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _read_xml_key_value(file_path):
    """Reads key-value pairs from an XML SharedPreferences file."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return {child.attrib.get('name', 'unknown'): child.text for child in root}
    except (ET.ParseError, FileNotFoundError, KeyError) as e:
        logfunc(f"[Meta AI] Could not parse XML file {os.path.basename(file_path)}: {e}")
        return {}


def _parse_binary_prefs(file_path):
    """Parses binary SharedPreferences files (non-XML format)."""
    try:
        with open(file_path, 'rb') as f:
            content = f.read()

        text = content.decode('utf-8', errors='ignore')
        text = text.replace('\x00', ' ').replace('\r', ' ').replace('\n', ' ')
        text = ' '.join(text.split())

        data = {}

        extractions = [
            ('device_serial',                ['device_frame_color_name', 'soc_build']),
            ('device_uuid',                  ['cloud_ota_error', 'build_flags_key']),
            ('btc_address',                  ['device_frame_type', 'device_identifier']),
            ('device_identifier',            ['device_lens_color_name', 'feature_key']),
            ('device_frame_type_short_name', ['device_lens_color']),
            ('device_frame_color_name',      ['soc_build', 'mcu_build', 'build_flavor']),
            ('device_lens_color_name',       ['feature_key', 'sku_code']),
            ('mcu_build',                    ['device_type']),
            ('soc_build',                    ['build_flavor']),
            ('device_type',                  ['device_hardware_type']),
            ('device_hardware_type',         ['device_uuid']),
        ]

        for key, terminators in extractions:
            key_pos = text.find(key)
            if key_pos == -1:
                continue
            value_start = key_pos + len(key)
            value_end = len(text)
            for terminator in terminators:
                term_pos = text.find(terminator, value_start)
                if term_pos != -1 and term_pos < value_end:
                    value_end = term_pos
            value = text[value_start:value_end].strip()
            if value.startswith('$'):
                value = value[1:]
            parts = value.split()
            value = parts[0] if len(parts) == 1 else ' '.join(parts[:4])
            if value:
                data[key] = value

        return data

    except Exception as e:
        logfunc(f"[Meta AI] Could not parse binary prefs file {os.path.basename(file_path)}: {e}")
        return {}


def _ms_to_unix(timestamp_ms):
    """Converts a millisecond timestamp to Unix seconds (float) for LAVA datetime columns."""
    if not timestamp_ms:
        return None
    try:
        return int(timestamp_ms) / 1000.0
    except (ValueError, TypeError):
        return None


def _parse_device_files():
    """
    Parses app_light_prefs files using the Context filename lookup map for
    O(1) access by filename rather than iterating the full file list.
    Returns (paired_devices dict, meta_accounts list).
    """
    lookup = Context.get_filename_lookup_map()
    paired_devices = {}
    meta_accounts  = []

    # connectivity_metadata.xml — direct lookup
    for file_path in lookup.get('connectivity_metadata.xml', []):
        data = _read_xml_key_value(file_path)
        mac = data.get('DEVICE-METADATA-ID', 'Unknown')
        paired_devices.setdefault(mac, {})
        paired_devices[mac]['mac']    = mac
        paired_devices[mac]['serial'] = data.get('serialNumber', '')

    # device_system_info_<mac> — variable suffix, scan map keys once
    for filename, paths in lookup.items():
        if not filename.startswith('device_system_info_'):
            continue
        mac = filename.replace('device_system_info_', '')
        paired_devices.setdefault(mac, {})
        for file_path in paths:
            data = _parse_binary_prefs(file_path)
            if data:
                paired_devices[mac]['mac']         = data.get('device_identifier', mac)
                paired_devices[mac]['btc']         = data.get('btc_address', '')
                paired_devices[mac]['serial']      = data.get('device_serial', '')
                paired_devices[mac]['uuid']        = data.get('device_uuid', '')
                paired_devices[mac]['frame']       = data.get('device_frame_type_short_name', '')
                paired_devices[mac]['frame_color'] = data.get('device_frame_color_name', '')
                paired_devices[mac]['lens']        = data.get('device_lens_color_name', '')
                paired_devices[mac]['mcu_build']   = data.get('mcu_build', '')
                paired_devices[mac]['soc_build']   = data.get('soc_build', '')

    # meta_fx_cache — direct lookup
    for file_path in lookup.get('meta_fx_cache', []):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            for account in cache_data.get('accounts', []):
                meta_accounts.append((
                    account.get('platform', 'Unknown'),
                    account.get('username', account.get('email', '')),
                    account.get('account_id', ''),
                ))
        except (json.JSONDecodeError, UnicodeDecodeError):
            try:
                with open(file_path, 'r', encoding='latin-1', errors='ignore') as f:
                    content = f.read()
                account_ids = re.findall(r'"account_id"\s*:\s*"?(\d+)"?', content)
                platforms   = re.findall(r'"account_type"\s*:\s*"([^"]+)"', content)
                usernames   = re.findall(r'"(?:username|email)"\s*:\s*"([^"]+)"', content)
                for i, account_id in enumerate(account_ids):
                    meta_accounts.append((
                        platforms[i] if i < len(platforms) else 'Unknown',
                        usernames[i] if i < len(usernames) else 'N/A',
                        account_id,
                    ))
            except Exception as e:
                logfunc(f"[Meta AI] Could not parse meta_fx_cache: {e}")

    return paired_devices, meta_accounts


# ---------------------------------------------------------------------------
# Artifact processors
# ---------------------------------------------------------------------------



@artifact_processor
def meta_ai_conversations(context):
    data_headers = (
        'Date',
        'Speaker',
        'Message',
    )
    data_list   = []
    source_path = ''

    for source_path in context.get_files_found():
        try:
            with open(source_path, 'r', encoding='utf-8', errors='ignore') as f:
                html_content = f.read()

            conv_dates = re.findall(
                r'Conversation with Meta AI_(\d{2}-\d{2}-\d{4})_\d+\.txt',
                html_content,
            )
            conv_blocks = re.findall(
                r'<td class="_2piu _a6_r">(Conversation with Meta AI.*?)</td>',
                html_content,
                re.DOTALL,
            )

            for i, block in enumerate(conv_blocks):
                block = unescape(block)
                messages = re.findall(
                    r'(You|Meta AI): (.+?)(?=(?:You|Meta AI):|$)',
                    block,
                    re.DOTALL,
                )
                conv_date = conv_dates[i] if i < len(conv_dates) else 'Unknown'
                for speaker, message in messages:
                    message_clean = message.strip().replace('\n', ' ')
                    if message_clean and message_clean != 'Conversation with Meta AI':
                        data_list.append((conv_date, speaker, message_clean))

        except Exception as e:
            logfunc(f"[Meta AI] Could not parse cloud conversations from {os.path.basename(source_path)}: {e}")

    return data_headers, data_list, source_path


@artifact_processor
def meta_ai_connected_devices_cloud(context):
    data_headers = (
        'Serial Number',
        'Last Update',
    )
    data_list   = []
    source_path = ''

    for source_path in context.get_files_found():
        try:
            with open(source_path, 'r', encoding='utf-8', errors='ignore') as f:
                html_content = f.read()

            serial_match = re.search(
                r'<td class="_a6_q">Serial number</td>\s*<td class="_2piu _a6_r">([^<]+)</td>',
                html_content,
            )
            time_match = re.search(
                r'<td class="_a6_q">Update time</td>\s*<td class="_2piu _a6_r">([^<]+)</td>',
                html_content,
            )
            serial      = serial_match.group(1) if serial_match else 'Unknown'
            update_time = time_match.group(1)   if time_match   else ''

            if serial != 'Unknown':
                data_list.append((serial, update_time))

        except Exception as e:
            logfunc(f"[Meta AI] Could not parse cloud devices from {os.path.basename(source_path)}: {e}")

    return data_headers, data_list, source_path


@artifact_processor
def meta_ai_cloud_media(context):
    data_headers = (
        'Device ID',
        'Timestamp',
        'Media File Path',
    )
    data_list   = []
    source_path = ''

    for source_path in context.get_files_found():
        try:
            with open(source_path, 'r', encoding='utf-8', errors='ignore') as f:
                html_content = f.read()

            sections = re.findall(
                r'<section class="_3-95 _a6-g">.*?</section>',
                html_content,
                re.DOTALL,
            )

            for section in sections:
                device_match = re.search(
                    r'<td class="_a6_q">Device ID</td>\s*<td class="_2piu _a6_r">([^<]+)</td>',
                    section,
                )
                media_match = re.search(
                    r'href="(posts/media/your_posts/[^"]+)"',
                    section,
                )
                time_match = re.search(
                    r'<td class="_2piu _a6_r">([A-Z][a-z]{2} \d{2}, \d{4} \d{1,2}:\d{2} [ap]m)</td>',
                    section,
                )
                device_id  = device_match.group(1) if device_match else 'Unknown'
                media_path = media_match.group(1)  if media_match  else ''
                timestamp  = time_match.group(1)   if time_match   else ''

                if media_path:
                    data_list.append((device_id, timestamp, media_path))

        except Exception as e:
            logfunc(f"[Meta AI] Could not parse cloud media from {os.path.basename(source_path)}: {e}")

    return data_headers, data_list, source_path

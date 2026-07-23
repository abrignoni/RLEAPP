__artifacts_v2__ = {
    "wireCookies": {
        "name": "Wire Cookies",
        "description": "Cookies from the Wire desktop app's network stores "
                       "(Network/Cookies, main profile and Electron partitions). "
                       "Includes the Wire 'zuid' auth session cookie with its "
                       "creation, expiry and last-access times. Cookie values are "
                       "OS-encrypted and are not decrypted here.",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-07-23",
        "last_update_date": "2026-07-23",
        "requirements": "none",
        "category": "Wire",
        "notes": "Only cookies for wire.com hosts are reported.",
        "paths": ('*/Network/Cookies',),
        "output_types": ["html", "tsv", "timeline", "lava"],
        "artifact_icon": "circle",
    },
}

import os
import sqlite3
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, logfunc

# Chromium/WebKit timestamps: microseconds since 1601-01-01 UTC.
_CHROME_EPOCH_OFFSET = 11644473600


def _chrome_us_to_dt(value):
    try:
        us = int(value)
    except (ValueError, TypeError):
        return ""
    if us <= 0:
        return ""
    try:
        return datetime.fromtimestamp(us / 1_000_000 - _CHROME_EPOCH_OFFSET,
                                      tz=timezone.utc)
    except (OSError, OverflowError, ValueError):
        return ""


def _source_label(path):
    parts = path.replace("\\", "/").split("/")
    if "Partitions" in parts:
        i = parts.index("Partitions")
        if i + 1 < len(parts):
            return f"Partition {parts[i + 1]}"
    return "Default profile"


@artifact_processor
def wireCookies(context):
    data_list = []
    source_path = ""
    parsed = set()

    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found) != "Cookies":
            continue
        real = os.path.realpath(file_found)
        if real in parsed:
            continue
        parsed.add(real)

        try:
            con = sqlite3.connect(f"file:{file_found}?mode=ro", uri=True)
            cur = con.cursor()
            cur.execute("""
                SELECT host_key, name, path, creation_utc, expires_utc,
                       last_access_utc, is_secure, is_httponly,
                       length(encrypted_value)
                FROM cookies
                WHERE host_key LIKE '%wire.com%'
                ORDER BY host_key, name
            """)
            rows = cur.fetchall()
            con.close()
        except sqlite3.Error as ex:
            logfunc(f"Wire cookies: could not read '{file_found}': {ex}")
            continue

        if rows:
            source_path = file_found
        label = _source_label(file_found)
        for (host, name, path, created, expires, last_access,
             secure, httponly, enc_len) in rows:
            data_list.append((
                label,
                host,
                name,
                path,
                _chrome_us_to_dt(created),
                _chrome_us_to_dt(expires),
                _chrome_us_to_dt(last_access),
                "Yes" if secure else "",
                "Yes" if httponly else "",
                enc_len or 0,
            ))

    data_headers = (
        "Source", "Host", "Name", "Path", ("Created", "datetime"),
        ("Expires", "datetime"), ("Last Access", "datetime"), "Secure",
        "HttpOnly", "Encrypted Value Length",
    )
    return data_headers, data_list, source_path

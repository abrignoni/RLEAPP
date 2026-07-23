__artifacts_v2__ = {
    "wireDesktopLog": {
        "name": "Wire Desktop Log",
        "description": "Activity timeline parsed from the Wire desktop app log "
                       "(logs/electron.log and electron.old): app launches, "
                       "auth/login navigation, team info sync, updates and other "
                       "notable events. Timestamps are the device's local time as "
                       "written by the app.",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-07-23",
        "last_update_date": "2026-07-23",
        "requirements": "none",
        "category": "Wire",
        "notes": "Repetitive config-restore lines are filtered out.",
        "paths": ('*/logs/electron.log', '*/logs/electron.old'),
        "output_types": ["html", "tsv", "timeline", "lava"],
        "artifact_icon": "file-text",
    },
    "wireDesktopEnvironment": {
        "name": "Wire Desktop Environment",
        "description": "Facts derived from the Wire desktop app log: operating "
                       "system user account, signed-in account/team identity, "
                       "auth session id, custom web-app URL, updater channel and "
                       "log time range.",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-07-23",
        "last_update_date": "2026-07-23",
        "requirements": "none",
        "category": "Wire",
        "notes": "",
        "paths": ('*/logs/electron.log', '*/logs/electron.old'),
        "output_types": ["html", "tsv", "lava"],
        "artifact_icon": "settings",
    },
}

import json
import os
import re

from scripts.ilapfuncs import artifact_processor

# [2026-07-23 15:30:31] [@wireapp/desktop/Component] Message...
_LINE_RE = re.compile(
    r"^\[(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]\s+"
    r"(?:\[(?P<comp>[^\]]+)\]\s+)?(?P<msg>.*)$")

# Lines we drop from the timeline (pure config-restore noise).
_NOISE_RE = re.compile(r'Restoring "|Read config:|Reading config file')

_OSUSER_RE = re.compile(r"[A-Za-z]:\\Users\\([^\\]+)\\", re.IGNORECASE)
_AUTHID_RE = re.compile(r"app\.wire\.com/auth/\?[^ \"']*\bid=([0-9a-f-]{36})")
_TEAMINFO_RE = re.compile(r'wire\.webapp\.team\.info"\s*:\s*"(\{.*?\})"', re.DOTALL)
_WEBAPP_RE = re.compile(r"https://wire-app\.wire\.com/[^\s\"']+")


def _log_files(context):
    """Wire desktop log files found, deduped, that look like the desktop log."""
    parsed = set()
    out = []
    for file_found in context.get_files_found():
        file_found = str(file_found)
        base = os.path.basename(file_found).lower()
        if base not in ("electron.log", "electron.old"):
            continue
        real = os.path.realpath(file_found)
        if real in parsed:
            continue
        parsed.add(real)
        try:
            with open(file_found, "r", encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError:
            continue
        if "@wireapp/desktop" in text:
            out.append((file_found, text))
    return out


@artifact_processor
def wireDesktopLog(context):
    files = _log_files(context)
    data_list = []
    source_path = ""
    for file_found, text in files:
        source_path = file_found
        for line in text.splitlines():
            m = _LINE_RE.match(line.strip())
            if not m:
                continue
            if _NOISE_RE.search(m.group("msg") or ""):
                continue
            comp = (m.group("comp") or "").replace("@wireapp/desktop/", "")
            msg = (m.group("msg") or "").strip()
            data_list.append((m.group("ts"), comp, msg[:1000]))

    data_headers = ("Timestamp (device local)", "Component", "Message")
    return data_headers, data_list, source_path


@artifact_processor
def wireDesktopEnvironment(context):
    files = _log_files(context)
    facts = []  # (property, value, context)
    seen = set()
    source_path = ""

    def add(prop, value, ctx=""):
        if value in (None, ""):
            return
        key = (prop, str(value))
        if key in seen:
            return
        seen.add(key)
        facts.append((prop, str(value), ctx))

    for file_found, text in files:
        source_path = file_found
        fname = os.path.basename(file_found)

        m = _OSUSER_RE.search(text)
        if m:
            add("OS User Account", m.group(1), fname)

        for aid in dict.fromkeys(_AUTHID_RE.findall(text)):
            add("Auth Session / Account ID", aid, fname)

        for url in dict.fromkeys(_WEBAPP_RE.findall(text)):
            add("Wire Web-App / Updater URL", url, fname)

        for raw in _TEAMINFO_RE.findall(text):
            try:
                info = json.loads(raw.encode().decode("unicode_escape"))
            except (ValueError, UnicodeDecodeError):
                try:
                    info = json.loads(raw)
                except ValueError:
                    continue
            add("Team Name", info.get("name"), fname)
            add("Team ID", info.get("teamID"), fname)
            add("Team Role", info.get("teamRole"), fname)
            add("Signed-in User ID", info.get("userID"), fname)

        # log time range
        stamps = re.findall(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]", text)
        if stamps:
            add("Log Start (device local)", stamps[0], fname)
            add("Log End (device local)", stamps[-1], fname)

    data_headers = ("Property", "Value", "Source File")
    return data_headers, facts, source_path

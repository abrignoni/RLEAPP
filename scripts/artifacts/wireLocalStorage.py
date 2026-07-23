__artifacts_v2__ = {
    "wireLocalStorage": {
        "name": "Wire Local Storage",
        "description": "Key/value pairs from the Wire desktop app's Chromium "
                       "Local Storage (main profile and Electron partitions): "
                       "app-instance id, analytics (Countly) device id, favourite "
                       "camera/mic device hashes, UI language and preferences.",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-07-23",
        "last_update_date": "2026-07-23",
        "requirements": "none",
        "category": "Wire",
        "notes": "Only entries for wire.com origins are reported.",
        "paths": ('*/Local Storage/leveldb/*',),
        "output_types": ["html", "tsv", "lava"],
        "artifact_icon": "database",
    },
}

import os

from scripts.ilapfuncs import artifact_processor, logfunc
from scripts.ccl import ccl_leveldb


def _leveldb_dirs(context):
    dirs = {}
    for file_found in context.get_files_found():
        file_found = str(file_found)
        parent = os.path.dirname(file_found)
        if os.path.basename(parent) == "leveldb" and \
                "Local Storage" in parent.replace("\\", "/"):
            dirs.setdefault(os.path.realpath(parent), parent)
    return list(dirs.values())


def _source_label(path):
    parts = path.replace("\\", "/").split("/")
    if "Partitions" in parts:
        i = parts.index("Partitions")
        if i + 1 < len(parts):
            return f"Partition {parts[i + 1]}"
    return "Default profile"


def _decode_value(v):
    if not v:
        return ""
    flag = v[:1]
    body = v[1:]
    try:
        if flag == b"\x00":
            return body.decode("utf-16-le", "replace")
        if flag == b"\x01":
            return body.decode("utf-8", "replace")
        return v.decode("utf-8", "replace")
    except Exception:  # pragma: no cover - defensive
        return v.decode("latin1", "replace")


@artifact_processor
def wireLocalStorage(context):
    data_list = []
    source_path = ""

    for ldb_dir in _leveldb_dirs(context):
        label = _source_label(ldb_dir)
        try:
            db = ccl_leveldb.RawLevelDb(ldb_dir)
        except Exception as ex:  # pragma: no cover - defensive
            logfunc(f"Wire Local Storage: could not open '{ldb_dir}': {ex}")
            continue

        latest = {}
        for rec in db.iterate_records_raw():
            if rec.state.name != "Live":
                continue
            k = rec.user_key or b""
            # Skip Local Storage bookkeeping keys (VERSION, META:*, METAACCESS:*).
            if k == b"VERSION" or k.startswith(b"META"):
                continue
            if k.startswith(b"_") and b"\x00" in k:
                origin, _, item = k.partition(b"\x00")
                origin = origin[1:].decode("utf-8", "replace")
                item = item.decode("utf-8", "replace")
            else:
                origin = ""
                item = k.decode("utf-8", "replace")
            if "wire.com" not in origin and origin != "":
                continue
            latest[(origin, item)] = _decode_value(rec.value)
        db.close()

        if latest:
            source_path = ldb_dir
        for (origin, item), value in latest.items():
            data_list.append((label, origin or "(app)", item, value[:2000]))

    data_headers = ("Source", "Origin", "Key", "Value")
    return data_headers, data_list, source_path

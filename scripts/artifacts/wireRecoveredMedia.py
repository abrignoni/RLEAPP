__artifacts_v2__ = {
    "wireRecoveredMedia": {
        "name": "Wire Recovered Media",
        "description": "Actual images/media recovered by decrypting the Wire "
                       "cached asset blobs (service-worker Cache Storage and the "
                       "HTTP disk cache) with the per-asset keys stored in the "
                       "IndexedDB asset-add events. Each cached blob is matched to "
                       "its event by SHA-256, integrity-verified, then AES-256-CBC "
                       "decrypted with the event otr_key and embedded in the report.",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-07-23",
        "last_update_date": "2026-07-23",
        "requirements": "PyCryptodome",
        "category": "Wire",
        "notes": "Only assets still present in an on-disk cache can be recovered. "
                 "Decryption follows Wire's asset scheme: blob = IV(16) || "
                 "AES-256-CBC ciphertext, SHA-256 taken over the blob.",
        "paths": (
            '*/https_app.wire.com_0.indexeddb.leveldb/*',
            '*/Service Worker/CacheStorage/*/*/*_0',
            '*/Cache_Data/f_*',
        ),
        "output_types": ["html", "tsv", "lava"],
        "artifact_icon": "image",
    },
}

import os
import re
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, logfunc, check_in_embedded_media
from scripts.ccl.indexeddb_to_json import load_indexeddb
from scripts.ccl.wire_assets import build_asset_index, recover_assets, crypto_available

_DBNAME_UUID_RE = re.compile(r"@([0-9a-f]{8}-[0-9a-f-]{27,})@")
_MLS_CRED_RE = re.compile(r"([0-9a-f-]{36}):([0-9a-f]+)@")


# --- self-contained IndexedDB resolvers (mirror wireIndexedDb.py) ---------- #

def _leveldb_dirs(context):
    dirs = {}
    for f in context.get_files_found():
        f = str(f)
        parent = os.path.dirname(f)
        if os.path.basename(parent).endswith(".indexeddb.leveldb"):
            dirs.setdefault(os.path.realpath(parent), parent)
    return list(dirs.values())


def _account_uuid(db_name):
    m = _DBNAME_UUID_RE.search(db_name or "")
    return m.group(1) if m else None


def _completeness(v):
    return sum(1 for x in v.values() if x not in (None, "", [], {})) if isinstance(v, dict) else 0


def _dedupe_by_id(records):
    best, order = {}, []
    for rec in records:
        v = rec.get("value")
        if not isinstance(v, dict):
            continue
        ident = v.get("id", rec.get("key"))
        if ident not in best:
            order.append(ident)
            best[ident] = rec
        elif _completeness(v) > _completeness(best[ident]["value"]):
            best[ident] = rec
    return [best[i] for i in order]


def _build_users(stores):
    users = {}
    for rec in _dedupe_by_id(stores.get("users", [])):
        v = rec["value"]
        if isinstance(v, dict) and v.get("id"):
            users[v["id"]] = v
    return users


def _self_user_ids(stores):
    ids = set()
    for rec in stores.get("clients", []) + stores.get("conversations", []) + stores.get("users", []):
        uid = _account_uuid(rec.get("db_name"))
        if uid:
            ids.add(uid)
    for rec in stores.get("mls_credentials", []):
        m = _MLS_CRED_RE.search(str(rec.get("key") or ""))
        if m:
            ids.add(m.group(1))
    return ids


def _display_name(users, uid, self_ids):
    if not uid:
        return ""
    u = users.get(uid) or {}
    name = u.get("name") or u.get("handle") or uid
    return f"{name} (me)" if uid in self_ids else name


def _account_label(users, self_ids, db_name):
    uid = _account_uuid(db_name)
    if not uid:
        return ""
    u = users.get(uid) or {}
    return f"@{u['handle']}" if u.get("handle") else uid


def _conv_names(stores, users, self_ids):
    names = {}
    for rec in _dedupe_by_id(stores.get("conversations", [])):
        v = rec["value"]
        cid = v.get("id")
        if not cid:
            continue
        name = v.get("name")
        if not name:
            parts = set((v.get("roles") or {}).keys())
            for o in v.get("others") or []:
                if isinstance(o, dict) and o.get("id"):
                    parts.add(o["id"])
                elif isinstance(o, str):
                    parts.add(o)
            name = ", ".join(sorted(
                _display_name(users, p, self_ids) for p in parts
                if p and p not in self_ids)) or cid
        names[cid] = name
    return names


def _iso_to_dt(value):
    if not value or not isinstance(value, str):
        return value
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.astimezone(timezone.utc) if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return value


@artifact_processor
def wireRecoveredMedia(context):
    # Recovered Media image is the 5th column so it shows when the report opens.
    data_headers = (
        ("Timestamp", "datetime"), "Account", "Conversation", "Sender",
        ("Recovered Media", "media"), "Filename", "Content Type", "Kind",
        "Asset ID", "Decrypted Size", "SHA-256 Verified", "Cache Source",
        "Message ID",
    )

    if not crypto_available():
        logfunc("Wire Recovered Media: PyCryptodome not available; skipping.")
        return data_headers, [], ""

    dirs = _leveldb_dirs(context)
    stores = {}
    for d in dirs:
        try:
            for store, recs in load_indexeddb(d, log=None).items():
                stores.setdefault(store, []).extend(recs)
        except Exception as ex:  # pragma: no cover - defensive
            logfunc(f"Wire Recovered Media: could not parse '{d}': {ex}")
    if not stores:
        return data_headers, [], ""

    users = _build_users(stores)
    self_ids = _self_user_ids(stores)
    conv_names = _conv_names(stores, users, self_ids)

    by_sha = build_asset_index(stores)
    recovered = recover_assets(context.get_files_found(), by_sha)

    data_list = []
    for asset_id, desc in recovered.items():
        name = desc["name"] or f"{asset_id}.{desc['ext']}"
        media_ref = check_in_embedded_media(
            desc["source"], desc["plain"], name,
            force_type=desc["ctype"], force_extension=desc["ext"])
        data_list.append((
            _iso_to_dt(desc["time"]),
            _account_label(users, self_ids, desc["db_name"]),
            conv_names.get(desc["conv"], desc["conv"] or ""),
            _display_name(users, desc["from_id"], self_ids),
            media_ref,
            name,
            desc["ctype"],
            desc["kind"],
            asset_id,
            len(desc["plain"]),
            "Yes",
            os.path.basename(desc["source"]),
            desc["event_id"] or "",
        ))

    data_list.sort(key=lambda r: (r[0] if isinstance(r[0], datetime)
                                  else datetime.min.replace(tzinfo=timezone.utc)))
    logfunc(f"Wire Recovered Media: decrypted {len(data_list)} cached asset(s).")
    return data_headers, data_list, (dirs[0] if dirs else "")

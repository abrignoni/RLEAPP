__artifacts_v2__ = {
    "wireRecoveredMedia": {
        "name": "Wire Recovered Media",
        "description": "Actual images/media recovered by decrypting the Wire "
                       "service-worker cached asset blobs with the per-asset keys "
                       "stored in the IndexedDB asset-add events. Each cached "
                       "blob is matched to its event by SHA-256, integrity-"
                       "verified, then AES-256-CBC decrypted with the event "
                       "otr_key. The decrypted files are embedded in the report.",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-07-23",
        "last_update_date": "2026-07-23",
        "requirements": "PyCryptodome",
        "category": "Wire",
        "notes": "Only assets still present in the on-disk service-worker cache "
                 "can be recovered. Decryption follows Wire's asset scheme: "
                 "blob = IV(16) || AES-256-CBC ciphertext, SHA-256 over the blob.",
        "paths": (
            '*/https_app.wire.com_0.indexeddb.leveldb/*',
            '*/Service Worker/CacheStorage/*/*/*_0',
        ),
        "output_types": ["html", "tsv", "lava"],
        "artifact_icon": "image",
    },
}

import hashlib
import os
import re
import struct
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, logfunc, check_in_embedded_media
from scripts.ccl.indexeddb_to_json import load_indexeddb

try:
    from Crypto.Cipher import AES
except ImportError:  # pragma: no cover
    AES = None

_DBNAME_UUID_RE = re.compile(r"@([0-9a-f]{8}-[0-9a-f-]{27,})@")
_MLS_CRED_RE = re.compile(r"([0-9a-f-]{36}):([0-9a-f]+)@")
_ASSET_ID_RE = re.compile(rb"/assets/[^/]+/([0-9]+-[0-9]+-[0-9a-f-]{36})")
# Chromium Simple Cache end-of-stream marker.
_EOF_MAGIC = struct.pack("<Q", 0xF4FA6F45970D41D8)


# --------------------------------------------------------------------------- #
# IndexedDB helpers (self-contained; mirrors wireIndexedDb.py resolvers)
# --------------------------------------------------------------------------- #

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


def _iso_to_dt(value):
    if not value or not isinstance(value, str):
        return value
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.astimezone(timezone.utc) if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return value


# --------------------------------------------------------------------------- #
# Simple Cache body extraction + Wire asset decryption
# --------------------------------------------------------------------------- #

def _candidate_bodies(data):
    """Yield candidate response-body byte ranges from a Simple Cache entry."""
    if len(data) < 20:
        return
    klen = struct.unpack_from("<I", data, 12)[0]
    eofs, idx = [], 0
    while True:
        e = data.find(_EOF_MAGIC, idx)
        if e < 0:
            break
        eofs.append(e)
        idx = e + 8
    # Preferred: each EOF record carries the preceding stream's size.
    for e in eofs:
        if e + 24 <= len(data):
            size = struct.unpack_from("<q", data, e + 16)[0]
            if 0 < size <= e:
                yield data[e - size:e]
    # Fallback: header + key (+4) up to the first EOF.
    if eofs:
        start = 20 + klen + 4
        if 0 < start < eofs[0]:
            yield data[start:eofs[0]]


def _pkcs7_unpad(b):
    if not b:
        return b
    p = b[-1]
    return b[:-p] if 1 <= p <= 16 and b[-p:] == bytes([p]) * p else b


def _sniff(plain):
    """Return (content_type, extension) from magic bytes, else ('', '')."""
    if plain.startswith(b"\xff\xd8\xff"):
        return "image/jpeg", "jpg"
    if plain.startswith(b"\x89PNG"):
        return "image/png", "png"
    if plain.startswith(b"GIF8"):
        return "image/gif", "gif"
    if plain[:4] == b"RIFF" and plain[8:12] == b"WEBP":
        return "image/webp", "webp"
    if plain[4:8] == b"ftyp":
        return "video/mp4", "mp4"
    return "", ""


def _asset_index(stores):
    """Map sha256(hex of encrypted blob) -> asset descriptor from asset events."""
    idx = {}
    for rec in stores.get("events", []):
        v = rec.get("value")
        if not isinstance(v, dict) or v.get("type") != "conversation.asset-add":
            continue
        d = v.get("data") or {}
        base = {
            "db_name": rec.get("db_name"),
            "from_id": v.get("from"),
            "conv": v.get("conversation"),
            "time": v.get("time"),
            "event_id": v.get("id"),
        }
        if d.get("otr_key") and d.get("sha256"):
            idx[bytes(d["sha256"]).hex()] = {
                **base, "otr": bytes(d["otr_key"]), "kind": "full",
                "asset_id": d.get("key"), "ctype": d.get("content_type") or "",
                "name": (d.get("info") or {}).get("name") or "",
            }
        if d.get("preview_otr_key") and d.get("preview_sha256"):
            idx[bytes(d["preview_sha256"]).hex()] = {
                **base, "otr": bytes(d["preview_otr_key"]), "kind": "preview",
                "asset_id": d.get("preview_key"), "ctype": "image/jpeg", "name": "",
            }
    return idx


@artifact_processor
def wireRecoveredMedia(context):
    data_headers = (
        ("Timestamp", "datetime"), "Account", "Conversation", "Sender",
        "Filename", "Content Type", "Kind", "Asset ID", ("Recovered Media", "media"),
        "Decrypted Size", "SHA-256 Verified", "Cache Entry", "Message ID",
    )

    if AES is None:
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
    conv_names = {}
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
        conv_names[cid] = name
    by_sha = _asset_index(stores)

    data_list = []
    source_path = dirs[0] if dirs else ""
    seen = set()

    for f in context.get_files_found():
        f = str(f)
        if not f.endswith("_0"):
            continue
        try:
            raw = open(f, "rb").read()
        except OSError:
            continue
        if b"wire.com" not in raw:
            continue

        matched = None
        for body in _candidate_bodies(raw):
            sha = hashlib.sha256(body).hexdigest()
            if sha in by_sha:
                matched = (sha, body)
                break
        if not matched:
            continue
        sha, blob = matched
        if sha in seen:
            continue
        seen.add(sha)
        info = by_sha[sha]

        try:
            cipher = AES.new(info["otr"], AES.MODE_CBC, blob[:16])
            plain = _pkcs7_unpad(cipher.decrypt(blob[16:]))
        except (ValueError, KeyError) as ex:
            logfunc(f"Wire Recovered Media: decrypt failed for {info.get('asset_id')}: {ex}")
            continue

        ctype, ext = _sniff(plain)
        ctype = ctype or info["ctype"] or "application/octet-stream"
        if not ext:
            ext = {"image/jpeg": "jpg", "image/png": "png",
                   "video/mp4": "mp4"}.get(info["ctype"], "bin")
        name = info["name"] or f"{info['asset_id']}.{ext}"

        media_ref = check_in_embedded_media(
            f, plain, name, force_type=ctype, force_extension=ext)

        data_list.append((
            _iso_to_dt(info["time"]),
            _account_label(users, self_ids, info["db_name"]),
            conv_names.get(info["conv"], info["conv"] or ""),
            _display_name(users, info["from_id"], self_ids),
            name,
            ctype,
            info["kind"],
            info["asset_id"] or "",
            media_ref,
            len(plain),
            "Yes",
            os.path.basename(f),
            info["event_id"] or "",
        ))

    logfunc(f"Wire Recovered Media: decrypted {len(data_list)} cached asset(s).")
    return data_headers, data_list, source_path

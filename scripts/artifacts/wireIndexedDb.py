__artifacts_v2__ = {
    "wireAccountInfo": {
        "name": "Wire Account Info",
        "description": "Signed-in Wire account owner(s) recovered from the "
                       "app.wire.com IndexedDB/LevelDB store: handle, display "
                       "name, user id, self device (client) and registration "
                       "details. One LevelDB can hold more than one login.",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-07-23",
        "last_update_date": "2026-07-23",
        "requirements": "none",
        "category": "Wire",
        "notes": "Parses https_app.wire.com_0.indexeddb.leveldb via the vendored "
                 "CCL Chromium IndexedDB reader and Spyder Forensics IndexedDBtoJSON logic.",
        "paths": ('*/https_app.wire.com_0.indexeddb.leveldb/*',),
        "output_types": ["html", "tsv", "timeline", "lava"],
        "artifact_icon": "user",
    },
    "wireUsers": {
        "name": "Wire Users",
        "description": "All Wire users (self and contacts) known to the client: "
                       "user id, handle, display name, email, phone, domain, team "
                       "and profile-picture asset keys.",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-07-23",
        "last_update_date": "2026-07-23",
        "requirements": "none",
        "category": "Wire",
        "notes": "",
        "paths": ('*/https_app.wire.com_0.indexeddb.leveldb/*',),
        "output_types": ["html", "tsv", "timeline", "lava"],
        "artifact_icon": "users",
    },
    "wireDevices": {
        "name": "Wire Devices",
        "description": "Wire clients (devices) recorded in the IndexedDB clients "
                       "store: the local device for each signed-in account plus "
                       "known devices, with model, class, registration time, last "
                       "active and verification state.",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-07-23",
        "last_update_date": "2026-07-23",
        "requirements": "none",
        "category": "Wire",
        "notes": "",
        "paths": ('*/https_app.wire.com_0.indexeddb.leveldb/*',),
        "output_types": ["html", "tsv", "timeline", "lava"],
        "artifact_icon": "smartphone",
    },
    "wireConversations": {
        "name": "Wire Conversations",
        "description": "Wire conversations: id, name, type, protocol, creator, "
                       "team, resolved participants, archived/muted state.",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-07-23",
        "last_update_date": "2026-07-23",
        "requirements": "none",
        "category": "Wire",
        "notes": "",
        "paths": ('*/https_app.wire.com_0.indexeddb.leveldb/*',),
        "output_types": ["html", "tsv", "timeline", "lava"],
        "artifact_icon": "message-square",
    },
    "wireMessages": {
        "name": "Wire Messages",
        "description": "Wire conversation events flattened to a message timeline: "
                       "text messages, pings, attachments, member joins and "
                       "conversation creations, with resolved sender and "
                       "conversation names.",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-07-23",
        "last_update_date": "2026-07-23",
        "requirements": "none",
        "category": "Wire",
        "notes": "",
        "paths": ('*/https_app.wire.com_0.indexeddb.leveldb/*',),
        "output_types": ["html", "tsv", "timeline", "lava"],
        "artifact_icon": "message-circle",
        "data_views": {
            "conversation": {
                "conversationDiscriminatorColumn": "Conversation ID",
                "conversationLabelColumn": "Conversation",
                "textColumn": "Message",
                "directionColumn": "Outgoing",
                "directionSentValue": 1,
                "timeColumn": "Timestamp",
                "senderColumn": "Sender",
                "mediaColumn": "Attachment",
            }
        },
    },
    "wireAttachments": {
        "name": "Wire Attachments",
        "description": "Files, images, audio and video shared in Wire "
                       "conversations (asset-add events): filename, MIME type, "
                       "size, sender, conversation and the server asset "
                       "key/token references.",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-07-23",
        "last_update_date": "2026-07-23",
        "requirements": "none",
        "category": "Wire",
        "notes": "Wire assets are end-to-end encrypted and stored server-side; "
                 "only metadata and asset references are present locally.",
        "paths": ('*/https_app.wire.com_0.indexeddb.leveldb/*',),
        "output_types": ["html", "tsv", "timeline", "lava"],
        "artifact_icon": "paperclip",
    },
    "wireCachedAssets": {
        "name": "Wire Cached Assets",
        "description": "Asset URLs recorded in the Wire service-worker cache "
                       "(workbox cache-entries): the remote asset URL and the "
                       "time it was cached.",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-07-23",
        "last_update_date": "2026-07-23",
        "requirements": "none",
        "category": "Wire",
        "notes": "",
        "paths": ('*/https_app.wire.com_0.indexeddb.leveldb/*',),
        "output_types": ["html", "tsv", "timeline", "lava"],
        "artifact_icon": "link",
    },
    "wireBlacklistedConversations": {
        "name": "Wire Blacklisted Conversations",
        "description": "Conversations recorded in the Wire conversationBlacklist "
                       "store, resolved to a name where possible.",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-07-23",
        "last_update_date": "2026-07-23",
        "requirements": "none",
        "category": "Wire",
        "notes": "",
        "paths": ('*/https_app.wire.com_0.indexeddb.leveldb/*',),
        "output_types": ["html", "tsv", "timeline", "lava"],
        "artifact_icon": "slash",
    },
    "wireKeyMaterialInventory": {
        "name": "Wire Key Material Inventory",
        "description": "Inventory (counts only) of the cryptographic key-material "
                       "stores in the Wire IndexedDB (Proteus/MLS/CoreCrypto). No "
                       "private key bytes are exported.",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-07-23",
        "last_update_date": "2026-07-23",
        "requirements": "none",
        "category": "Wire",
        "notes": "Metadata only. Presence and counts of key stores, not the keys.",
        "paths": ('*/https_app.wire.com_0.indexeddb.leveldb/*',),
        "output_types": ["html", "tsv", "lava"],
        "artifact_icon": "key",
    },
}

import os
import re
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, logfunc
from scripts.ccl.indexeddb_to_json import load_indexeddb


# --------------------------------------------------------------------------- #
# Reference data
# --------------------------------------------------------------------------- #

# Wire conversation "type" enum -> human label.
CONV_TYPE = {
    0: "Group / regular",
    1: "Self",
    2: "One-to-one (connect)",
    3: "One-to-one",
    4: "Connect (pending)",
    5: "Global team",
}

# Stores that hold private cryptographic key material (inventoried, never dumped).
CRYPTO_STORES = (
    "secrets", "keys", "prekeys", "sessions",
    "mls_credentials", "mls_signature_keypairs", "mls_hpke_private_keys",
    "mls_encryption_keypairs", "mls_epoch_encryption_keypairs", "mls_psk_bundles",
    "mls_keypackages", "mls_groups", "mls_pending_groups", "mls_pending_messages",
    "mls_buffered_commits", "proteus_prekeys", "proteus_identities",
    "proteus_sessions", "e2ei_enrollment", "e2ei_refresh_token", "e2ei_acme_ca",
    "e2ei_intermediate_certs", "e2ei_crls", "crls", "_encryptionSettings",
    "group_ids", "pending_proposals", "pendingProposals", "subconversations",
    "last_key_material_update_dates", "pendingEnrollmentData", "consumer_data",
)

# db name looks like "wire@production@<uuid>@permanent" or
# "core-wire@production@<uuid>@permanent"; the uuid is the account owner.
_DBNAME_UUID_RE = re.compile(r"@([0-9a-f]{8}-[0-9a-f-]{27,})@")
_MLS_CRED_RE = re.compile(r"([0-9a-f-]{36}):([0-9a-f]+)@")
# Object-store keys are serialized as "<IdbKey ...>" by the CCL reader.
_IDBKEY_RE = re.compile(r"^<IdbKey (.+)>$", re.DOTALL)

# Cache one parse per LevelDB directory for the whole run.
_PARSE_CACHE = {}


# --------------------------------------------------------------------------- #
# Loading / small helpers
# --------------------------------------------------------------------------- #

def _leveldb_dirs(context):
    """Distinct leveldb directories reconstructed from the copied files."""
    dirs = {}
    for file_found in context.get_files_found():
        file_found = str(file_found)
        parent = os.path.dirname(file_found)
        if os.path.basename(parent).endswith(".indexeddb.leveldb"):
            dirs.setdefault(os.path.realpath(parent), parent)
    return list(dirs.values())


def _load(context):
    """Parse every Wire leveldb folder found, merge stores, cache per run.

    Returns (stores, source_dirs). ``stores`` maps object-store name to a list
    of records ``{db_name, db_number, origin, key, value}`` across all folders.
    """
    dirs = _leveldb_dirs(context)
    key = tuple(sorted(os.path.realpath(d) for d in dirs))
    if key in _PARSE_CACHE:
        return _PARSE_CACHE[key], dirs

    merged = {}
    for d in dirs:
        try:
            stores = load_indexeddb(d, log=None)
        except Exception as ex:  # pragma: no cover - defensive
            logfunc(f"Wire: could not parse LevelDB '{d}': {ex}")
            continue
        for store, records in stores.items():
            merged.setdefault(store, []).extend(records)

    _PARSE_CACHE[key] = merged
    return merged, dirs


def _source(context, dirs):
    return "\n".join(context.get_relative_path(d) for d in dirs)


def _iso_to_dt(value):
    """Parse a Wire ISO-8601 timestamp string to an aware UTC datetime."""
    if not value or not isinstance(value, str):
        return value
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except (ValueError, TypeError):
        return value


def _ms_to_dt(value):
    """Parse an epoch-milliseconds number to an aware UTC datetime."""
    try:
        return datetime.fromtimestamp(float(value) / 1000.0, tz=timezone.utc)
    except (ValueError, TypeError, OSError, OverflowError):
        return value


def _clean_key(raw):
    """Strip the '<IdbKey ...>' wrapper the CCL reader puts on serialized keys."""
    if not isinstance(raw, str):
        return raw
    m = _IDBKEY_RE.match(raw.strip())
    return m.group(1).strip() if m else raw


def _account_uuid(db_name):
    m = _DBNAME_UUID_RE.search(db_name or "")
    return m.group(1) if m else None


def _completeness(value):
    if not isinstance(value, dict):
        return 0
    return sum(1 for v in value.values() if v not in (None, "", [], {}))


def _dedupe_by_id(records, id_field="id"):
    """Keep the most complete record per value[id_field] (LevelDB keeps history).

    Returns list of (record, value) preserving first-seen order.
    """
    best = {}
    order = []
    for rec in records:
        val = rec.get("value")
        if not isinstance(val, dict):
            continue
        ident = val.get(id_field, rec.get("key"))
        if ident not in best:
            order.append(ident)
            best[ident] = rec
        elif _completeness(val) > _completeness(best[ident].get("value")):
            best[ident] = rec
    return [(best[i], best[i]["value"]) for i in order]


# --------------------------------------------------------------------------- #
# Cross-referencing (users, self identities, account labels)
# --------------------------------------------------------------------------- #

def _build_users(stores):
    """{user_id: value(dict, richest)} for the users store."""
    users = {}
    for _rec, v in _dedupe_by_id(stores.get("users", [])):
        uid = v.get("id")
        if uid:
            users[uid] = v
    return users


def _self_user_ids(stores):
    """Every account-owner user id represented in the dump."""
    ids = set()
    for rec in stores.get("clients", []) + stores.get("conversations", []) \
            + stores.get("users", []):
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
    """Friendly label for the account that owns a given database."""
    uid = _account_uuid(db_name)
    if not uid:
        return ""
    u = users.get(uid) or {}
    handle = u.get("handle")
    if handle:
        return f"@{handle}"
    return uid


def _domain_of(value):
    q = value.get("qualified_id")
    if isinstance(q, dict) and q.get("domain"):
        return q.get("domain")
    return value.get("domain")


# --------------------------------------------------------------------------- #
# Artifacts
# --------------------------------------------------------------------------- #

@artifact_processor
def wireAccountInfo(context):
    stores, dirs = _load(context)
    users = _build_users(stores)
    self_ids = _self_user_ids(stores)

    # Map self client-id -> local_identity client record (per account db).
    local_clients = {}
    for rec in stores.get("clients", []):
        if _clean_key(rec.get("key")) == "local_identity" and isinstance(rec.get("value"), dict):
            uid = _account_uuid(rec.get("db_name"))
            v = rec["value"]
            # keep the richest local_identity per account
            if uid not in local_clients or _completeness(v) > _completeness(local_clients[uid]["value"]):
                local_clients[uid] = rec

    # client-id per account from mls_credentials keys
    cred_clients = {}
    for rec in stores.get("mls_credentials", []):
        m = _MLS_CRED_RE.search(str(rec.get("key") or ""))
        if m:
            cred_clients.setdefault(m.group(1), m.group(2))

    data_list = []
    for uid in sorted(self_ids):
        u = users.get(uid, {})
        rec = local_clients.get(uid)
        c = rec["value"] if rec else {}
        client_id = c.get("id") or cred_clients.get(uid, "")
        data_list.append((
            f"@{u.get('handle')}" if u.get("handle") else "",
            u.get("name", ""),
            uid,
            client_id,
            c.get("model", ""),
            c.get("label", ""),
            c.get("class", ""),
            c.get("type", ""),
            _iso_to_dt(c.get("time")),
            _iso_to_dt(c.get("last_active")),
            (c.get("meta") or {}).get("is_verified"),
            u.get("email", ""),
            _domain_of(u) or "",
            u.get("team", ""),
            ", ".join(u.get("supported_protocols") or []),
        ))

    data_headers = (
        "Handle", "Display Name", "User ID", "Local Client (Device) ID",
        "Device Model", "Device Label", "Device Class", "Device Type",
        ("Device Registered", "datetime"), ("Device Last Active", "datetime"),
        "Device Verified", "Email", "Domain", "Team ID", "Supported Protocols",
    )
    return data_headers, data_list, _source(context, dirs)


@artifact_processor
def wireUsers(context):
    stores, dirs = _load(context)
    users = _build_users(stores)
    self_ids = _self_user_ids(stores)

    data_list = []
    for uid, v in users.items():
        assets = v.get("assets") or []
        asset_keys = ", ".join(a.get("key", "") for a in assets if isinstance(a, dict))
        data_list.append((
            "Yes" if uid in self_ids else "",
            v.get("name", ""),
            f"@{v.get('handle')}" if v.get("handle") else "",
            uid,
            v.get("email", ""),
            v.get("phone", ""),
            _domain_of(v) or "",
            v.get("team", ""),
            v.get("accent_id", ""),
            ", ".join(v.get("supported_protocols") or []),
            v.get("legalhold_status", ""),
            asset_keys,
        ))

    data_headers = (
        "Is Account Owner", "Display Name", "Handle", "User ID", "Email",
        ("Phone", "phonenumber"), "Domain", "Team ID", "Accent Id",
        "Supported Protocols", "Legal Hold Status", "Profile Picture Asset Keys",
    )
    return data_headers, data_list, _source(context, dirs)


@artifact_processor
def wireDevices(context):
    stores, dirs = _load(context)
    users = _build_users(stores)
    self_ids = _self_user_ids(stores)

    data_list = []
    seen = set()
    for rec in stores.get("clients", []):
        v = rec.get("value")
        if not isinstance(v, dict):
            continue
        pk = _clean_key(rec.get("key"))
        cid = v.get("id")
        sig = (rec.get("db_name"), pk, cid)
        if sig in seen:
            continue
        seen.add(sig)
        mls_keys = v.get("mls_public_keys") or {}
        data_list.append((
            _account_label(users, self_ids, rec.get("db_name")),
            "Yes" if pk == "local_identity" else "",
            cid or "",
            v.get("model", ""),
            v.get("label", ""),
            v.get("class", ""),
            v.get("type", ""),
            _iso_to_dt(v.get("time")),
            _iso_to_dt(v.get("last_active")),
            (v.get("meta") or {}).get("is_verified"),
            v.get("domain") or "",
            ", ".join(sorted(mls_keys.keys())) if isinstance(mls_keys, dict) else "",
            ", ".join(v.get("capabilities") or []),
        ))

    data_headers = (
        "Account", "Local Device", "Client (Device) ID", "Model", "Label",
        "Class", "Type", ("Registered", "datetime"), ("Last Active", "datetime"),
        "Verified", "Domain", "MLS Public Key Types", "Capabilities",
    )
    return data_headers, data_list, _source(context, dirs)


@artifact_processor
def wireConversations(context):
    stores, dirs = _load(context)
    users = _build_users(stores)
    self_ids = _self_user_ids(stores)

    data_list = []
    for rec, v in _dedupe_by_id(stores.get("conversations", [])):
        cid = v.get("id")
        if not cid:
            continue
        participants = set()
        if isinstance(v.get("roles"), dict):
            participants.update(v["roles"].keys())
        for o in v.get("others") or []:
            if isinstance(o, str):
                participants.add(o)
            elif isinstance(o, dict) and o.get("id"):
                participants.add(o["id"])
        if v.get("creator"):
            participants.add(v["creator"])
        part_names = sorted(_display_name(users, p, self_ids) for p in participants)

        data_list.append((
            _account_label(users, self_ids, rec.get("db_name")),
            v.get("name") or "",
            CONV_TYPE.get(v.get("type"), f"Type {v.get('type')}"),
            v.get("protocol", ""),
            _display_name(users, v.get("creator"), self_ids),
            ", ".join(part_names),
            len(participants),
            "Yes" if v.get("archived_state") else "",
            "Yes" if v.get("muted_state") else "",
            v.get("team_id") or "",
            cid,
            v.get("group_id") or "",
            v.get("domain") or "",
        ))

    data_headers = (
        "Account", "Name", "Type", "Protocol", "Creator", "Participants",
        "Participant Count", "Archived", "Muted", "Team ID",
        "Conversation ID", "Group ID", "Domain",
    )
    return data_headers, data_list, _source(context, dirs)


def _event_text(etype, d, users, self_ids):
    """Return (kind, message_text, attachment_name) for an event."""
    if etype == "conversation.message-add":
        text = d.get("content")
        if d.get("mentions"):
            text = f"{text}  [mentions: {len(d['mentions'])}]"
        return "message", text, ""
    if etype == "conversation.asset-add":
        info = d.get("info") or {}
        name = info.get("name", "")
        label = f"[{d.get('content_type', 'file')}] {name}".strip()
        if d.get("content_length"):
            try:
                label += f" ({int(d['content_length'])} bytes)"
            except (ValueError, TypeError):
                pass
        return "asset", label, name
    if etype == "conversation.knock":
        return "ping", "\U0001F44B ping", ""
    if etype == "conversation.member-join":
        joined = d.get("user_ids") or [
            u.get("id") for u in d.get("users", []) if isinstance(u, dict)]
        return "member-join", "joined: " + ", ".join(
            _display_name(users, u, self_ids) for u in joined), ""
    if etype == "conversation.member-leave":
        left = d.get("user_ids") or []
        return "member-leave", "left: " + ", ".join(
            _display_name(users, u, self_ids) for u in left), ""
    if etype in ("conversation.one2one-creation", "conversation.group-creation"):
        return "conversation-created", d.get("name") or "(conversation created)", ""
    return etype, d.get("content") or "", ""


@artifact_processor
def wireMessages(context):
    stores, dirs = _load(context)
    users = _build_users(stores)
    self_ids = _self_user_ids(stores)

    # conversation id -> friendly name
    conv_names = {}
    for _rec, v in _dedupe_by_id(stores.get("conversations", [])):
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
            parts.discard(None)
            name = ", ".join(sorted(
                _display_name(users, p, self_ids) for p in parts
                if p not in self_ids)) or cid
        conv_names[cid] = name

    rows = []
    for rec in stores.get("events", []):
        v = rec.get("value")
        if not isinstance(v, dict):
            continue
        d = v.get("data") or {}
        etype = v.get("type")
        kind, text, attachment = _event_text(etype, d, users, self_ids)
        sender_id = v.get("from") or ""
        cid = v.get("conversation") or ""
        rows.append((
            _iso_to_dt(v.get("time")),
            _account_label(users, self_ids, rec.get("db_name")),
            conv_names.get(cid, cid),
            _display_name(users, sender_id, self_ids),
            1 if sender_id in self_ids else 0,
            kind,
            text or "",
            attachment,
            v.get("id", ""),
            sender_id,
            cid,
            v.get("status", ""),
        ))

    rows.sort(key=lambda r: (r[0] if isinstance(r[0], datetime)
                             else datetime.min.replace(tzinfo=timezone.utc)))

    data_headers = (
        ("Timestamp", "datetime"), "Account", "Conversation", "Sender",
        "Outgoing", "Message Type", "Message", "Attachment", "Message ID",
        "Sender ID", "Conversation ID", "Status",
    )
    return data_headers, rows, _source(context, dirs)


@artifact_processor
def wireAttachments(context):
    stores, dirs = _load(context)
    users = _build_users(stores)
    self_ids = _self_user_ids(stores)

    conv_names = {}
    for _rec, v in _dedupe_by_id(stores.get("conversations", [])):
        if v.get("id"):
            conv_names[v["id"]] = v.get("name") or v["id"]

    data_list = []
    for rec in stores.get("events", []):
        v = rec.get("value")
        if not isinstance(v, dict) or v.get("type") != "conversation.asset-add":
            continue
        d = v.get("data") or {}
        info = d.get("info") or {}
        size = d.get("content_length")
        try:
            size = int(size) if size is not None else ""
        except (ValueError, TypeError):
            pass
        cid = v.get("conversation") or ""
        data_list.append((
            _iso_to_dt(v.get("time")),
            _account_label(users, self_ids, rec.get("db_name")),
            conv_names.get(cid, cid),
            _display_name(users, v.get("from"), self_ids),
            info.get("name", ""),
            d.get("content_type", ""),
            size,
            d.get("key", ""),
            d.get("token", "") or d.get("asset_token", ""),
            d.get("domain", ""),
            "Yes" if d.get("otr_key") else "",
            "Yes" if d.get("sha256") else "",
            v.get("id", ""),
            cid,
        ))

    data_headers = (
        ("Timestamp", "datetime"), "Account", "Conversation", "Sender",
        "Filename", "Content Type", "Size (bytes)", "Asset Key", "Asset Token",
        "Asset Domain", "Encrypted (OTR key)", "SHA-256 present", "Message ID",
        "Conversation ID",
    )
    return data_headers, data_list, _source(context, dirs)


@artifact_processor
def wireCachedAssets(context):
    stores, dirs = _load(context)

    data_list = []
    seen = set()
    for rec in stores.get("cache-entries", []):
        v = rec.get("value")
        if not isinstance(v, dict):
            continue
        url = v.get("url", "")
        ts = v.get("timestamp")
        sig = (url, ts)
        if sig in seen:
            continue
        seen.add(sig)
        data_list.append((
            _ms_to_dt(ts),
            v.get("cacheName", ""),
            url,
        ))

    data_headers = (("Cached", "datetime"), "Cache Name", "Asset URL")
    return data_headers, data_list, _source(context, dirs)


@artifact_processor
def wireBlacklistedConversations(context):
    stores, dirs = _load(context)
    users = _build_users(stores)
    self_ids = _self_user_ids(stores)

    conv_names = {}
    for _rec, v in _dedupe_by_id(stores.get("conversations", [])):
        if v.get("id"):
            conv_names[v["id"]] = v.get("name") or ""

    data_list = []
    seen = set()
    for rec in stores.get("conversationBlacklist", []):
        v = rec.get("value")
        if not isinstance(v, dict):
            continue
        cid = v.get("id")
        if cid in seen:
            continue
        seen.add(cid)
        data_list.append((
            _account_label(users, self_ids, rec.get("db_name")),
            cid or "",
            v.get("domain", ""),
            conv_names.get(cid, ""),
        ))

    data_headers = ("Account", "Conversation ID", "Domain", "Known Name")
    return data_headers, data_list, _source(context, dirs)


@artifact_processor
def wireKeyMaterialInventory(context):
    stores, dirs = _load(context)

    data_list = []
    for store in CRYPTO_STORES:
        recs = stores.get(store, [])
        if recs:
            data_list.append((store, len(recs)))

    data_headers = ("Key-Material Store", "Record Count")
    return data_headers, data_list, _source(context, dirs)

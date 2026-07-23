__artifacts_v2__ = {
    "wireServiceWorkerCache": {
        "name": "Wire Service Worker Cache",
        "description": "Assets cached on disk by the Wire web app's service "
                       "worker (Service Worker/CacheStorage). Each entry records "
                       "the requested asset URL, the resolved CDN (CloudFront) "
                       "download URL and its expiry. The cached bodies are Wire "
                       "end-to-end-encrypted (application/octet-stream), so they "
                       "cannot be rendered as images without the asset keys.",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-07-23",
        "last_update_date": "2026-07-23",
        "requirements": "none",
        "category": "Wire",
        "notes": "Parses Chromium Simple Cache entry files (*_0). Bodies remain "
                 "encrypted; only request/CDN URLs and metadata are extracted.",
        "paths": ('*/Service Worker/CacheStorage/*/*/*_0',),
        "output_types": ["html", "tsv", "timeline", "lava"],
        "artifact_icon": "hard-drive",
    },
}

import os
import re
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor

# RFC 3986 URL characters, so a match stops at the first binary byte that
# follows the URL inside the Simple Cache entry.
_URLSAFE = r"[A-Za-z0-9\-._~:/?#\[\]@!$&'()*+,;=%]"
_ASSET_URL_RE = re.compile(r"https://" + _URLSAFE + r"+/assets/" + _URLSAFE + r"+")
_CDN_URL_RE = re.compile(r"https://prod-assets\.wire\.com/" + _URLSAFE + r"+")
_ANY_WIRE_URL_RE = re.compile(r"https://" + _URLSAFE + r"*wire\.com" + _URLSAFE + r"*")
_ASSET_ID_RE = re.compile(r"/assets/[^/]+/([0-9]+-[0-9]+-[0-9a-f-]{36})")
_EXPIRES_RE = re.compile(r"[?&]Expires=(\d+)")
_CTYPE_RE = re.compile(r"\b((?:application|image|video|audio|text)/[A-Za-z0-9.+\-]+)")
# CloudFront key-pair ids are upper-case alphanumeric; trim trailing cache bytes.
_KEYPAIR_TRIM_RE = re.compile(r"(Key-Pair-Id=[A-Z0-9]+).*$")


def _unix_to_dt(value):
    try:
        return datetime.fromtimestamp(int(value), tz=timezone.utc)
    except (ValueError, TypeError, OSError, OverflowError):
        return ""


@artifact_processor
def wireServiceWorkerCache(context):
    data_list = []
    source_path = ""
    parsed = set()

    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith("_0"):
            continue
        real = os.path.realpath(file_found)
        if real in parsed:
            continue
        parsed.add(real)

        try:
            with open(file_found, "rb") as fh:
                raw = fh.read()
        except OSError:
            continue
        if b"wire.com" not in raw:
            continue

        text = raw.decode("latin1", "replace")
        req = _ASSET_URL_RE.search(text)
        req_url = req.group(0) if req else ""
        if not req_url:
            any_url = _ANY_WIRE_URL_RE.search(text)
            req_url = any_url.group(0) if any_url else ""
        if not req_url:
            continue

        cdn = _CDN_URL_RE.search(text)
        cdn_url = cdn.group(0) if cdn else ""
        if cdn_url:
            cdn_url = _KEYPAIR_TRIM_RE.sub(r"\1", cdn_url)
        aid = _ASSET_ID_RE.search(req_url)
        expires = ""
        if cdn_url:
            em = _EXPIRES_RE.search(cdn_url)
            if em:
                expires = _unix_to_dt(em.group(1))
        # content type of the cached response (excluding the request Accept header)
        ctypes = [c for c in _CTYPE_RE.findall(text) if c != "application/json"]
        ctype = ctypes[0] if ctypes else ""

        source_path = file_found
        data_list.append((
            os.path.basename(file_found),
            req_url,
            aid.group(1) if aid else "",
            cdn_url,
            expires,
            ctype,
            len(raw),
            "Body is Wire-encrypted (not an image)",
        ))

    data_headers = (
        "Cache Entry", "Request URL", "Asset ID", "CDN Download URL",
        ("CDN Expires", "datetime"), "Content Type", "Entry Size (bytes)",
        "Note",
    )
    return data_headers, data_list, source_path

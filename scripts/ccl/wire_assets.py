"""
Wire asset recovery helpers.

Wire encrypts every shared asset with AES-256-CBC using a per-asset key
(``otr_key``) and prepends a random 16-byte IV, so the on-the-wire blob is
``IV || ciphertext`` and the event's ``sha256`` is the hash of that blob. The
encrypted blobs are cached on disk by the web app in two places:

  * the service-worker Cache Storage (Chromium Simple Cache ``*_0`` entries), and
  * the ordinary HTTP disk cache (Chromium block-file ``f_*`` entries),

both of which store the blob verbatim. Given the keys from the IndexedDB
asset-add events, we can match a cached blob to its event by SHA-256, verify
integrity and decrypt it back to the original image/media.

This module holds the shared, Context-free machinery so the Wire artifacts
(recovered-media, messages, attachments) can all reuse it. Actual check-in of
the decrypted bytes into the report is done by the caller (needs Context).
"""

import hashlib
import struct

try:
    from Crypto.Cipher import AES
except ImportError:  # pragma: no cover
    AES = None

# Chromium Simple Cache end-of-stream marker.
_EOF_MAGIC = struct.pack("<Q", 0xF4FA6F45970D41D8)


def crypto_available():
    return AES is not None


def _candidate_bodies(data):
    """Yield candidate response-body ranges from a Simple Cache (*_0) entry."""
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
    for e in eofs:
        if e + 24 <= len(data):
            size = struct.unpack_from("<q", data, e + 16)[0]
            if 0 < size <= e:
                yield data[e - size:e]
    if eofs:
        start = 20 + klen + 4
        if 0 < start < eofs[0]:
            yield data[start:eofs[0]]


def _pkcs7_unpad(b):
    if not b:
        return b
    p = b[-1]
    return b[:-p] if 1 <= p <= 16 and b[-p:] == bytes([p]) * p else b


def sniff(plain):
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


def build_asset_index(stores):
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


_EXT_FALLBACK = {"image/jpeg": "jpg", "image/png": "png", "video/mp4": "mp4"}


def recover_assets(files_found, by_sha):
    """Decrypt every cached asset whose blob is present in ``files_found``.

    ``files_found`` is the artifact's file list; Simple Cache ``*_0`` entries
    and block-file ``f_*`` bodies are examined. Returns
    ``{asset_id: descriptor}`` where descriptor adds ``plain`` (decrypted bytes),
    ``ctype``, ``ext`` and ``source`` (the cache file) to the event descriptor.
    """
    out = {}
    if AES is None or not by_sha:
        return out
    seen_sha = set()
    for f in files_found:
        f = str(f)
        base = f.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
        is_sc = f.endswith("_0")
        is_bf = base.startswith("f_")
        if not (is_sc or is_bf):
            continue
        try:
            with open(f, "rb") as fh:
                raw = fh.read()
        except OSError:
            continue

        candidates = []
        if is_bf:
            candidates.append(raw)            # block-file body == blob verbatim
        if is_sc:
            candidates.extend(_candidate_bodies(raw))

        for body in candidates:
            if len(body) < 32 or len(body) % 16 != 0:
                continue
            sha = hashlib.sha256(body).hexdigest()
            info = by_sha.get(sha)
            if not info or sha in seen_sha:
                continue
            try:
                cipher = AES.new(info["otr"], AES.MODE_CBC, body[:16])
                plain = _pkcs7_unpad(cipher.decrypt(body[16:]))
            except (ValueError, KeyError):
                continue
            ctype, ext = sniff(plain)
            ctype = ctype or info["ctype"] or "application/octet-stream"
            if not ext:
                ext = _EXT_FALLBACK.get(info["ctype"], "bin")
            seen_sha.add(sha)
            out[info["asset_id"]] = {
                **info, "plain": plain, "ctype": ctype, "ext": ext,
                "sha256": sha, "source": f,
            }
    return out

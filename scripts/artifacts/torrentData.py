__artifacts_v2__ = {
    "torrentData": {
        "name": "Torrent Data",
        "description": "Metadata from .torrent files: torrent name, info hash, and each listed "
                       "file's directory, file name and length.",
        "author": "@AlexisBrignoni",
        "creation_date": "2023-09-27",
        "last_update_date": "2026-10-09",
        "requirements": "bencoding",
        "category": "Torrent Data",
        "notes": "Info Hash is the SHA-1, in upper case, of the bytes of the info dictionary as "
                 "stored in the file, located by walking the file's bencoded structure. It is "
                 "blank when those bytes cannot be located. For a torrent with a files list, "
                 "each listed file gives one line: Directory is every path component before the "
                 "last, joined with '/', and File is the last. For a torrent with a length key "
                 "and no files list, one line gives the torrent name as File and that length. "
                 "Reference: BitTorrent.org, "
                 "'BEP 3: The BitTorrent Protocol Specification', "
                 "https://www.bittorrent.org/beps/bep_0003.html",
        "paths": ('*/*.torrent',),
        "output_types": "standard",
        "html_columns": ["Path"],
        "artifact_icon": "cloud-download",
    }
}

import hashlib

import bencoding

from scripts.ilapfuncs import artifact_processor
from scripts.html_safe import esc


def _decode(value):
    if isinstance(value, bytes):
        try:
            return value.decode()
        except UnicodeDecodeError:
            return value.decode('latin-1', 'replace')
    return value


def _skip(data, pos):
    """Return the offset just past the bencoded value that starts at pos."""
    lead = data[pos:pos + 1]
    if lead == b'i':
        return data.index(b'e', pos) + 1
    if lead in (b'l', b'd'):
        pos += 1
        while data[pos:pos + 1] != b'e':
            if pos >= len(data):
                raise ValueError('unterminated bencoded container')
            pos = _skip(data, pos)
        return pos + 1
    if lead.isdigit():
        colon = data.index(b':', pos)
        end = colon + 1 + int(data[pos:colon])
        if end > len(data):
            raise ValueError('bencoded string runs past the end of the file')
        return end
    raise ValueError('not a bencoded value')


def _stored_info_bytes(data):
    """Return the stored bytes of the top-level info value, or None when not located."""
    try:
        if data[:1] != b'd':
            return None
        pos = 1
        while data[pos:pos + 1] != b'e':
            key_end = _skip(data, pos)
            colon = data.index(b':', pos)
            key = data[colon + 1:key_end]
            value_end = _skip(data, key_end)
            if key == b'info':
                return data[key_end:value_end]
            pos = value_end
    except (ValueError, RecursionError):
        return None
    return None


@artifact_processor
def torrentData(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('.torrent'):
            continue
        source_path = file_found
        with open(file_found, 'rb') as f:
            raw = f.read()
        decoded = bencoding.bdecode(raw)

        info = decoded.get(b'info', {})
        stored_info = _stored_info_bytes(raw)
        info_hash = hashlib.sha1(stored_info).hexdigest().upper() if stored_info else ''
        torrentname = _decode(info.get(b'name', b''))

        rows = []
        for fileinfo in info.get(b'files', []):
            length = fileinfo.get(b'length', '')
            path_parts = fileinfo.get(b'path', [])
            dirr = '/'.join(str(_decode(part)) for part in path_parts[:-1])
            filen = _decode(path_parts[-1]) if path_parts else ''
            rows.append(f'<tr><td>{esc(dirr)}</td><td>{esc(filen)}</td><td>{esc(length)}</td></tr>')
        if b'files' not in info and b'length' in info:
            rows.append(f'<tr><td></td><td>{esc(torrentname)}</td>'
                        f'<td>{esc(info.get(b"length", ""))}</td></tr>')
        path_table = ('<table><tr><th>Directory</th><th>File</th><th>Length</th></tr>'
                      + ''.join(rows) + '</table>') if rows else ''

        data_list.append((torrentname, info_hash, path_table))

    data_headers = ('Torrent Name', 'Info Hash', 'Path')
    return data_headers, data_list, context.get_relative_path(source_path)

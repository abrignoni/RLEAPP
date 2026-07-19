__artifacts_v2__ = {
    "torrentData": {
        "name": "Torrent Data",
        "description": "Metadata from .torrent files: torrent name, info hash, and the file list.",
        "author": "@AlexisBrignoni",
        "creation_date": "2023-09-27",
        "last_update_date": "2026-06-28",
        "requirements": "bencoding",
        "category": "Torrent Data",
        "notes": "Info Hash is the SHA-1 of the bencoded info dictionary (uppercased).",
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
            decoded = bencoding.bdecode(f.read())

        info = decoded.get(b'info', {})
        info_hash = hashlib.sha1(bencoding.bencode(info)).hexdigest().upper()
        torrentname = _decode(info.get(b'name', b''))

        rows = []
        for fileinfo in info.get(b'files', []):
            length = fileinfo.get(b'length', '')
            path_parts = fileinfo.get(b'path', [])
            dirr = _decode(path_parts[0]) if len(path_parts) > 1 else ''
            filen = _decode(path_parts[-1]) if path_parts else ''
            rows.append(f'<tr><td>{esc(dirr)}</td><td>{esc(filen)}</td><td>{esc(length)}</td></tr>')
        path_table = ('<table><tr><th>Directory</th><th>File</th><th>Length</th></tr>'
                      + ''.join(rows) + '</table>') if rows else ''

        data_list.append((torrentname, info_hash, path_table))

    data_headers = ('Torrent Name', 'Info Hash', 'Path')
    return data_headers, data_list, context.get_relative_path(source_path)

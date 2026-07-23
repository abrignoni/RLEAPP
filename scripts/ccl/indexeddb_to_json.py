"""
indexeddb_to_json.py

In-memory adaptation of the Spyder Forensics "IndexedDBtoJSON.py" helper
(www.spyderforensics.com, "Advanced Applied Database Forensics"). The original
walks a Chromium IndexedDB/LevelDB folder with the CCL reader and writes a raw
JSON file plus a "normalized" JSON file to disk.

This RLEAPP-branch copy keeps the exact same parsing/normalization pipeline but:
  * returns the parsed data structure in memory instead of writing files;
  * retains the owning database (name/number/origin) on every record so an
    artifact can attribute records to the correct signed-in account when a
    single LevelDB holds more than one Wire login;
  * is import-safe and quiet (progress goes through an optional log callback).

The original file-writing CLI is preserved under ``if __name__ == "__main__"``
for standalone use, but RLEAPP calls ``load_indexeddb()`` directly.

Parsing/deserialization is done by the vendored CCL modules
(https://github.com/cclgroupltd/ccl_chromium_reader).
"""

import argparse
import ast
import base64
import json
import pathlib
import re
from collections.abc import Mapping

from . import ccl_chromium_indexeddb

UNDEFINED_PATTERN = re.compile(r"<Undefined>")
IDBKEY_RE = re.compile(r"^<IdbKey (.+)>$", re.DOTALL)


def serialize_key_value(key_or_value):
    """Convert IdbKey or IdbValue to a JSON-serializable format."""
    if isinstance(key_or_value, bytes):
        return base64.b64encode(key_or_value).decode("utf-8")
    elif isinstance(key_or_value, memoryview):
        return base64.b64encode(bytes(key_or_value)).decode("utf-8")
    else:
        return str(key_or_value)


def normalize_key(k):
    """Strip <IdbKey ...> if present."""
    if isinstance(k, str):
        m = IDBKEY_RE.match(k)
        if m:
            return m.group(1)
    return k


def safe_eval(s):
    """Evaluate Python-style dict/list strings that may include <Undefined>."""
    s = UNDEFINED_PATTERN.sub("None", s)
    try:
        return ast.literal_eval(s)
    except Exception:
        return s


def parse_nested_maybe_python(obj, _depth=0):
    """Walk loaded data and convert stringified Python dict/list/tuple values
    into real structures."""
    if _depth > 10:
        return obj
    if isinstance(obj, Mapping):
        return {k: parse_nested_maybe_python(v, _depth) for k, v in obj.items()}
    if isinstance(obj, list):
        return [parse_nested_maybe_python(v, _depth) for v in obj]
    if isinstance(obj, str):
        s = obj.strip()
        if (
            (s.startswith("{") and s.endswith("}")) or
            (s.startswith("[") and s.endswith("]")) or
            (s.startswith("(") and s.endswith(")"))
        ):
            parsed = safe_eval(s)
            if parsed is None or isinstance(parsed, str):
                return obj
            return parse_nested_maybe_python(parsed, _depth + 1)
        return obj
    return obj


def sanitize_for_json(obj):
    """Convert non-JSON types into JSON-safe values."""
    if isinstance(obj, Mapping):
        return {str(normalize_key(k)): sanitize_for_json(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [sanitize_for_json(v) for v in obj]
    if isinstance(obj, set):
        return [sanitize_for_json(v) for v in sorted(obj, key=lambda x: str(x))]
    if isinstance(obj, (bytes, memoryview)):
        return base64.b64encode(bytes(obj)).decode("ascii")
    return obj


def normalize_json_data(raw_data):
    """Normalize raw IndexedDB data into cleaned JSON-safe structures."""
    parsed = parse_nested_maybe_python(raw_data)
    cleaned = sanitize_for_json(parsed)
    return cleaned


def export_indexeddb_to_data(ldb_path, log=None):
    """Process an IndexedDB LevelDB folder and return raw export data.

    Returns a dict ``{object_store_name: [record, ...]}`` where each record is
    ``{"db_name", "db_number", "origin", "key", "value"}``. ``key``/``value`` are
    the serialized (string) forms produced by the CCL reader; run the result
    through :func:`normalize_json_data` to get real Python structures.
    """
    def _log(msg):
        if log:
            log(msg)

    blob_dir = pathlib.Path(ldb_path).parent / (
        pathlib.Path(ldb_path).name.replace(".leveldb", ".blob"))
    wrapper = ccl_chromium_indexeddb.WrappedIndexDB(
        ldb_path, blob_dir if blob_dir.exists() else None)
    output_data = {}

    for db_info in wrapper.database_ids:
        db = wrapper[db_info.dbid_no]
        _log(f"  Database {db.db_number}: {db.name} (origin={db.origin})")

        for obj_store_name in db.object_store_names:
            if obj_store_name is None:
                continue
            obj_store = db[obj_store_name]
            output_data.setdefault(obj_store.name, [])

            record_count = 0
            for record in obj_store.iterate_records():
                record_count += 1
                output_data[obj_store.name].append({
                    "db_name": db.name,
                    "db_number": db.db_number,
                    "origin": db.origin,
                    "key": serialize_key_value(record.key),
                    "value": serialize_key_value(record.value),
                })
            if record_count:
                _log(f"    {obj_store.name}: {record_count} record(s)")

    return output_data


def load_indexeddb(ldb_path, log=None):
    """Read a LevelDB folder and return the fully normalized store dict.

    ``{object_store_name: [{"db_name", "db_number", "origin", "key", "value"}]}``
    with ``key``/``value`` converted to real Python structures.
    """
    raw = export_indexeddb_to_data(ldb_path, log=log)
    return normalize_json_data(raw)


# --------------------------------------------------------------------------- #
# Standalone CLI (unchanged behaviour: writes raw + normalized JSON to disk)
# --------------------------------------------------------------------------- #

def _main(args):
    ldb_path = pathlib.Path(args.input)
    output_folder = pathlib.Path(args.output)
    if not ldb_path.is_dir():
        raise NotADirectoryError(f"Input must be a LevelDB directory: {ldb_path}")
    output_folder.mkdir(parents=True, exist_ok=True)

    raw_data = export_indexeddb_to_data(ldb_path, log=print)
    raw_json_path = output_folder / f"{ldb_path.name}.json"
    with open(raw_json_path, "w", encoding="utf-8") as fh:
        json.dump(raw_data, fh, ensure_ascii=False, indent=4)

    normalized = normalize_json_data(raw_data)
    normalized_json_path = output_folder / f"{ldb_path.name}_Normalized.json"
    with open(normalized_json_path, "w", encoding="utf-8") as fh:
        json.dump(normalized, fh, ensure_ascii=False, indent=2,
                  default=lambda o: None if o is ... else str(o))
    print(f"Raw JSON        : {raw_json_path}")
    print(f"Normalized JSON : {normalized_json_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert IndexedDB to JSON and normalize the data")
    parser.add_argument("-i", "--input", required=True,
                        help="Input IndexedDB LevelDB directory path")
    parser.add_argument("-o", "--output", required=True,
                        help="Output folder for JSON exports")
    _main(parser.parse_args())

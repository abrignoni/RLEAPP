__artifacts_v2__ = {
    "offlinePages": {
        "name": "Offline Pages",
        "description": "Saved offline web pages (MHTML) with the Snapshot-Content-Location header"
                       " value and a media preview.",
        "author": "@AlexisBrignoni",
        "creation_date": "2023-01-25",
        "last_update_date": "2026-11-23",
        "requirements": "none",
        "category": "Offline Pages",
        "notes": "Timestamp Modified is the modification time the tool reads from the input for "
                 "the file as a UTC time, to the whole second, such as from a tar header or a zip"
                 " entry's NTFS or extended timestamp field. When the tool reads no UTC time, "
                 "Timestamp Modified is blank and Modified (no zone, as stored) shows the date "
                 "and time the input holds, with no zone conversion. That is the case for a FAT "
                 "directory entry, an exFAT directory entry (its stored UTC offset is not applied"
                 " or shown here) and a zip entry with only its DOS date and time. Both columns "
                 "are blank when the input holds neither, and a recorded time of 0 is treated as "
                 "no time. For a folder or single-file input Timestamp Modified is the time the "
                 "operating system reports for that file on the examiner's machine, including any"
                 " conversion it applied, and whatever copied the file there may have set it. The"
                 " staged copy's own time is not reported. Web Source is the "
                 "Snapshot-Content-Location header and MIME Date is the Date header, each as "
                 "Python's email parser returns the first header of that name. Encoded words are "
                 "not decoded, and bytes that are not valid UTF-8 are replaced. Timestamp "
                 "Modified does not establish a source event time.",
        "paths": ('*/*.mhtml', '*/*.mht'),
        "output_types": "standard",
        "artifact_icon": "globe",
    }
}

import email
import os

from datetime import datetime, timedelta, timezone
from scripts.ilapfuncs import artifact_processor, check_in_media


def _utc(seconds):
    """Unix seconds as a UTC datetime in whole seconds, '' for none or a value datetime cannot hold."""
    if seconds is None:
        return ''
    try:
        return datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=seconds // 1)
    except OverflowError:
        return ''


def _file_times(seeker, path):
    """(UTC seconds, reading with no zone) the input records for a staged file.

    The staged copy's own time is not used: for a FAT, exFAT or DOS-only zip reading it is
    that reading placed in the examiner's time zone.
    """
    infos = getattr(seeker, 'file_infos', None) or {}
    windows = str(path).replace('/', '\\')
    bare = windows.removeprefix('\\\\?\\')
    info = next((infos[name] for name in (str(path), windows, bare, '\\\\?\\' + bare)
                 if name in infos), None)
    times = getattr(info, 'times', None)
    for value in (getattr(times, 'modified', None), getattr(info, 'modification_date', None)):
        if isinstance(value, (int, float)) and value:
            return value, ''
    return None, getattr(times, 'modified_no_zone', None) or ''


@artifact_processor
def offlinePages(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found).startswith('.'):
            continue
        source_path = file_found
        modified, no_zone = _file_times(context.get_seeker(), file_found)
        with open(file_found, 'r', encoding='utf-8', errors='replace') as fp:
            message = email.message_from_file(fp)
        media = check_in_media(file_found, os.path.basename(file_found))
        data_list.append((_utc(modified), no_zone, message['Date'] or '',
                          media, message['Snapshot-Content-Location'] or '',
                          message['Subject'] or '',
                          context.get_relative_path(file_found)))

    data_headers = (('Timestamp Modified', 'datetime'), 'Modified (no zone, as stored)', 'MIME Date', ('File', 'media'),
                    'Web Source', 'Subject', 'Source in Extraction')
    return data_headers, data_list, context.get_relative_path(source_path)

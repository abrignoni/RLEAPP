__artifacts_v2__ = {
    "sysShutdownProcesses": {
        "name": "Sysdiagnose - Shutdown Log Processes",
        "description": "Parses remaining client processes at shutdown from the shutdown.log file"
                       " in Sysdiagnose logs, based off work by Kaspersky Lab"
                       " https://github.com/KasperskyLab/iShutdown",
        "author": "@KevinPagano3",
        "creation_date": "2024-02-13",
        "last_update_date": "2026-07-06",
        "requirements": "none",
        "category": "Sysdiagnose",
        "notes": "",
        "paths": ('*/shutdown.log',),
        "output_types": "standard",
        "artifact_icon": "power",
    },
    "sysShutdownReboots": {
        "name": "Sysdiagnose - Shutdown Log Reboots",
        "description": "Parses reboot events from the shutdown.log file in Sysdiagnose logs,"
                       " based off work by Kaspersky Lab"
                       " https://github.com/KasperskyLab/iShutdown",
        "author": "@KevinPagano3",
        "creation_date": "2024-02-13",
        "last_update_date": "2026-07-06",
        "requirements": "none",
        "category": "Sysdiagnose",
        "notes": "",
        "paths": ('*/shutdown.log',),
        "output_types": "standard",
        "artifact_icon": "power",
    }
}

import re

from scripts.ilapfuncs import artifact_processor, convert_ts_int_to_utc


def _parse_shutdown_log(file_found, source_file):
    """Parses one shutdown.log, returning (process_rows, reboot_rows)."""
    process_rows = []
    reboot_rows = []

    with open(file_found, encoding='utf-8', mode='r') as f:
        lines = f.readlines()

    entry_num = 1
    entries = []
    reboots = 1

    for line in lines:
        pid_match = re.search(r'remaining client pid: (\d+) \((.*?)\)', line)
        if pid_match:
            pid, path = pid_match.groups()
            entries.append((pid, path))

        sigterm_match = re.search(r'SIGTERM: \[(\d+)\]', line)
        if sigterm_match:
            timestamp = int(sigterm_match.group(1))
            reboot_time = convert_ts_int_to_utc(timestamp)
            reboot_rows.append((reboot_time, reboots, source_file))
            reboots += 1

            for pid, path in entries:
                process_rows.append((reboot_time, entry_num, pid, path, source_file))
                entry_num += 1
            entries = []

    return process_rows, reboot_rows


@artifact_processor
def sysShutdownProcesses(context):
    data_list = []
    source_path = ''

    for file_found in context.get_files_found():
        file_found = str(file_found)
        source_path = file_found
        process_rows, _ = _parse_shutdown_log(file_found, context.get_relative_path(file_found))
        data_list.extend(process_rows)

    data_headers = (('Timestamp', 'datetime'), 'Entry Number', 'PID', 'Path', 'Source File')
    return data_headers, data_list, source_path


@artifact_processor
def sysShutdownReboots(context):
    data_list = []
    source_path = ''

    for file_found in context.get_files_found():
        file_found = str(file_found)
        source_path = file_found
        _, reboot_rows = _parse_shutdown_log(file_found, context.get_relative_path(file_found))
        data_list.extend(reboot_rows)

    data_headers = (('Timestamp', 'datetime'), 'Reboot Number', 'Source File')
    return data_headers, data_list, source_path

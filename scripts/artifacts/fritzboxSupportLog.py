__artifacts_v2__ = {
    "get_fritz_devinfo": {
        "name": "Fritz!Box Device Info",
        "description": "Outputs the Device Info from a Fritzbox Supportdata dump",
        "author": "@C_Peter",
        "creation_date": "2026-07-05",
        "last_update_date": "2026-07-05",
        "requirements": "none",
        "category": "FritzBox Supportdata",
        "notes": "",
        "paths": ('*/support_FRITZ*.txt'),
        "output_types": "standard",
        'artifact_icon': 'router',
    },
    "get_fritz_callog": {
        "name": "Fritz!Box Call Log",
        "description": "Processes the Call Log from a Fritzbox Supportdata dump",
        "author": "@C_Peter",
        "creation_date": "2026-07-05",
        "last_update_date": "2026-07-05",
        "requirements": "none",
        "category": "FritzBox Supportdata",
        "notes": "",
        "paths": ('*/support_FRITZ*.txt'),
        "output_types": "standard",
        'artifact_icon': 'phone-call',
    },
    "get_fritz_events": {
        "name": "Fritz!Box Events",
        "description": "Processes the Eventlog from a Fritzbox Supportdata dump",
        "author": "@C_Peter",
        "creation_date": "2026-07-05",
        "last_update_date": "2026-07-05",
        "requirements": "none",
        "category": "FritzBox Supportdata",
        "notes": "",
        "paths": ('*/support_FRITZ*.txt'),
        "output_types": "standard",
        'artifact_icon': 'activity',
    },
    "get_fritz_landevices": {
        "name": "Fritz!Box Landevices",
        "description": "Processes the listed Landevices from a Fritzbox Supportdata dump",
        "author": "@C_Peter",
        "creation_date": "2026-07-05",
        "last_update_date": "2026-07-05",
        "requirements": "none",
        "category": "FritzBox Supportdata",
        "notes": "",
        "paths": ('*/support_FRITZ*.txt'),
        "output_types": "standard",
        'artifact_icon': 'devices',
    },
    "get_fritz_logs": {
        "name": "Fritz!Box Logs",
        "description": "Processes the logs from a Fritzbox Supportdata dump",
        "author": "@C_Peter",
        "creation_date": "2026-07-05",
        "last_update_date": "2026-07-05",
        "requirements": "none",
        "category": "FritzBox Supportdata",
        "notes": "",
        "paths": ('*/support_FRITZ*.txt'),
        "output_types": "standard",
        'artifact_icon': 'logs',
    },
    "get_fritz_dmesg": {
        "name": "Fritz!Box dmesg",
        "description": "Processes the dmesg logs from a Fritzbox Supportdata dump",
        "author": "@C_Peter",
        "creation_date": "2026-07-05",
        "last_update_date": "2026-07-05",
        "requirements": "none",
        "category": "FritzBox Supportdata",
        "notes": "",
        "paths": ('*/support_FRITZ*.txt'),
        "output_types": "standard",
        'artifact_icon': 'cpu',
    }
}

import re
from datetime import datetime, timezone, timedelta
from scripts.ilapfuncs import artifact_processor, logfunc

tz_map = {
        "CET":  timezone(timedelta(hours=1)),
        "CEST": timezone(timedelta(hours=2)),
        "UTC":  timezone.utc,
        "GMT":  timezone.utc,
        "EST":  timezone(timedelta(hours=-5)),
        "EDT":  timezone(timedelta(hours=-4)),
        "CST":  timezone(timedelta(hours=-6)), 
        "CDT":  timezone(timedelta(hours=-5)),
        "MST":  timezone(timedelta(hours=-7)),
        "MDT":  timezone(timedelta(hours=-6)),
        "PST":  timezone(timedelta(hours=-8)),
        "PDT":  timezone(timedelta(hours=-7)),
        "BRT":  timezone(timedelta(hours=-3)),
        "BRST": timezone(timedelta(hours=-2)),
        "JST":  timezone(timedelta(hours=9)),
        "KST":  timezone(timedelta(hours=9)),
        "HKT":  timezone(timedelta(hours=8)),
        "SGT":  timezone(timedelta(hours=8)),
        "AEST": timezone(timedelta(hours=10)),
        "AEDT": timezone(timedelta(hours=11)),
        "ACST": timezone(timedelta(hours=9, minutes=30)),
        "ACDT": timezone(timedelta(hours=10, minutes=30)),
        "AWST": timezone(timedelta(hours=8)),
        "NZST": timezone(timedelta(hours=12)),
        "NZDT": timezone(timedelta(hours=13)),
        "IST":  timezone(timedelta(hours=5, minutes=30)),
        "CST_CN": timezone(timedelta(hours=8)),
    } 

_PARSED_LOG= False
_LOG_DICT = {}
_TITLE_DICT = {}

def get_timezone(dt, tz_name):
    """
    Checks for the correct timezone offset
    """

    if tz_name in ("CET", "CEST"):
        year = dt.year
        start = datetime(year, 3, 31)
        start -= timedelta(days=start.weekday() + 1)
        end = datetime(year, 10, 31)
        end -= timedelta(days=end.weekday() + 1)
        if start <= dt.replace(tzinfo=None) < end:
            return timezone(timedelta(hours=2))
        return timezone(timedelta(hours=1))

    if tz_name in ("EST", "EDT"):
        if dt.year >= 2007:
            start = datetime(dt.year, 3, 8)
            start += timedelta(days=(6 - start.weekday()) % 7)
            start += timedelta(weeks=0)
            end = datetime(dt.year, 11, 1)
            end += timedelta(days=(6 - end.weekday()) % 7)
            if start <= dt.replace(tzinfo=None) < end:
                return timezone(timedelta(hours=-4))
        return timezone(timedelta(hours=-5))

    return tz_map.get(tz_name, timezone.utc)

# Helper to split the log output
def split_log(log_file) -> dict:
    """Function to split the Supportdata Log txt file in section parts"""
    global _PARSED_LOG, _LOG_DICT # pylint: disable=global-statement
    if _PARSED_LOG:
        return
    if not log_file:
        return

    with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
        log_txt = f.read()

    title_keys = {
        "version": "version",
        "subversion": "subversion",
        "produkt": "product",
        "datum": "date",
    }

    logdict = {}
    title_re  = re.compile(r"^##### TITLE\s+(\S+)\s*(.*)$")
    start_re  = re.compile(r"^##### BEGIN SECTION\s+(.+?)\s*$")
    uptime_re = re.compile(r"uptime:\s+\d{2}:\d{2}:\d{2}\s+up\s+(?:(?P<days>\d+)\s+days?,\s+)?(?P<hours>\d+):(?P<minutes>\d+)")

    current_section = None
    uptime_seconds = None
    current_lines = []

    def flush():
        if current_section:
            logdict[current_section] = "\n".join(current_lines)

    for line in log_txt.splitlines():
        if uptime_seconds is None:
            uptime_match = uptime_re.search(line)
            if uptime_match:
                uptime_seconds = (
                    int(uptime_match.group("days") or 0) * 86400 +
                    int(uptime_match.group("hours")) * 3600 +
                    int(uptime_match.group("minutes")) * 60
                )

        title_match = title_re.match(line)
        if title_match:
            key = title_keys.get(title_match.group(1).lower())
            if key:
                value = title_match.group(2).strip()

                if key == "date":
                    fields = value.split()

                    tz_name = fields[-2]
                    dt = datetime.strptime(
                        " ".join(fields[:-2] + [fields[-1]]),
                        "%a %b %d %H:%M:%S %Y"
                    ).replace(tzinfo=tz_map[tz_name])

                    _TITLE_DICT["timezone"] = tz_name
                    _TITLE_DICT["date"] = int(dt.timestamp())
                else:
                    _TITLE_DICT[key] = value
            continue

        start_match = start_re.search(line)
        if start_match:
            flush()
            current_section = start_match.group(1)
            current_lines = []
            continue

        if not current_section:
            continue

        current_lines.append(line)

    flush()
    if uptime_seconds:
        _TITLE_DICT["boot"] = _TITLE_DICT["date"] - uptime_seconds
    _LOG_DICT = logdict
    _PARSED_LOG = True

@artifact_processor
def get_fritz_devinfo(context):
    """Outputs the Device Info from a Fritzbox Supportdata dump"""
    files_found = context.get_files_found()
    source_path = files_found[0]
    data_list = []
    device_dict = {}
    split_log(source_path)
    support_data = None
    for section, content in _LOG_DICT.items():
        if section.startswith("Support_Data Supportdata"):
            support_data = content
            logfunc(f'FritzLog does include a section: {section}.')
            break
    if support_data is None:
        logfunc('FritzLog does not include a \"Support_Data Supportdata\" section.')
    else:
        for line in support_data.splitlines():
            line = line.strip()
            if not line or "\t" not in line:
                continue
            key, value = line.split("\t", 1)
            device_dict[key] = value

        data_dict = {}
        data_dict["ProductID"]      = device_dict.get("ProductID", None)
        data_dict["Serialnumber"]   = device_dict.get("SerialNumber", None)
        data_dict["TR069 Serial"]   = device_dict.get("tr069_serial", None)
        data_dict["GPON Serial"]    = device_dict.get("gpon_serial", None)
        data_dict["Bootloader"]     = device_dict.get("bootloaderVersion", None)
        data_dict["Firmware"]       = device_dict.get("firmware_info", None)
        data_dict["Country"]        = device_dict.get("country", None)
        data_dict["Language"]       = device_dict.get("language", None)
        data_dict["MAC_A"]          = device_dict.get("maca", None)
        data_dict["MAC_B"]          = device_dict.get("macb", None)
        data_dict["MAC_WLAN"]       = device_dict.get("macwlan", None)
        data_dict["MAC_WLAN2"]      = device_dict.get("macwlan2", None)
        data_dict["MAC_DSL"]        = device_dict.get("macdsl", None)
        data_dict["USB MAC"]        = device_dict.get("usb_board_mac", None)
        data_dict["USB RNDIS MAC"]  = device_dict.get("usb_rndis_mac", None)
        data_dict["IP"]             = device_dict.get("my_ipaddress", None)
        data_dict["WLAN SSID"]      = device_dict.get("wlan_ssid", None)

        for key, value in data_dict.items():
            data_list.append((key, value))

    data_headers = ('Key', 'Value')

    return data_headers, data_list, source_path


@artifact_processor
def get_fritz_callog(context):
    """Processes the Call Log from a Fritzbox Supportdata dump"""
    files_found = context.get_files_found()
    source_path = files_found[0]
    data_list = []
    call_re = re.compile(
        r"""
        call\s+idx:(?P<idx>\d+)\s+
        (?P<date>\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2})\s+
        msn:(?P<msn>\S*)\s+
        number:(?P<number>\S*)\s+
        duration:(?P<duration>\d+)\s+
        call_type:(?P<call_type>\S+)\s+
        port:(?P<port>\S+)\s+
        port_name:(?P<port_name>.*)
        """,
        re.VERBOSE
    )
    split_log(source_path)
    calllog = _LOG_DICT.get("calllog", None)
    if calllog is None:
        logfunc('FritzLog does not include a \"calllog\" section.')
    else:
        logfunc('FritzLog does include a \"calllog\" section.')
        tz_name = _TITLE_DICT.get("timezone", "UTC")
        tz = tz_map.get(tz_name, timezone.utc)
        data_list = []    
        for line in calllog.splitlines():
            stripped = line.strip()
            match = call_re.match(stripped)
            if not match:
                continue
            data = match.groupdict()
            naive_dt = datetime.strptime(data["date"], "%d.%m.%Y %H:%M:%S")
            tz = get_timezone(naive_dt,_TITLE_DICT.get("timezone", "UTC"))
            dt = naive_dt.replace(tzinfo=tz)
            call_time = int(dt.timestamp())
            time_utc = datetime.fromtimestamp(call_time, tz=timezone.utc)
            msn = data["msn"]
            number = data["number"]
            idx = int(data["idx"])
            duration = int(data["duration"])
            call_type = data["call_type"]
            port = int(data["port"])
            port_name = data["port_name"].strip()
            data_list.append((time_utc, idx, msn, number, duration, call_type,  port, port_name))

    data_headers = (('Timestamp', 'datetime'), "IDX", "MSN", ('Phone Number', 'phonenumber'), "Duration", "Call Type", "Port", "Port Name")

    return data_headers, data_list, source_path

@artifact_processor
def get_fritz_events(context):
    """Processes the Eventlog from a Fritzbox Supportdata dump"""
    files_found = context.get_files_found()
    source_path = files_found[0]
    data_list = []
    event_re = re.compile(
        r"^(?P<date>\d{2}\.\d{2}\.\d{2})\s+"
        r"(?P<time>\d{2}:\d{2}:\d{2})\s+"
        r"(?P<message>.*)$"
    )
    split_log(source_path)
    elog = _LOG_DICT.get("Events Events", None)
    if elog is None:
        logfunc('FritzLog does not include an \"Events Events\" section.')
    else:
        logfunc('FritzLog does include an \"Events Events\" section.')
        tz_name = _TITLE_DICT.get("timezone", "UTC")
        tz = tz_map.get(tz_name, timezone.utc)
        data_list = []
        for line in elog.splitlines():
            match = event_re.match(line)
            if not match:
                continue
            naive_dt = datetime.strptime(
                f"{match.group('date')} {match.group('time')}",
                "%d.%m.%y %H:%M:%S")
            tz = get_timezone(naive_dt,_TITLE_DICT.get("timezone", "UTC"))
            dt = naive_dt.replace(tzinfo=tz)
            event_time = int(dt.timestamp())
            time_utc = datetime.fromtimestamp(event_time, tz=timezone.utc)
            event = match.group("message").strip()
            data_list.append((time_utc, event))

    data_headers = (('Timestamp', 'datetime'), "Event")

    return data_headers, data_list, source_path

@artifact_processor
def get_fritz_landevices(context):
    """Processes the listed Landevices from a Fritzbox Supportdata dump"""
    files_found = context.get_files_found()
    source_path = files_found[0]
    data_list = []
    split_log(source_path)
    lando = _LOG_DICT.get("landevices LAN devices", None)
    if lando is None:
        logfunc('FritzLog does not include an \"landevices LAN devices\" section.')
    else:
        logfunc('FritzLog does include an \"landevices LAN devices\" section.')
        current: dict[str, object] | None = None
        ignore_nested = False
        values = {"UID", "ip", "mac", "name", "friendly_name", "vendorname", "firstused", "lastused"}
        for line in lando.splitlines():
            line = line.strip()
            if line.startswith("landevice") and line.endswith("/"):
                m = re.match(r"^landevice(\d+)/$", line)
                if not m:
                    continue

                idx = int(m.group(1))
                if current is not None:
                    data_list.append((
                        current["landevice"],
                        current["UID"],
                        current["ip"],
                        current["mac"],
                        current["name"],
                        current["friendly_name"],
                        current["vendorname"],
                        datetime.fromtimestamp(int(current["firstused"]), tz=timezone.utc) if current["firstused"] else None,
                        datetime.fromtimestamp(int(current["lastused"]), tz=timezone.utc) if current["lastused"] else None,
                    ))

                #if idx == 0:
                #    current = None
                #    continue
                current = {h: None for h in values}
                current["landevice"] = idx
                ignore_nested = False
                continue  
            if current is None:
                continue
            if line.startswith("-----------"):
                break
            if line.startswith(("iplist")) and line.endswith("/"):
                ignore_nested = True
                continue
            if ignore_nested:
                if line.startswith("url"):
                    ignore_nested = False
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            if key in values:
                if key in ("firstused", "lastused") and value:
                    value = int(value)
                current[key] = value

        if current:
            data_list.append((
                current["landevice"],
                current["UID"],
                current["ip"],
                current["mac"],
                current["name"],
                current["friendly_name"],
                current["vendorname"],
                datetime.fromtimestamp(int(current["firstused"]), tz=timezone.utc) if current["firstused"] else None,
                datetime.fromtimestamp(int(current["lastused"]), tz=timezone.utc) if current["lastused"] else None,
            ))

    data_headers = ('Landevice', 'UID', 'IP', 'MAC', 'Name', 'Friendly Name', 'Vendorname', ('First used', 'datetime'), ('Last used', 'datetime'))
    return data_headers, data_list, source_path


@artifact_processor
def get_fritz_logs(context):
    """Processes the logs from a Fritzbox Supportdata dump"""
    files_found = context.get_files_found()
    source_path = files_found[0]
    data_list = []
    split_log(source_path)
    log_re = re.compile(
        r"^(?P<date>\d{4}-\d{2}-\d{2}) "
        r"(?P<time>\d{2}:\d{2}:\d{2}\.\d{3}) - "
        r"(?P<message>.*)$"
    )
    tz = tz_map.get(_TITLE_DICT.get("timezone"), timezone.utc)
    for section, content in _LOG_DICT.items():
        if content:
            for line in content.splitlines():
                match = log_re.match(line)
                if not match:
                    continue

                naive_dt = datetime.strptime(
                    f"{match.group('date')} {match.group('time')}",
                    "%Y-%m-%d %H:%M:%S.%f")
                tz = get_timezone(naive_dt,_TITLE_DICT.get("timezone", "UTC"))
                dt = naive_dt.replace(tzinfo=tz)
                log_time = int(dt.timestamp())
                time_utc = datetime.fromtimestamp(log_time, tz=timezone.utc)
                message = match.group("message")
                data_list.append((time_utc, message, section))

    data_headers = (('Timestamp', 'datetime'), "Message", "Section")

    return data_headers, data_list, source_path


@artifact_processor
def get_fritz_dmesg(context):
    """Processes the dmesg logs from a Fritzbox Supportdata dump"""
    files_found = context.get_files_found()
    source_path = files_found[0]
    data_list = []
    split_log(source_path)
    dmesg_re = re.compile(r"^\[(?P<sec>\d+\.\d+)\]\[(?P<section>[^\]]+)\]\s*(?P<message>.*)$")
    boot_ts = _TITLE_DICT.get("boot", 0)
    dmesg = _LOG_DICT.get("dmesg", None)
    if dmesg is None:
        logfunc('FritzLog does not include an \"dmesg\" section.')
    else:
        logfunc('FritzLog does include an \"dmesg\" section.')
        for line in dmesg.splitlines():
            line = line.strip()
            dmesg_match = dmesg_re.match(line)
            if not dmesg_match:
                continue
            event_time = boot_ts + float(dmesg_match.group("sec"))
            time_utc = datetime.fromtimestamp(event_time, tz=timezone.utc)
            section = dmesg_match.group("section").strip()
            message = dmesg_match.group("message")

            data_list.append((time_utc, section, message))

    data_headers = (('Timestamp', 'datetime'), "Section", "Message")

    return data_headers, data_list, source_path

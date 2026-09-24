"""
Robinhood law enforcement returns.

A Robinhood production mixes CSV exports and PDFs:

  crypto_account_transfers.csv, crypto_account_orders.csv   crypto (RHC) activity
  data_request_ip_timestamps_*.csv                          IP log
  <account>_1099_<date>.csv                                 1099-B detail
  Account Master PDF                                        a browser print of an internal
                                                            account page, with edit logs
  <account>_account_statement_<date>.pdf                    brokerage (RHF) statements
  <uuid>_rhc_statement_<uuid>_<date>.pdf                    crypto (RHC) statements

CSV values are reported as produced, with the provider's own column names. The PDFs have
no columns to keep, so their text is read from page positions; that code was written for
and tested against the layouts of one production, and the Parsing Notes artifact lists
anything it could not place.
"""

__artifacts_v2__ = {
    'robinhoodCryptoTransfers': {
        'name': 'Robinhood - Crypto Transfers',
        'description': 'Rows of a crypto_account_transfers.csv file.',
        'author': '@CyberMike81',
        'creation_date': '2026-09-23',
        'last_update_date': '2026-09-24',
        'requirements': 'none',
        'category': 'Robinhood Returns',
        'notes': ('Timestamp (UTC) is derived from created_at, which states an offset; Time Basis records that. '
                  'withdrawal_submitted_timestamp is reported as produced and is empty in the synthetic fixture; '
                  'a blank value remains blank. This file states no account number. Leading and trailing spaces '
                  'in a cell are removed; nothing else in a value is changed. Other Columns (as produced) is '
                  'empty unless the file carries columns this artifact does not name; any such column is kept '
                  'there as JSON. A text line at the end of the file that is not a record is listed in Robinhood '
                  "- Parsing Notes. Source File is the file's path within the input; the same file can appear "
                  'more than once in a production, and each copy is reported. Layouts are those of synthetic '
                  'files and one 2025 production; other production years and layouts may differ.'),
        'paths': ('*crypto_account_transfers*.csv',),
        'output_types': 'standard',
        'artifact_icon': 'send',
    },
    'robinhoodCryptoOrders': {
        'name': 'Robinhood - Crypto Orders',
        'description': 'Rows of a crypto_account_orders.csv file.',
        'author': '@CyberMike81',
        'creation_date': '2026-09-23',
        'last_update_date': '2026-09-24',
        'requirements': 'none',
        'category': 'Robinhood Returns',
        'notes': ('Time Entered: The file states no time zone for this column, so it is reported as produced and '
                  'not converted. This file states no account number. Leading and trailing spaces in a cell are '
                  'removed; nothing else in a value is changed. Other Columns (as produced) is empty unless the '
                  'file carries columns this artifact does not name; any such column is kept there as JSON. A '
                  'text line at the end of the file that is not a record is listed in Robinhood - Parsing Notes. '
                  "Source File is the file's path within the input; the same file can appear more than once in a "
                  'production, and each copy is reported. Layouts are those of synthetic files and one 2025 '
                  'production; other production years and layouts may differ.'),
        'paths': ('*crypto_account_orders*.csv',),
        'output_types': 'standard',
        'artifact_icon': 'shopping-cart',
    },
    'robinhoodIPLog': {
        'name': 'Robinhood - IP Log',
        'description': 'Rows of a data_request_ip_timestamps CSV file.',
        'author': '@CyberMike81',
        'creation_date': '2026-09-23',
        'last_update_date': '2026-09-24',
        'requirements': 'none',
        'category': 'Robinhood Returns',
        'notes': ('event_date_time: The file states no time zone for this column, so it is reported as produced '
                  'and not converted. geo_ip columns are reported as produced. Leading and trailing spaces in a '
                  'cell are removed; nothing else in a value is changed. Other Columns (as produced) is empty '
                  'unless the file carries columns this artifact does not name; any such column is kept there as '
                  'JSON. A text line at the end of the file that is not a record is listed in Robinhood - Parsing '
                  "Notes. Source File is the file's path within the input; the same file can appear more than "
                  'once in a production, and each copy is reported. Layouts are those of synthetic files and one '
                  '2025 production; other production years and layouts may differ.'),
        'paths': ('*data_request_ip_timestamps*.csv',),
        'output_types': 'standard',
        'artifact_icon': 'globe',
    },
    'robinhood1099': {
        'name': 'Robinhood - 1099-B Detail',
        'description': 'Rows of a Robinhood 1099 CSV file.',
        'author': '@CyberMike81',
        'creation_date': '2026-09-23',
        'last_update_date': '2026-09-24',
        'requirements': 'none',
        'category': 'Robinhood Returns',
        'notes': ('Values are as produced. Where BASIS NOT SHOWN is Y, the COST BASIS value in the file is not a '
                  'reported basis. Leading and trailing spaces in a cell are removed; nothing else in a value is '
                  'changed. Other Columns (as produced) is empty unless the file carries columns this artifact '
                  'does not name; any such column is kept there as JSON. A text line at the end of the file that '
                  "is not a record is listed in Robinhood - Parsing Notes. Source File is the file's path within "
                  'the input; the same file can appear more than once in a production, and each copy is reported. '
                  'Layouts are those of synthetic files and one 2025 production; other production years and '
                  'layouts may differ.'),
        'paths': ('*_1099_*.csv',),
        'output_types': 'standard',
        'artifact_icon': 'file-text',
    },
    'robinhoodAccountMaster': {
        'name': 'Robinhood - Account Master',
        'description': 'Labelled fields read from an Account Master PDF.',
        'author': '@CyberMike81',
        'creation_date': '2026-09-23',
        'last_update_date': '2026-09-24',
        'requirements': 'pdfminer.six',
        'category': 'Robinhood Returns',
        'notes': ('Text is read from positions on the page (label rows, column positions, font sizes) observed in '
                  'the tested production. Location gives the page and the vertical position in points of the text '
                  'a row came from, and Source Text gives that text as read. Reader-detected unmapped text and '
                  'file-level PDF failures or unrecognised layouts are listed in Robinhood - Parsing Notes; this '
                  'does not establish complete extraction. Field is the label printed above the value. A label '
                  "outside the tested vocabulary is reported as '(unrecognized label) <label>' with its value, "
                  "and text that did not sit under a label as '(unlabelled text)'. When the printed UUID is cut "
                  'off, the full value is taken from the print footer URL and Location says so. Source File is '
                  "the file's path within the input; the same file can appear more than once in a production, and "
                  'each copy is reported. Layouts are those of synthetic files and one 2025 production; other '
                  'production years and layouts may differ. Account is blank when this PDF has no Account Number '
                  'in its Account Information section, including all edit-log fixture rows. Account is not '
                  'inferred from adjacent PDFs or shared folder names; review Source File and the original return '
                  'to establish attribution.'),
        'paths': ('*[Aa]ccount [Mm]aster*.pdf',),
        'output_types': 'standard',
        'artifact_icon': 'user',
    },
    'robinhoodAccountMasterEditLog': {
        'name': 'Robinhood - Account Master Edit Log',
        'description': 'Rows of the edit-log tables printed in an Account Master PDF.',
        'author': '@CyberMike81',
        'creation_date': '2026-09-23',
        'last_update_date': '2026-09-24',
        'requirements': 'pdfminer.six',
        'category': 'Robinhood Returns',
        'notes': ('Text is read from positions on the page (label rows, column positions, font sizes) observed in '
                  'the tested production. Location gives the page and the vertical position in points of the text '
                  'a row came from, and Source Text gives that text as read. Reader-detected unmapped text and '
                  'file-level PDF failures or unrecognised layouts are listed in Robinhood - Parsing Notes; this '
                  'does not establish complete extraction. Timestamp (UTC) is converted from the printed time and '
                  'zone abbreviation, read as a fixed North American offset (EST = UTC-5). Cells that wrap onto '
                  'more lines are joined to their record only when line spacing ties them to that record alone; '
                  'other wrapped text is listed in Unattached Text with no record fields, so it is never placed '
                  "on the wrong record. Unattached Text is empty for every other row. Source File is the file's "
                  'path within the input; the same file can appear more than once in a production, and each copy '
                  'is reported. Layouts are those of synthetic files and one 2025 production; other production '
                  'years and layouts may differ. Account is blank when this PDF has no Account Number in its '
                  'Account Information section, including all edit-log fixture rows. Account is not inferred from '
                  'adjacent PDFs or shared folder names; review Source File and the original return to establish '
                  'attribution.'),
        'paths': ('*[Aa]ccount [Mm]aster*.pdf',),
        'output_types': 'standard',
        'artifact_icon': 'edit',
    },
    'robinhoodStatements': {
        'name': 'Robinhood - Statements',
        'description': 'Statement periods and balances from brokerage and crypto statement PDFs.',
        'author': '@CyberMike81',
        'creation_date': '2026-09-23',
        'last_update_date': '2026-09-24',
        'requirements': 'pdfminer.six',
        'category': 'Robinhood Returns',
        'notes': ('RHF holdings are not mapped into the Holdings column. Source lines outside the header and '
                  'activity tables, including positions, are retained in Parsing Notes; repeated section titles '
                  'and page numbers are excluded. A warning identifies this limit. PDF layout checks used '
                  'pdfminer.six 20260107. Text is read from positions on the page (label rows, column positions, '
                  'font sizes) observed in the tested production. Location gives the page and the vertical '
                  'position in points of the text a row came from, and Source Text gives that text as read. '
                  'Reader-detected unmapped text and file-level PDF failures or unrecognised layouts are listed '
                  'in Robinhood - Parsing Notes; this does not establish complete extraction. Balances are the '
                  'printed values with $ and thousands separators removed and (x) written as -x; digits are not '
                  "rounded. Holdings lists the holdings table as printed. Statement is 'RHF brokerage statement' "
                  "or 'RHC crypto statement' by the statement's own layout. Account Basis says where Account came "
                  'from: printed on the statement, or taken from the file name when the pages print none (a '
                  "Parsing Notes row then says so). Source File is the file's path within the input; the same "
                  'file can appear more than once in a production, and each copy is reported. Layouts are those '
                  'of synthetic files and one 2025 production; other production years and layouts may differ. RHC '
                  "Account Number, Name (RHC), and Address (RHC) report the crypto statement's ACCOUNT NUMBER, "
                  'NAME, and ADDRESS labels; they are empty for RHF statements or missing labels. Account remains '
                  'the RHS number on RHC statements, as identified by Account Basis.'),
        'paths': ('*_account_statement_*.pdf', '*_rhc_statement_*.pdf'),
        'output_types': 'standard',
        'artifact_icon': 'book-open',
    },
    'robinhoodStatementActivity': {
        'name': 'Robinhood - Statement Activity',
        'description': 'Activity lines from brokerage and crypto statement PDFs.',
        'author': '@CyberMike81',
        'creation_date': '2026-09-23',
        'last_update_date': '2026-09-24',
        'requirements': 'pdfminer.six',
        'category': 'Robinhood Returns',
        'notes': ('Text is read from positions on the page (label rows, column positions, font sizes) observed in '
                  'the tested production. Location gives the page and the vertical position in points of the text '
                  'a row came from, and Source Text gives that text as read. Reader-detected unmapped text and '
                  'file-level PDF failures or unrecognised layouts are listed in Robinhood - Parsing Notes; this '
                  'does not establish complete extraction. Dates are calendar dates as printed, with no time or '
                  'zone. Quantities, prices and values have $ and thousands separators removed and (x) written as '
                  '-x; digits are not rounded. Debit and Credit are as printed. Account Basis says where Account '
                  'came from: printed on the statement, or taken from the file name when the pages print none (a '
                  "Parsing Notes row then says so). Source File is the file's path within the input; the same "
                  'file can appear more than once in a production, and each copy is reported. Layouts are those '
                  'of synthetic files and one 2025 production; other production years and layouts may differ.'),
        'paths': ('*_account_statement_*.pdf', '*_rhc_statement_*.pdf'),
        'output_types': 'standard',
        'artifact_icon': 'list',
    },
    'robinhoodParsingNotes': {
        'name': 'Robinhood - Parsing Notes',
        'description': ('Text in Robinhood PDFs and CSV exports that the readers could not place '
                        'as a record.'),
        'author': '@CyberMike81',
        'creation_date': '2026-09-23',
        'last_update_date': '2026-09-24',
        'requirements': 'pdfminer.six',
        'category': 'Robinhood Returns',
        'notes': ("One row per note. Level 'error' marks an unreadable PDF, with file name and exception type; "
                  "'warning' marks an unrecognised layout, missing account attribution, or text kept but not "
                  "mapped to a field; 'info' marks source lines outside mapped tables, layout observations and "
                  'text lines at the end of a CSV export (a notice line in the tested files), which are kept here '
                  'with their full text instead of being reported as records. An empty artifact means the readers '
                  "raised no notes, not that the files were fully understood. Source File is the file's path "
                  'within the input; the same file can appear more than once in a production, and each copy is '
                  'reported. Layouts are those of synthetic files and one 2025 production; other production years '
                  'and layouts may differ.'),
        'paths': ('*[Aa]ccount [Mm]aster*.pdf', '*_account_statement_*.pdf', '*_rhc_statement_*.pdf', '*crypto_account_transfers*.csv', '*crypto_account_orders*.csv', '*data_request_ip_timestamps*.csv', '*_1099_*.csv'),
        'output_types': 'standard',
        'artifact_icon': 'alert-triangle',
    },
}

import io
import json
import os
import re
import csv
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from scripts.ilapfuncs import artifact_processor, logfunc


# ==========================================================================
# PDF reading by @CyberMike81; contributed under the MIT license.
# Checked against the layouts of the tested production.
# ==========================================================================

# --------------------------------------------------------------------------
# Output schemas
# --------------------------------------------------------------------------
PROV = ["source", "locator", "account_basis", "raw"]

SCHEMAS = {
    "identity": ["provider", "account", "section", "field", "value"] + PROV,
    "events": ["provider", "account", "ts_utc", "ts_original", "tz_basis"] + PROV,
    "statements": ["provider", "account", "statement_type", "period_start", "period_end",
                   "opening_balance", "closing_balance", "holdings", "rhc_account", "name", "address"] + PROV,
    "statement_activity": ["provider", "account", "statement_type", "period_end", "date", "description",
                           "type", "symbol", "quantity", "price", "debit", "credit", "value", "fee"] + PROV,
    "other_records": ["provider", "account", "section", "record"] + PROV,
    "warnings": ["provider", "level", "message"] + PROV,
}

BASIS_STATED_OFFSET = "stated offset"


BASIS_STATED_ABBR = "stated zone abbreviation (fixed offset)"


BASIS_NOT_STATED = "zone not stated"


BASIS_UNPARSED = "unparsed"


def new_result():
    return {name: [] for name in SCHEMAS}


def row(table, **kw):
    """Build a row with the fixed key order for `table`; missing keys become ''."""
    return {k: ("" if kw.get(k) is None else kw.get(k)) for k in SCHEMAS[table]}


def warn(res, provider, message, source, locator="", level="warning", raw=""):
    res["warnings"].append(row("warnings", provider=provider, level=level, message=message,
                               source=source, locator=locator, raw=raw))


# --------------------------------------------------------------------------
# Text helpers
# --------------------------------------------------------------------------
def clean(v):
    if v is None:
        return ""
    s = str(v).replace("\r\n", "\n").replace("\r", "\n")
    s = "\n".join(" ".join(part.split()) for part in s.split("\n"))
    s = re.sub(r"\n{2,}", "\n", s).strip()
    return s


_NUM_RE = re.compile(r"^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?$")


def num(v):
    """
    Exact numeric text -> plain decimal string. '$1,234.50' -> '1234.50',
    '(12.34)' -> '-12.34', '1.23E-7' -> '0.000000123'. Digits after the point are kept as
    produced (no rounding, no trailing-zero trimming). Text that is not a plain number
    ('<0.01', '--', 'N/A') is returned as produced so qualifiers are never lost.
    """
    s = clean(v)
    if not s or s in ("--", "-"):
        return ""
    t, neg = s, False
    if t.startswith("(") and t.endswith(")"):
        neg, t = True, t[1:-1].strip()
    t = t.replace("$", "").replace(",", "").strip()
    m = _NUM_RE.match(t)
    if not m:
        return s
    if m.group(3) and abs(int(m.group(3)[1:])) > 64:   # absurd exponent: keep as produced
        return s
    return _plain_decimal(t, neg)


def _plain_decimal(t, neg=False):
    d = Decimal(t)                       # exact construction; no context rounding
    if neg:
        d = d.copy_negate()              # exact
    sign, digs, exp = d.as_tuple()
    ds = "".join(str(x) for x in digs) or "0"
    if exp >= 0:
        out = ds + "0" * exp
    else:
        k = -exp
        ds = ds.rjust(k + 1, "0")
        out = ds[:-k] + "." + ds[-k:]          # fraction digits kept as produced (5.30 stays 5.30)
    ip, dot, fp = out.partition(".")
    out = (ip.lstrip("0") or "0") + dot + fp
    if set(out) <= set("0."):
        return out                             # zero (any sign) is written without a sign
    return ("-" if sign else "") + out



# --------------------------------------------------------------------------
# Timestamps (locale-independent)
# --------------------------------------------------------------------------
_MONTHS = {m: i + 1 for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep",
                                           "oct", "nov", "dec"])}


# North American abbreviations read as fixed offsets. The stated abbreviation is trusted;
# no seasonal re-interpretation is applied.
_TZ_ABBR = {"PST": -8, "PDT": -7, "MST": -7, "MDT": -6, "CST": -6, "CDT": -5, "EST": -5, "EDT": -4,
            "AKST": -9, "AKDT": -8, "HST": -10, "UTC": 0, "GMT": 0, "Z": 0}


def _month(name):
    return _MONTHS.get(name.strip(".").lower()[:3])


def _hour12(h, ap):
    h = int(h)
    if ap:
        if not 1 <= h <= 12:
            raise ValueError("bad 12-hour value")
        h = (h % 12) + (12 if ap.lower() == "pm" else 0)
    return h


def parse_ts(value):
    """
    Returns (ts_utc, ts_original, tz_basis). ts_utc is 'YYYY-MM-DD HH:MM:SS[.fraction]' with the
    source's fractional digits kept exactly. Values without a zone remain unconverted.
    """
    orig = clean(value)
    if not orig:
        return "", "", ""
    s = orig
    try:
        y = mo = d = hh = mi = None
        ss, frac, tz, offset = 0, "", None, None
        m = re.match(r"^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2})(?::(\d{2})(?:\.(\d+))?)?\s*(Z|[+-]\d{2}:?\d{2})?$", s)
        if m:
            y, mo, d, hh, mi = (int(x) for x in m.group(1, 2, 3, 4, 5))
            ss, frac, z = int(m.group(6) or 0), m.group(7) or "", m.group(8)
            if z == "Z":
                offset = 0
            elif z:
                zz = z.replace(":", "")
                offset = (1 if zz[0] == "+" else -1) * (int(zz[1:3]) * 60 + int(zz[3:5]))
        if y is None:
            m = re.match(r"^([A-Za-z]+),?\s+(\d{1,2}),?\s+(\d{4})\s+(\d{1,2}):(\d{2})\s*([aApP][mM])\s+([A-Z]{1,4})$", s)
            if m and _month(m.group(1)):
                y, mo, d = int(m.group(3)), _month(m.group(1)), int(m.group(2))
                hh, mi, tz = _hour12(m.group(4), m.group(6)), int(m.group(5)), m.group(7)
        if y is None:
            m = re.match(r"^([A-Za-z]{3,9})\.? (\d{1,2}), (\d{4}),? (\d{1,2}):(\d{2})(?::(\d{2}))?\s*([aApP][mM])?\s*([A-Z]{1,4})?$", s)
            if m and _month(m.group(1)):
                y, mo, d = int(m.group(3)), _month(m.group(1)), int(m.group(2))
                hh, mi, ss = _hour12(m.group(4), m.group(7)), int(m.group(5)), int(m.group(6) or 0)
                tz = m.group(8)
        if y is None:
            m = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4}),?\s+(\d{1,2}):(\d{2})(?::(\d{2}))?\s*([aApP][mM])?\s*([A-Z]{1,4})?$", s)
            if m:
                mo, d, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
                hh, mi, ss = _hour12(m.group(4), m.group(7)), int(m.group(5)), int(m.group(6) or 0)
                tz = m.group(8)
        if y is None:
            return "", orig, BASIS_UNPARSED
        base = datetime(y, mo, d, hh, mi, ss)           # validates the calendar
    except (ValueError, TypeError):
        return "", orig, BASIS_UNPARSED
    fr = ("." + frac) if frac else ""
    if offset is not None:
        return (base - timedelta(minutes=offset)).strftime("%Y-%m-%d %H:%M:%S") + fr, orig, BASIS_STATED_OFFSET
    if tz:
        if tz not in _TZ_ABBR:
            return "", orig, f"zone '{tz}' not recognized"
        return (base - timedelta(hours=_TZ_ABBR[tz])).strftime("%Y-%m-%d %H:%M:%S") + fr, orig, BASIS_STATED_ABBR
    return "", orig, BASIS_NOT_STATED


def detect_pdf(pages) -> str:
    first = " ".join(s["t"] for p in pages[:2] for _, _, segs in p for s in segs)
    if "Accounts : Account Master" in first or "Accounts:Account Master" in first:
        return "rh_account_master"
    if "Crypto Statement" in first and "RHS ACCOUNT NUMBER" in first:
        return "rh_rhc_statement"
    if "Robinhood Securities" in first and "Account Summary" in first:
        return "rh_rhf_statement"
    return "document_pdf"


# ==========================================================================
# ROBINHOOD: CSVs
# ==========================================================================
def _rh_acct_from_name(source):
    m = re.search(r"account_number__(\d{6,})__", source) or \
        re.search(r"(?:^|/|> )(\d{8,10})_(?:account_statement|1099)", source)
    return m.group(1) if m else ""


class _QuietPdfminer:
    """Silence pdfminer's font warnings for the duration of a call, then restore the level."""

    def __enter__(self):
        import logging  # pylint: disable=import-outside-toplevel
        self.lg = logging.getLogger("pdfminer")  # pylint: disable=attribute-defined-outside-init
        self.level = self.lg.level  # pylint: disable=attribute-defined-outside-init
        self.lg.setLevel(logging.ERROR)
        return self

    def __exit__(self, *exc):
        self.lg.setLevel(self.level)
        return False


def pdf_rows(data: bytes):
    """
    Pages -> list of (top, size, segments) sorted by top; segment = {'x0','x1','t'}.
    Characters within 2pt of the same top form a row; a gap wider than
    max(3pt, 0.45 * font size) starts a new segment.
    """
    from pdfminer.high_level import extract_pages  # pylint: disable=import-outside-toplevel
    from pdfminer.layout import LAParams, LTChar  # pylint: disable=import-outside-toplevel

    def chars(o):
        for c in o:
            if isinstance(c, LTChar):
                yield c
            elif hasattr(c, "__iter__"):
                yield from chars(c)

    pages = []
    with _QuietPdfminer():
        for page in extract_pages(io.BytesIO(data), laparams=LAParams()):
            cs = sorted(chars(page), key=lambda c, _h=page.height: (round(_h - c.y1, 1), c.x0))
            lines = []
            for c in cs:
                top = page.height - c.y1
                if lines and abs(lines[-1][0] - top) <= 2.0:
                    lines[-1][1].append(c)
                else:
                    lines.append([top, [c]])
            prow = []
            for top, cc in sorted(lines, key=lambda l: l[0]):
                cc.sort(key=lambda c: (c.x0, c.y0))
                segs, cur = [], {}
                for c in cc:
                    t = c.get_text()
                    if cur and c.x0 - cur["x1"] <= max(3.0, 0.45 * c.size):
                        cur["t"] += t
                        cur["x1"] = max(cur["x1"], c.x1)
                    else:
                        if cur:
                            segs.append(cur)
                        cur = {"x0": round(c.x0, 1), "x1": round(c.x1, 1), "t": t}
                if cur:
                    segs.append(cur)
                out = []
                for s in segs:
                    s["t"] = " ".join(s["t"].replace("ﬁ", "fi").replace("ﬂ", "fl").split())
                    s["x1"] = round(s["x1"], 1)
                    if s["t"]:
                        out.append(s)
                if out:
                    prow.append((round(top, 1), round(cc[0].size, 1), out))
            pages.append(prow)
    return pages


def _row_text(segs):
    return " ".join(s["t"] for s in segs)


def _ploc(pno, top):
    return f"page {pno + 1}, y {top:.0f}"


def _join_wrapped(parts):
    out = ""
    for p in parts:
        out = p if not out else (out + p if out.endswith("-") else out + " " + p)
    return out


def _assign_columns(header_segs, segs):
    """Nearest header centre (for centred / right-aligned statement tables)."""
    centres = [((h["x0"] + h["x1"]) / 2, h["t"]) for h in header_segs]
    out = {h["t"]: [] for h in header_segs}
    for s in segs:
        c = (s["x0"] + s["x1"]) / 2
        best = min(centres, key=lambda hc, _c=c: (abs(hc[0] - _c), hc[0]))
        out[best[1]].append(s["t"])
    return {k: " ".join(v) for k, v in out.items()}


def _assign_nearest_left(header_segs, segs):
    out = {h["t"]: [] for h in header_segs}
    for s in segs:
        best = min(header_segs, key=lambda h, _x=s["x0"]: (abs(h["x0"] - _x), h["x0"]))
        out[best["t"]].append(s["t"])
    return {k: " ".join(v) for k, v in out.items()}


def _assign_left(header_segs, segs, slack=4.0):
    hs = sorted(header_segs, key=lambda h: h["x0"])
    out = {h["t"]: [] for h in hs}
    for s in segs:
        target = hs[0]
        for h in hs:
            if s["x0"] >= h["x0"] - slack:
                target = h
        out[target["t"]].append(s["t"])
    return {k: " ".join(v) for k, v in out.items()}


def _wrapped_table(rows, header, key_col, res, provider, source, what):
    """
    Rows (pno, top, size, segs) of a left-aligned table whose cells can wrap onto lines
    above and below the main line. A main line has a value in key_col and at least one
    other cell. A wrapped line is attached to a record only when it is chained to that
    record's main line by line-height steps (each step <= 2.2 x font size) and not also
    chained to a neighbouring record. Anything else is not attached: it is returned in
    `loose`, flagged with a warning naming the neighbouring records, and never merged
    into a record by guesswork.
    Returns (records, loose): records = [(cells, locator, raw_text)],
    loose = [(locator, text)].
    """
    lines = []
    for pno, top, size, segs in rows:
        cells = _assign_nearest_left(header, segs)
        filled = [k for k, v in cells.items() if v]
        g = pno * 2000 + top
        is_main = bool(cells.get(key_col)) and len(filled) >= 2
        lines.append({"g": g, "cells": cells, "loc": _ploc(pno, top), "text": _row_text(segs), "main": is_main,
                      "step": 2.2 * (size or 6.3), "owner": None})
    lines.sort(key=lambda l: l["g"])
    mains = [k for k, l in enumerate(lines) if l["main"]]
    for mi, k in enumerate(mains):
        lines[k]["owner"] = mi
    claims = {}                                        # line index -> set of main indexes
    for mi, k in enumerate(mains):
        for direction in (-1, 1):
            j, prev = k + direction, lines[k]
            while 0 <= j < len(lines) and not lines[j]["main"]:
                if abs(lines[j]["g"] - prev["g"]) > max(prev["step"], lines[j]["step"]):
                    break
                claims.setdefault(j, set()).add(mi)
                prev = lines[j]
                j += direction
    loose = []
    for j, l in enumerate(lines):
        if l["main"]:
            continue
        c = claims.get(j, set())
        if len(c) == 1:
            l["owner"] = next(iter(c))
        else:
            before = [lines[k]["loc"] for k in mains if lines[k]["g"] < l["g"]][-1:]
            after = [lines[k]["loc"] for k in mains if lines[k]["g"] > l["g"]][:1]
            near = " and ".join(before + after) or "no record"
            why = "could belong to either neighbouring record" if c else "is not joined to any record by line spacing"
            warn(res, provider, f"{what}: wrapped text {why}; not attached (records near: {near})", source,
                 l["loc"], raw=l["text"])
            loose.append((l["loc"], l["text"]))
    out = []
    for mi, k in enumerate(mains):
        m = lines[k]
        mine = [l for l in lines if l["owner"] == mi]
        merged = {key: _join_wrapped([l["cells"].get(key, "") for l in mine if l["cells"].get(key, "")])
                  for key in m["cells"]}
        out.append((merged, m["loc"], "\n".join(l["text"] for l in mine)))
    return out, loose


# ==========================================================================
# ROBINHOOD: Account Master PDF
# ==========================================================================
AM_LABELS = {
    "First Name", "Last Name", "Has Mononym", "Email", "Phone Number", "Number of Dependents",
    "Citizenship", "Marital Status", "Date of Birth (DOB)", "Date of Death (DOD)", "Account Number",
    "UUID", "Account Status", "Account Type", "Customer Account Type", "Subject", "Line1", "Line2",
    "City", "State", "Postal Code", "Country", "ID Type", "Value", "Status", "Occupation", "Employer",
    "Industry", "Updated At", "Updated at", "Updated By", "Requires tax form resubmission", "Is nonresident alien",
    "Certified at", "Subjected to backup tax withholding", "Permanent residential address country",
    "Permanent residential address", "Letter of explanation", "Other letter of explanation",
    "Claims treaty benefits", "Address Line 1", "Address Line 2", "Is politically exposed person",
    "Signed", "Signed At", "Suitability completed", "Has Investment Experience",
    "Passes Risk Tolerance Check", "Interested in options", "Employment", "Employment Status", "Employer address",
    "Professional trader", "Options experience", "Mark Type", "SSN", "Address", "Locality", "Region",
    "Approved By", "Approved At", "Is Control Person", "Security Symbol",
    "Is eligible to participate in IPO Access", "Is IPO Access Restricted Person",
    "IPO Access Restricted Reason", "Is Security Affiliated", "Affiliated Person Name",
    "Affiliated Person Relationship", "Firm Name", "Affiliate Attention", "Affiliate Line 1",
    "Affiliate Line 2", "Affiliate City", "Affiliate State", "Affiliate Postal Code",
    "Object To Disclosure", "Object To Class Actions", "Robinhood Employee", "Heightened Supervision",
    "Is Large Trader", "Created At", "Margin Allowed", "Rejected At", "Rejected By",
    "Automatically Approved", "Automatically Rejected", "Manual Review Assignee",
}


AM_SECTION_SIZE = 9.0      # section headings 10.2pt; labels/values 6.3pt


AM_SUBHEAD_SIZE = 7.0      # sub-headings 7.3pt (only when not consumed as a value)


AM_VALUE_GAP = 25.0        # a value row sits ~18pt under its label row


AM_UI_TEXT = {"Edit", "Clear email", "Show Unredacted Values", "Refresh", "Previous", "Next", "Expand",
              "Fetch estate", "Add Estate", "Add Trust", "Enroll", "Restrict", "Request a new Tax Form"}


def _is_label_row(segs):
    labels = [s for s in segs if s["t"] in AM_LABELS]
    return bool(labels) and len(labels) >= max(1, len(segs) // 2)


def _looks_like_values_for(label_segs, segs):
    """Value boxes are inset ~6pt right of their label; a row that starts there is values."""
    return any(l["x0"] + 3 <= segs[0]["x0"] <= l["x0"] + 10 for l in label_segs)


def _strip_print_chrome(pages):
    """Flatten to (pno, top, size, segs) and drop the browser print header/footer rows."""
    out, urls = [], []
    for pno, p in enumerate(pages):
        for top, size, segs in p:
            txt = _row_text(segs)
            if re.match(r"^\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2} [AP]M", txt) and "Major Oak" in txt:
                continue
            if txt.startswith("https://oak.robinhood.com/"):
                urls.append(segs[0]["t"])
                continue
            out.append((pno, top, size, segs))
    return out, urls


_EDIT_TITLE = re.compile(r"^\S.*\bedit logs\b")


def parse_rh_account_master(pages, source):
    """
    Browser print of the Robinhood 'Major Oak' Account Master page. Every non-chrome text item
    ends up as a mapped field, an '(unrecognized label)' field with its value, an
    '(unlabelled text)' item, an edit-log record, or a warning. Nothing is dropped silently.
    """
    res = new_result()
    P = "Robinhood"
    rows, urls = _strip_print_chrome(pages)
    last_on_page = {}
    for k, (pno, _, _, _) in enumerate(rows):
        last_on_page[pno] = k
    fields = []            # (section, label, value, locator, raw)
    section = major = ""
    unl, unknown_labels = 0, 0
    edit_blocks = []
    i = 0

    def adjacent(k):
        p0, t0, _, _ = rows[k]
        p1, t1, _, _ = rows[k + 1]
        return (p1 == p0 and 0 < t1 - t0 <= AM_VALUE_GAP) or (p1 == p0 + 1 and last_on_page.get(p0) == k)

    def value_row_ok(k, col_segs):
        if k + 1 >= len(rows) or not adjacent(k):
            return False
        _, _, s1, nsegs = rows[k + 1]
        if s1 >= AM_SECTION_SIZE or nsegs[0]["t"] == "Agreement Type" or _EDIT_TITLE.match(_row_text(nsegs)):
            return False
        return (not _is_label_row(nsegs)) or _looks_like_values_for(col_segs, nsegs)

    while i < len(rows):
        pno, top, size, segs = rows[i]
        txt = _row_text(segs)
        if _EDIT_TITLE.match(txt):
            j = i + 1
            while j < len(rows):
                t2 = _row_text(rows[j][3])
                if rows[j][2] >= AM_SECTION_SIZE and not _EDIT_TITLE.match(t2):
                    break
                j += 1
            edit_blocks.append(rows[i:j])
            i = j
            continue
        if segs[0]["t"] == "Agreement Type" and len(segs) >= 3:
            j = i + 1
            body = []
            while j < len(rows):
                _, _, s2, sg2 = rows[j]
                if s2 >= AM_SECTION_SIZE or _is_label_row(sg2) or sg2[0]["t"] == "Agreement Type" \
                        or (s2 >= AM_SUBHEAD_SIZE and len(sg2) == 1) or _EDIT_TITLE.match(_row_text(sg2)):
                    break
                body.append(rows[j])
                j += 1
            recs, loose = _wrapped_table(body, segs, "Agreement Type", res, P, source, "Agreements table")
            for cells, lc, rawt in recs:
                val = "; ".join(f"{k.lower()}: {v}" for k, v in cells.items() if k != "Agreement Type" and v)
                fields.append((section, cells["Agreement Type"], val, lc, rawt))
            for lc, t in loose:
                unl += 1
                fields.append((section, "(unlabelled text)", t, lc, t))
            i = j
            continue
        if _is_label_row(segs) and size < AM_SECTION_SIZE:
            cols = [s for s in segs if s["t"] not in AM_UI_TEXT]          # known AND unknown labels are columns
            vals, rawt, vloc = {}, txt, _ploc(pno, top)
            if value_row_ok(i, cols):
                p1, t1, _, nsegs = rows[i + 1]
                nsegs = [s for s in nsegs if s["t"] not in AM_UI_TEXT]
                vals = _assign_left(cols, nsegs) if nsegs else {}
                rawt = txt + "\n" + _row_text(rows[i + 1][3])
                vloc = f"{_ploc(pno, top)} to {_ploc(p1, t1)}"
                i += 1
            for s in cols:
                if s["t"] in AM_LABELS:
                    fields.append((section, s["t"], clean(vals.get(s["t"], "")), vloc, rawt))
                else:
                    unknown_labels += 1
                    fields.append((section, f"(unrecognized label) {s['t']}", clean(vals.get(s["t"], "")), vloc, rawt))
            i += 1
            continue
        if size >= AM_SECTION_SIZE:
            major = re.sub(r"\s+(Edit|V2|Expand)$", "", segs[0]["t"]).strip()
            section = major
            rest = " ".join(s["t"] for s in segs[1:] if s["t"] not in AM_UI_TEXT)
            if rest:
                unl += 1
                fields.append((section, "(unlabelled text)", rest, _ploc(pno, top), txt))
            i += 1
            continue
        if size >= AM_SUBHEAD_SIZE and len(segs) == 1:
            section = f"{major} / {segs[0]['t']}" if major else segs[0]["t"]
            i += 1
            continue
        keep = [s for s in segs if s["t"] not in AM_UI_TEXT]
        # an unknown label row: a line whose next line starts inside its value box
        if keep and i + 1 < len(rows) and adjacent(i) and rows[i + 1][2] < AM_SUBHEAD_SIZE \
                and _looks_like_values_for(keep, rows[i + 1][3]) and not _is_label_row(rows[i + 1][3]):
            p1, t1, _, nsegs = rows[i + 1]
            nsegs = [s for s in nsegs if s["t"] not in AM_UI_TEXT]
            vals = _assign_left(keep, nsegs) if nsegs else {}
            for s in keep:
                unknown_labels += 1
                fields.append((section, f"(unrecognized label) {s['t']}", clean(vals.get(s["t"], "")),
                               f"{_ploc(pno, top)} to {_ploc(p1, t1)}", txt + "\n" + _row_text(rows[i + 1][3])))
            i += 2
            continue
        if keep:
            unl += 1
            fields.append((section, "(unlabelled text)", " ".join(s["t"] for s in keep), _ploc(pno, top), txt))
        i += 1

    def first(label, sec=None):
        for s_, l, v, _, _ in fields:
            if l == label and v and (sec is None or s_ == sec):
                return v
        return ""

    acct = first("Account Number", "Account Information")
    uuid = first("UUID")
    uuid_note = ""
    for u in urls:  # the on-screen UUID can be cut off; the print footer URL carries it whole
        m = re.search(r"/master/v\d+/([0-9a-f-]{36})", u)
        if m and uuid and m.group(1).startswith(uuid[:8]) and m.group(1) != uuid:
            uuid, uuid_note = m.group(1), u
            break
    AB = "stated in file (Account Master)" if acct else ""
    seen = set()
    for sec, lab, val, lc, rawt in fields:
        key = (sec, lab)
        if key in seen and not val and not lab.startswith("("):
            continue
        seen.add(key)
        if lab == "UUID" and uuid:
            val = uuid
            if uuid_note:
                lc, rawt = lc + "; full value from print footer URL", rawt + "\n" + uuid_note
        res["identity"].append(row("identity", provider=P, account=acct, section=sec, field=lab, value=val,
                                   source=source, locator=lc, account_basis=AB, raw=rawt))
    if unl:
        warn(res, P, f"Account Master: {unl} text item(s) did not match a known label layout; kept as "
                     f"'(unlabelled text)' in Robinhood - Account Master", source)
    if unknown_labels:
        warn(res, P, f"Account Master: {unknown_labels} label(s) not in the known vocabulary; kept as "
                     f"'(unrecognized label)' fields with their values", source)

    if not acct:
        warn(res, P, "Account Master: Account is blank because no Account Number was found in "
             "this PDF's Account Information section; no account is inferred from other files", source)
    for block in edit_blocks:
        _rh_edit_logs(block, acct, res, source, AB)
    return res


def _rh_edit_logs(rows, acct, res, source, account_basis):
    """Edit-log tables: header 'Model Field Previous Value New Value Author Timestamp'."""
    P = "Robinhood"
    blocks, cur = [], None
    for pno, top, size, segs in rows:
        txt = _row_text(segs)
        if txt.startswith("Brokeback edit logs") or txt.startswith("Identi edit logs"):
            cur = [txt.split(" edit logs")[0] + " edit log", None, []]
            blocks.append(cur)
            continue
        if cur is None:
            continue
        if [s["t"] for s in segs][:2] == ["Model", "Field"]:
            if cur[1] is None:
                cur[1] = segs
            continue                      # repeated header on a later page
        if cur[1] is None:
            if not all(s["t"] in AM_UI_TEXT for s in segs):
                warn(res, P, f"{cur[0]}: text before the table header", source, _ploc(pno, top), raw=txt)
            continue
        if txt not in ("Previous Next",) and not all(s["t"] in AM_UI_TEXT for s in segs):
            cur[2].append((pno, top, size, segs))
    for log_name, header, body in blocks:
        if header is None:
            continue
        recs, loose = _wrapped_table(body, header, "Model", res, P, source, log_name)
        for lc, t in loose:
            res["other_records"].append(row("other_records", provider=P, account=acct,
                                            section=f"{log_name} (text not attached to a record)", record=t,
                                            source=source, locator=lc, account_basis=account_basis, raw=t))
        for c, lc, rawt in recs:
            field, prev = c.get("Field", ""), c.get("Previous Value", "")
            m = re.match(r"^(\S+?)(--)$", field)
            if m and not prev:
                field, prev = m.group(1), "--"
            author, stamp = c.get("Author", ""), c.get("Timestamp", "")
            m = re.match(r"^(\S+@\S+?\.[A-Za-z]{2,24})((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* "
                         r"\d{1,2}, \d{4}.*)$", author)
            if m and not stamp:
                author, stamp = m.group(1), m.group(2)
            u, o, b = parse_ts(stamp)
            rec = row(
                "events", provider=P, account=acct, ts_utc=u, ts_original=o, tz_basis=b,
                source=source, locator=lc, account_basis=account_basis, raw=rawt)
            rec["edit"] = {"log": log_name, "model": c.get("Model", ""), "field": field, "previous": prev,
                           "new": c.get("New Value", ""), "author": author}     # fields kept apart for RLEAPP
            res["events"].append(rec)


# ==========================================================================
# ROBINHOOD: statements
# ==========================================================================
RHC_KV_LABELS = ("NAME", "ACCOUNT NUMBER", "RHS ACCOUNT NUMBER", "ADDRESS", "PERIOD START",
                 "PERIOD END", "OPENING BALANCE", "CLOSING BALANCE")


def parse_rh_rhc_statement(pages, source):
    res = new_result()
    P = "Robinhood"
    kv, kvloc = {}, {}
    holdings, activity = [], []
    for pno, p in enumerate(pages):
        # labels and values use different font sizes, so they are paired by the vertical centre
        # of their lines (within 4pt; 0.8pt apart in the tested production, labels 19.5pt apart)
        labels = [(top, top + size / 2, s) for top, size, segs in p for s in segs
                  if s["x0"] < 100 and s["t"] in RHC_KV_LABELS]
        if labels:
            last = None
            stop = max(t for t, _, _ in labels) + 4.0
            first_top = min(t for t, _, _ in labels) - 4.0
            for top, size, segs in p:
                if top > stop + 40:
                    break
                centre = top + size / 2
                for s in segs:
                    if s["x0"] < 120:
                        continue
                    lab = next((l["t"] for _, lc_, l in labels if abs(lc_ - centre) <= 4.0), None)
                    if lab:
                        kv[lab] = s["t"] if lab not in kv else kv[lab] + " " + s["t"]
                        kvloc.setdefault(lab, []).append(_ploc(pno, top))
                        last = lab
                    elif last and top > first_top:
                        kv[last] = kv[last] + ", " + s["t"]
                        kvloc.setdefault(last, []).append(_ploc(pno, top))
        hold_hdr = act_hdr = None
        for top, _, segs in p:
            txt = _row_text(segs)
            if txt.startswith("This statement is provided") or "which can be found here" in txt:
                continue
            if segs[0]["t"] == "CRYPTOCURRENCY HELD IN ACCOUNT":
                hold_hdr, act_hdr = segs, None
                continue
            if segs[0]["t"] == "DATE" and any(s["t"] == "TRANSACTION TYPE" for s in segs):
                act_hdr, hold_hdr = segs, None
                continue
            if txt in ("ACCOUNT ACTIVITY", "PORTFOLIO ALLOCATION") or txt.startswith("*"):
                hold_hdr = None
                continue
            if hold_hdr and len(segs) >= 3:
                holdings.append((_assign_columns(hold_hdr, segs), _ploc(pno, top), txt))
                continue
            if act_hdr:
                if re.match(r"\d{4}-\d{2}-\d{2}$", segs[0]["t"]):
                    activity.append((_assign_columns(act_hdr, segs), _ploc(pno, top), txt))
                elif activity:
                    warn(res, P, "RHC activity: line without a date; kept in raw of the previous row", source,
                         _ploc(pno, top), raw=txt)
                    a, lc, t = activity[-1]
                    activity[-1] = (a, lc, t + "\n" + txt)
    acct_rhs = kv.get("RHS ACCOUNT NUMBER", "")
    acct_rhc = kv.get("ACCOUNT NUMBER", "")
    pend = kv.get("PERIOD END", "")
    missing = [k for k in ("ACCOUNT NUMBER", "RHS ACCOUNT NUMBER", "PERIOD END") if not kv.get(k)]
    if missing:
        warn(res, P, "RHC statement: no value found for " + ", ".join(missing), source)
    AB = "stated in file (RHS ACCOUNT NUMBER)" if acct_rhs else ""
    kv_raw = json.dumps([[k, v] for k, v in kv.items()], ensure_ascii=False)
    kv_loc = "; ".join(f"{k} at {', '.join(v)}" for k, v in kvloc.items())

    def mv(h):
        return next((v for k, v in h.items() if k.startswith("MARKET VALUE")), "")

    hold_txt = "; ".join(f"{h.get('SYMBOL', '')} {h.get('QUANTITY', '')} ({mv(h)})" for h, _, _ in holdings)
    res["statements"].append(row("statements", provider=P, account=acct_rhs, statement_type="RHC crypto statement",
                                 period_start=kv.get("PERIOD START"), period_end=pend,
                                 rhc_account=acct_rhc, name=kv.get("NAME"), address=kv.get("ADDRESS"),
                                 opening_balance=num(kv.get("OPENING BALANCE")),
                                 closing_balance=num(kv.get("CLOSING BALANCE")), holdings=hold_txt, source=source,
                                 locator=kv_loc + ("; holdings at " + ", ".join(lc for _, lc, _ in holdings)
                                                   if holdings else ""),
                                 account_basis=AB,
                                 raw=kv_raw + ("\n" + "\n".join(t for _, _, t in holdings) if holdings else "")))
    for a, lc, t in activity:
        res["statement_activity"].append(row(
            "statement_activity", provider=P, account=acct_rhs, statement_type="RHC crypto statement",
            period_end=pend, date=a.get("DATE"), description=a.get("TRANSACTION TYPE"), type=a.get("TRANSACTION TYPE"),
            debit=_dash(a.get("DEBIT")), credit=_dash(a.get("CREDIT")), price=num(a.get("PRICE")),
            value=num(a.get("VALUE")), fee=_dash(a.get("FEE", "")), source=source, locator=lc, account_basis=AB, raw=t))
    return res


def _dash(v):
    v = clean(v)
    return "" if v in ("--", "-") else v


# Section titles repeated on RHF statements. They are not holdings and are not kept as records.
_RHF_CHROME = {
    "Account Summary", "Account Activity", "Portfolio Summary",
    "Executed Trades Pending Settlement", "Income and Expense",
    "Robinhood Securities, LLC", "Robinhood Securities",
}


def parse_rh_rhf_statement(pages, source):
    """
    RHF monthly statement. Reads the header (account, period, portfolio value), the Account
    Activity table and the Executed Trades Pending Settlement table. Every other line is kept
    in Other records. The holdings column is left blank: this layout's positions are not mapped
    into it, and the warning says so.
    """
    res = new_result()
    P = "Robinhood"
    acct = period_start = period_end = ""
    opening = closing = ""
    hdr, kind, hdr_size = None, "", None
    lines = []                           # [kind, cells, locator, rawtext]
    hdr_src = []
    unmapped = []                        # (locator, text) outside the header and activity tables

    def keep_unmapped(pno, top, txt):
        if not txt or txt in _RHF_CHROME or re.fullmatch(r"Page \d+ of \d+", txt):
            return
        unmapped.append((_ploc(pno, top), txt))

    for pno, p in enumerate(pages):
        for top, size, segs in p:
            txt = _row_text(segs)
            header_hit = False
            m = re.search(r"Account #:\s*(\d+)", txt)
            if m and not acct:
                acct = m.group(1)
                hdr_src.append((_ploc(pno, top), txt))
                header_hit = True
            m = re.search(r"(\d{2}/\d{2}/\d{4}) to (\d{2}/\d{2}/\d{4})", txt)
            if m and not period_end:
                period_start, period_end = _mdy(m.group(1)), _mdy(m.group(2))
                hdr_src.append((_ploc(pno, top), txt))
                header_hit = True
            if segs[0]["t"] == "Portfolio Value" and len(segs) >= 3 and not opening:
                opening, closing = num(segs[1]["t"]), num(segs[2]["t"])
                hdr_src.append((_ploc(pno, top), txt))
                header_hit = True
            names = [s["t"] for s in segs]
            if names and names[0] == "Description" and "Debit" in names:
                hdr, hdr_size = segs, size
                kind = "pending settlement" if "Trade Date" in names else "activity"
                continue
            if hdr is None:
                if not header_hit:
                    keep_unmapped(pno, top, txt)
                continue
            if re.fullmatch(r"Page \d+ of \d+", txt):
                continue
            if txt.startswith("Total ") or size > hdr_size + 0.8:
                keep_unmapped(pno, top, txt)   # table total or the heading that ended the table
                hdr = None
                continue
            cells = _assign_columns(hdr, segs)
            date_col = "Date" if kind == "activity" else "Trade Date"
            if re.search(r"\d{2}/\d{2}/\d{4}", cells.get(date_col, "")):
                lines.append([kind, cells, _ploc(pno, top), txt])
                continue
            others = [k for k, v in cells.items() if v and k != "Description"]
            desc_col = next(h for h in hdr if h["t"] == "Description")
            next_col_x = min((h["x0"] for h in hdr if h["x0"] > desc_col["x0"]), default=9999)
            if lines and lines[-1][0] == kind and not others and segs[0]["x0"] < next_col_x:
                lines[-1][1]["Description"] = (lines[-1][1].get("Description", "") + " " + cells["Description"]).strip()
                lines[-1][3] += "\n" + txt
            else:
                warn(res, P, f"RHF {kind} table: line could not be read as a record; kept in Other records",
                     source, _ploc(pno, top), raw=txt)
                res["other_records"].append(row("other_records", provider=P, section=f"RHF statement {kind} "
                                                f"(unparsed line)", record=txt, source=source,
                                                locator=_ploc(pno, top), raw=txt))
    AB = "stated in file (Account #)"
    if not acct:
        acct = _rh_acct_from_name(source)
        AB = "from file name" if acct else ""
        warn(res, P, "RHF statement: no 'Account #' found on the pages; " +
             ("account taken from the file name" if acct else "account left blank"), source)
    for lc, txt in unmapped:
        res["other_records"].append(row(
            "other_records", provider=P, section="RHF statement (not mapped to holdings or activity)",
            record=txt, source=source, locator=lc, raw=txt))
    warn(res, P, "RHF statement: holdings are not mapped to the holdings column. " +
         (f"{len(unmapped)} other line(s) kept in Other records." if unmapped else
          "No other statement lines were found outside the header and activity tables."), source)
    for r in res["other_records"]:
        r["account"], r["account_basis"] = acct, AB
    res["statements"].append(row("statements", provider=P, account=acct, statement_type="RHF brokerage statement",
                                 period_start=period_start, period_end=period_end, opening_balance=opening,
                                 closing_balance=closing, source=source,
                                 locator="; ".join(lc for lc, _ in hdr_src) or "page 1", account_basis=AB,
                                 raw="\n".join(t for _, t in hdr_src)))
    for kind, c, lc, t in lines:
        pending = kind == "pending settlement"
        res["statement_activity"].append(row(
            "statement_activity", provider=P, account=acct,
            statement_type="RHF brokerage statement" + (" (executed, pending settlement)" if pending else ""),
            period_end=period_end, date=_mdy(c.get("Trade Date" if pending else "Date", "")),
            description=c.get("Description", "") + (f" (settle {c.get('Settle Date', '')})" if pending else ""),
            type=c.get("Transaction"), symbol=c.get("Symbol", ""), quantity=num(c.get("Qty")), price=num(c.get("Price")),
            debit=num(c.get("Debit")), credit=num(c.get("Credit")), source=source, locator=lc, account_basis=AB,
            raw=t))
    return res


def _mdy(v):
    m = re.match(r"^(\d{2})/(\d{2})/(\d{4})$", clean(v))
    return f"{m.group(3)}-{m.group(1)}-{m.group(2)}" if m else clean(v)


# ==========================================================================
# RLEAPP artifacts
# ==========================================================================
_PDF_KINDS = {"rh_account_master": parse_rh_account_master, "rh_rhc_statement": parse_rh_rhc_statement,
              "rh_rhf_statement": parse_rh_rhf_statement}
_PDF_CACHE = {}


def _aware(utc_text):
    """'YYYY-MM-DD HH:MM:SS[.fraction]' (already UTC) -> aware datetime; '' stays ''."""
    if not utc_text:
        return ""
    main, _, frac = utc_text.partition(".")
    value = datetime.strptime(main, "%Y-%m-%d %H:%M:%S")
    if frac:
        value = value.replace(microsecond=int(frac[:6].ljust(6, "0")))
    return value.replace(tzinfo=timezone.utc)


def _parsed_pdfs(context, kinds=None):
    """Matched PDFs, including file-level notes; kinds=None also returns failed/unknown files."""
    from pdfminer.pdfparser import PDFException  # pylint: disable=import-outside-toplevel

    out = []
    for file_found in sorted(str(f) for f in context.get_files_found()):
        if not file_found.lower().endswith(".pdf"):
            continue
        # A failed stat/read must be file-local too. Do not cache failures lacking a stat.
        key = None
        try:
            stat = os.stat(file_found)
            key = (file_found, stat.st_size, stat.st_mtime_ns)
            if key in _PDF_CACHE:
                kind, result = _PDF_CACHE[key]
            else:
                with open(file_found, "rb") as handle:
                    data = handle.read()
                pages = pdf_rows(data)
                kind = detect_pdf(pages)
                if kind in _PDF_KINDS:
                    result = _PDF_KINDS[kind](pages, file_found)
                else:
                    result = new_result()
                    message = (f"{os.path.basename(file_found)}: PDF layout not recognised by the "
                               "Robinhood readers; no structured records extracted. "
                               "PDF tax statements are not supported; review the source PDF.")
                    warn(result, "Robinhood", message, file_found, "whole document")
                    logfunc(f"Robinhood: {message}")
        except (PDFException, OSError, ValueError, TypeError, KeyError, IndexError) as err:
            kind, result = "unreadable_pdf", new_result()
            # Exception messages can contain machine-local paths; name the file and error type.
            message = f"{os.path.basename(file_found)}: could not read PDF ({type(err).__name__}); no records extracted"
            warn(result, "Robinhood", message, file_found, "whole document", level="error")
            logfunc(f"Robinhood: {message}")
        if key is not None:
            if len(_PDF_CACHE) >= 64 and key not in _PDF_CACHE:
                _PDF_CACHE.clear()
            _PDF_CACHE[key] = (kind, result)
        if kinds is None or kind in kinds:
            out.append((file_found, kind, result))
    return out


def _read_csv(path):
    """(header, [(csv_record_number, cells)], footers). Record numbers count CSV records, header = 1.
    A footer is a trailing record after the last multi-cell record that holds one long text cell
    (the exports end with a notice line); footers are not records and are listed in Parsing Notes."""
    with open(path, "rb") as handle:
        data = handle.read()
    for enc in ("utf-8-sig", "cp1252"):
        try:
            text = data.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        text = data.decode("latin-1")
    rows = list(csv.reader(io.StringIO(text, newline="")))
    if not rows:
        return [], [], []
    header = [h.strip() for h in rows[0]]
    body = [(i, r) for i, r in enumerate(rows[1:], start=2) if any(c.strip() for c in r)]
    last_multi = max((k for k, (_, r) in enumerate(body) if sum(1 for c in r if c.strip()) > 1), default=-1)
    footers = [(i, r) for k, (i, r) in enumerate(body)
               if k > last_multi and len(header) > 2 and r and r[0].strip() and len(r[0].strip()) > 40
               and sum(1 for c in r if c.strip()) == 1]
    footer_numbers = {i for i, _ in footers}
    return header, [(i, r) for i, r in body if i not in footer_numbers], footers


def _csv_artifact(context, columns, required, utc_from=None):
    """Rows of one CSV export, columns as produced. A file is used only when its header holds
    every column in `required`."""
    headers = []
    if utc_from:
        headers += [("Timestamp (UTC)", "datetime"), "Time Basis"]
    headers += list(columns) + ["Other Columns (as produced)", "CSV Record", "Source File"]
    rows, sources = [], set()
    for file_found in sorted(str(f) for f in context.get_files_found()):
        if not os.path.isfile(file_found):
            continue
        try:
            header, body, _ = _read_csv(file_found)
        except (OSError, csv.Error) as err:
            logfunc(f"Robinhood: could not read {os.path.basename(file_found)}: {err}")
            continue
        if not all(c in header for c in required):
            continue
        for number, cells in body:
            rec = {header[i]: cells[i].strip() if i < len(cells) else "" for i in range(len(header))}
            extra = {(header[i] if i < len(header) and header[i] else f"(column {i + 1})"): c.strip()
                     for i, c in enumerate(cells) if c.strip() and (i >= len(header) or header[i] not in columns)}
            line = []
            if utc_from:
                utc, _, basis = parse_ts(rec.get(utc_from, ""))
                line += [_aware(utc), basis]
            line += [rec.get(c, "") for c in columns]
            line += [json.dumps(extra, ensure_ascii=False) if extra else "", number,
                     context.get_relative_path(file_found)]
            rows.append(line)
            sources.add(file_found)
    return tuple(headers), rows, "\n".join(sorted(sources))


_TRANSFER_COLUMNS = ("id", "created_at", "withdrawal_submitted_timestamp", "currency_code", "transfer_type",
                     "amount", "network", "network_fee", "native_network_fee", "usd_amount_at_request",
                     "fiat_amount_at_request", "state", "to_address", "address_tag", "blockchain_txn_id",
                     "blockchain_txn_state")
_ORDER_COLUMNS = ("Time Entered", "UUID", "Symbol", "Side", "Quantity", "State", "Order Type", "Leaves Quantity",
                  "Entered Price", "Average Price", "Notional")
_IPLOG_COLUMNS = ("event_date_time", "account_number", "user__secret", "user__username", "device_platform",
                  "user_agent", "client_ip", "geo_ip", "geo_ip_timezone", "geo_ip_city_name", "geo_ip_country_name")
_1099_COLUMNS = ("1099-B", "ACCOUNT NUMBER", "TAX YEAR", "DATE ACQUIRED", "SALE DATE", "DESCRIPTION", "SHARES",
                 "COST BASIS", "SALES PRICE", "TERM", "ORDINARY", "FED TAX WITHHELD", "WASH AMT DISALLOWED",
                 "ACCRDMKTDISCOUNT", "FORM8949CODE", "GROSSPROCEEDSINDICATOR", "LOSSNOTALLOWED", "NON COVERED",
                 "BASIS NOT SHOWN", "FORM 1099 NOT REC", "COLLECTIBLE", "QOF", "PROFIT", "UNRELPROFITPREV",
                 "UNRELPROFIT", "AGGPROFIT", "STATECODE", "FATCA", "STATEIDNUM", "STATETAXWHELD", "PAYER FED ID",
                 "PAYER NAME1", "PAYER NAME2")


@artifact_processor
def robinhoodCryptoTransfers(context):
    return _csv_artifact(context, _TRANSFER_COLUMNS, ("id", "created_at", "transfer_type"), utc_from="created_at")


@artifact_processor
def robinhoodCryptoOrders(context):
    return _csv_artifact(context, _ORDER_COLUMNS, ("UUID", "Time Entered", "Side"))


@artifact_processor
def robinhoodIPLog(context):
    return _csv_artifact(context, _IPLOG_COLUMNS, ("event_date_time", "client_ip"))


@artifact_processor
def robinhood1099(context):
    return _csv_artifact(context, _1099_COLUMNS, ("1099-B", "ACCOUNT NUMBER"))


@artifact_processor
def robinhoodAccountMaster(context):
    rows, sources = [], set()
    for source, _, res in _parsed_pdfs(context, ("rh_account_master",)):
        for r in res["identity"]:
            rows.append([r["account"], r["section"], r["field"], r["value"], r["locator"], r["raw"],
                         context.get_relative_path(source)])
            sources.add(source)
    headers = ("Account", "Section", "Field", "Value", "Location", "Source Text", "Source File")
    return headers, rows, "\n".join(sorted(sources))


@artifact_processor
def robinhoodAccountMasterEditLog(context):
    rows, sources = [], set()
    for source, _, res in _parsed_pdfs(context, ("rh_account_master",)):
        for r in res["events"]:
            edit = r.get("edit")
            if not edit:
                continue
            rows.append([_aware(r["ts_utc"]), r["ts_original"], r["tz_basis"], r["account"], edit["log"],
                         edit["model"], edit["field"], edit["previous"], edit["new"], edit["author"], "",
                         r["locator"], r["raw"], context.get_relative_path(source)])
            sources.add(source)
        for r in res["other_records"]:
            if r["section"].endswith("(text not attached to a record)"):
                log = r["section"].replace(" (text not attached to a record)", "")
                rows.append(["", "", "", r["account"], log, "", "", "", "", "", r["record"], r["locator"], r["raw"],
                             context.get_relative_path(source)])
                sources.add(source)
    headers = (("Timestamp (UTC)", "datetime"), "Timestamp (as printed)", "Time Basis", "Account", "Log",
               "Model", "Field", "Previous Value", "New Value", "Author", "Unattached Text", "Location",
               "Source Text", "Source File")
    return headers, rows, "\n".join(sorted(sources))


@artifact_processor
def robinhoodStatements(context):
    rows, sources = [], set()
    for source, _, res in _parsed_pdfs(context, ("rh_rhf_statement", "rh_rhc_statement")):
        for r in res["statements"]:
            rows.append([r["statement_type"], r["account"], r["account_basis"], r["period_start"], r["period_end"],
                         r["opening_balance"], r["closing_balance"], r["holdings"],
                         r["rhc_account"], r["name"], r["address"], r["locator"], r["raw"],
                         context.get_relative_path(source)])
            sources.add(source)
    headers = ("Statement", "Account", "Account Basis", "Period Start", "Period End", "Opening Balance",
               "Closing Balance",
               "Holdings", "RHC Account Number", "Name (RHC)", "Address (RHC)",
               "Location", "Source Text", "Source File")
    return headers, rows, "\n".join(sorted(sources))


@artifact_processor
def robinhoodStatementActivity(context):
    rows, sources = [], set()
    for source, _, res in _parsed_pdfs(context, ("rh_rhf_statement", "rh_rhc_statement")):
        for r in res["statement_activity"]:
            rows.append([r["date"], r["statement_type"], r["account"], r["account_basis"], r["period_end"],
                         r["description"], r["type"],
                         r["symbol"], r["quantity"], r["price"], r["debit"], r["credit"], r["value"], r["fee"],
                         r["locator"], r["raw"], context.get_relative_path(source)])
            sources.add(source)
    headers = ("Date", "Statement", "Account", "Account Basis", "Period End", "Description", "Type", "Symbol",
               "Quantity", "Price",
               "Debit", "Credit", "Value", "Fee", "Location", "Source Text", "Source File")
    return headers, rows, "\n".join(sorted(sources))


@artifact_processor
def robinhoodParsingNotes(context):
    rows, sources = [], set()
    for source, kind, res in _parsed_pdfs(context):
        for r in res["warnings"]:
            rows.append([kind.replace("rh_", "").replace("_", " "), r["level"], r["message"], r["locator"], r["raw"],
                         context.get_relative_path(source)])
            sources.add(source)
        if kind == "rh_rhf_statement":
            for r in res["other_records"]:
                rows.append(["rhf statement", "info", r["section"], r["locator"], r["raw"],
                             context.get_relative_path(source)])
                sources.add(source)
    for file_found in sorted(str(f) for f in context.get_files_found()):
        if not file_found.lower().endswith(".csv") or not os.path.isfile(file_found):
            continue
        try:
            _, _, footers = _read_csv(file_found)
        except (OSError, csv.Error):
            continue
        for number, cells in footers:
            rows.append([os.path.basename(file_found), "info", "text line at the end of the file; not a record",
                         f"CSV record {number}", cells[0].strip(), context.get_relative_path(file_found)])
            sources.add(file_found)
    headers = ("Document", "Level", "Message", "Location", "Source Text", "Source File")
    return headers, rows, "\n".join(sorted(sources))

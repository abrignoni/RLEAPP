"""
Coinbase IdvComplianceReport (compliance_report.csv) law enforcement returns.

The report is one CSV holding many sections. A section starts with a one-cell row whose
text ends in '***' (for example 'TRANSACTIONS ***'). Some sections are key/value lists,
others are tables with their own header row, and a few (TOTALS) are small grids. Section
membership varies by production, so every section is reported: the ones named below get
their own artifact, and every other section is reported cell for cell under
'Other Sections', so nothing in the file is dropped.

Values are reported as produced. The only derived columns are the UTC timestamps, and
each one sits next to the timestamp as produced and a column saying how it was derived.
"""

__artifacts_v2__ = {
    'coinbaseCRSubscriber': {
        'name': 'Coinbase Compliance Report - Subscriber Details',
        'description': ('Key/value rows from the USER ATTRIBUTES, IDENTITY and PERSONAL DETAILS '
                        'sections.'),
        'author': '@CyberMike81',
        'creation_date': '2026-09-23',
        'last_update_date': '2026-09-24',
        'requirements': 'none',
        'category': 'Coinbase Compliance Report',
        'notes': ('Cell text is reported with leading and trailing spaces removed and runs of spaces inside a '
                  'line reduced to one; line breaks inside a cell are kept. User ID is the USER ID from the '
                  "report's USER ATTRIBUTES section, repeated on each row so rows from several reports in one "
                  "case stay separable; it is constant when one report is parsed. Source File is the report's "
                  'path within the input. A production can hold the same report more than once, and each copy is '
                  'reported, so compare Source File before counting rows as separate records. Layouts are those '
                  'of synthetic returns and one 2025 production; other production years and layouts may differ. '
                  'After blank lines, repeated headers and uppercase header-like rows with at least two known '
                  'column labels start a new table. Uncertain header-like blocks are retained in Other Sections '
                  'as unmapped table blocks; other blocks continue the preceding table. This heuristic does not '
                  'establish support for every future layout.'),
        'paths': ('*compliance_report*.csv',),
        'output_types': 'standard',
        'artifact_icon': 'user',
    },
    'coinbaseCRIdVerification': {
        'name': 'Coinbase Compliance Report - ID Verification Profiles',
        'description': 'Rows from the JUMIO PROFILES section of the report.',
        'author': '@CyberMike81',
        'creation_date': '2026-09-23',
        'last_update_date': '2026-09-24',
        'requirements': 'none',
        'category': 'Coinbase Compliance Report',
        'notes': ('Cell text is reported with leading and trailing spaces removed and runs of spaces inside a '
                  'line reduced to one; line breaks inside a cell are kept. Timestamp (UTC) is converted only '
                  'when the value states an offset (-0800, Z) or a zone abbreviation; abbreviations are read as '
                  'fixed North American offsets as printed (PST = UTC-8). Values with no zone are left '
                  'unconverted and Time Basis says so. Fractions beyond microseconds are truncated in the UTC '
                  'column; the column as produced keeps every digit. Other Columns (as produced) is empty unless '
                  'the file carries columns this artifact does not name; any such column is kept there as JSON, '
                  "so a new column in a later production is not dropped. User ID is the USER ID from the report's "
                  'USER ATTRIBUTES section, repeated on each row so rows from several reports in one case stay '
                  "separable; it is constant when one report is parsed. Source File is the report's path within "
                  'the input. A production can hold the same report more than once, and each copy is reported, so '
                  'compare Source File before counting rows as separate records. Layouts are those of synthetic '
                  'returns and one 2025 production; other production years and layouts may differ. After blank '
                  'lines, repeated headers and uppercase header-like rows with at least two known column labels '
                  'start a new table. Uncertain header-like blocks are retained in Other Sections as unmapped '
                  'table blocks; other blocks continue the preceding table. This heuristic does not establish '
                  'support for every future layout.'),
        'paths': ('*compliance_report*.csv',),
        'output_types': 'standard',
        'artifact_icon': 'credit-card',
    },
    'coinbaseCRPhoneNumbers': {
        'name': 'Coinbase Compliance Report - Phone Numbers',
        'description': 'Rows from the PHONE NUMBERS section of the report.',
        'author': '@CyberMike81',
        'creation_date': '2026-09-23',
        'last_update_date': '2026-09-24',
        'requirements': 'none',
        'category': 'Coinbase Compliance Report',
        'notes': ('Cell text is reported with leading and trailing spaces removed and runs of spaces inside a '
                  'line reduced to one; line breaks inside a cell are kept. Other Columns (as produced) is empty '
                  'unless the file carries columns this artifact does not name; any such column is kept there as '
                  'JSON, so a new column in a later production is not dropped. User ID is the USER ID from the '
                  "report's USER ATTRIBUTES section, repeated on each row so rows from several reports in one "
                  "case stay separable; it is constant when one report is parsed. Source File is the report's "
                  'path within the input. A production can hold the same report more than once, and each copy is '
                  'reported, so compare Source File before counting rows as separate records. Layouts are those '
                  'of synthetic returns and one 2025 production; other production years and layouts may differ. '
                  'After blank lines, repeated headers and uppercase header-like rows with at least two known '
                  'column labels start a new table. Uncertain header-like blocks are retained in Other Sections '
                  'as unmapped table blocks; other blocks continue the preceding table. This heuristic does not '
                  'establish support for every future layout.'),
        'paths': ('*compliance_report*.csv',),
        'output_types': 'standard',
        'artifact_icon': 'phone',
    },
    'coinbaseCRPreviousEmails': {
        'name': 'Coinbase Compliance Report - Previous Emails',
        'description': 'Rows from the PREVIOUS EMAILS section of the report.',
        'author': '@CyberMike81',
        'creation_date': '2026-09-23',
        'last_update_date': '2026-09-24',
        'requirements': 'none',
        'category': 'Coinbase Compliance Report',
        'notes': ('Cell text is reported with leading and trailing spaces removed and runs of spaces inside a '
                  'line reduced to one; line breaks inside a cell are kept. Other Columns (as produced) is empty '
                  'unless the file carries columns this artifact does not name; any such column is kept there as '
                  'JSON, so a new column in a later production is not dropped. User ID is the USER ID from the '
                  "report's USER ATTRIBUTES section, repeated on each row so rows from several reports in one "
                  "case stay separable; it is constant when one report is parsed. Source File is the report's "
                  'path within the input. A production can hold the same report more than once, and each copy is '
                  'reported, so compare Source File before counting rows as separate records. Layouts are those '
                  'of synthetic returns and one 2025 production; other production years and layouts may differ. '
                  'After blank lines, repeated headers and uppercase header-like rows with at least two known '
                  'column labels start a new table. Uncertain header-like blocks are retained in Other Sections '
                  'as unmapped table blocks; other blocks continue the preceding table. This heuristic does not '
                  'establish support for every future layout.'),
        'paths': ('*compliance_report*.csv',),
        'output_types': 'standard',
        'artifact_icon': 'mail',
    },
    'coinbaseCRBillingAddresses': {
        'name': 'Coinbase Compliance Report - Billing Addresses',
        'description': 'Rows from the BILLING ADDRESSES section of the report.',
        'author': '@CyberMike81',
        'creation_date': '2026-09-23',
        'last_update_date': '2026-09-24',
        'requirements': 'none',
        'category': 'Coinbase Compliance Report',
        'notes': ('Cell text is reported with leading and trailing spaces removed and runs of spaces inside a '
                  'line reduced to one; line breaks inside a cell are kept. Other Columns (as produced) is empty '
                  'unless the file carries columns this artifact does not name; any such column is kept there as '
                  'JSON, so a new column in a later production is not dropped. User ID is the USER ID from the '
                  "report's USER ATTRIBUTES section, repeated on each row so rows from several reports in one "
                  "case stay separable; it is constant when one report is parsed. Source File is the report's "
                  'path within the input. A production can hold the same report more than once, and each copy is '
                  'reported, so compare Source File before counting rows as separate records. Layouts are those '
                  'of synthetic returns and one 2025 production; other production years and layouts may differ. '
                  'After blank lines, repeated headers and uppercase header-like rows with at least two known '
                  'column labels start a new table. Uncertain header-like blocks are retained in Other Sections '
                  'as unmapped table blocks; other blocks continue the preceding table. This heuristic does not '
                  'establish support for every future layout.'),
        'paths': ('*compliance_report*.csv',),
        'output_types': 'standard',
        'artifact_icon': 'map-pin',
    },
    'coinbaseCRBankAccounts': {
        'name': 'Coinbase Compliance Report - Bank Accounts',
        'description': 'Rows from the BANK ACCOUNTS section of the report.',
        'author': '@CyberMike81',
        'creation_date': '2026-09-23',
        'last_update_date': '2026-09-24',
        'requirements': 'none',
        'category': 'Coinbase Compliance Report',
        'notes': ('Cell text is reported with leading and trailing spaces removed and runs of spaces inside a '
                  'line reduced to one; line breaks inside a cell are kept. Other Columns (as produced) is empty '
                  'unless the file carries columns this artifact does not name; any such column is kept there as '
                  'JSON, so a new column in a later production is not dropped. User ID is the USER ID from the '
                  "report's USER ATTRIBUTES section, repeated on each row so rows from several reports in one "
                  "case stay separable; it is constant when one report is parsed. Source File is the report's "
                  'path within the input. A production can hold the same report more than once, and each copy is '
                  'reported, so compare Source File before counting rows as separate records. Layouts are those '
                  'of synthetic returns and one 2025 production; other production years and layouts may differ. '
                  'After blank lines, repeated headers and uppercase header-like rows with at least two known '
                  'column labels start a new table. Uncertain header-like blocks are retained in Other Sections '
                  'as unmapped table blocks; other blocks continue the preceding table. This heuristic does not '
                  'establish support for every future layout.'),
        'paths': ('*compliance_report*.csv',),
        'output_types': 'standard',
        'artifact_icon': 'dollar-sign',
    },
    'coinbaseCRPaymentMethods': {
        'name': 'Coinbase Compliance Report - Other Payment Methods',
        'description': ('Rows from the card, PayPal, SEPA, Fedwire, SWIFT, UK, bank wire and '
                        'intrabank payment method sections.'),
        'author': '@CyberMike81',
        'creation_date': '2026-09-23',
        'last_update_date': '2026-09-24',
        'requirements': 'none',
        'category': 'Coinbase Compliance Report',
        'notes': ('Cell text is reported with leading and trailing spaces removed and runs of spaces inside a '
                  'line reduced to one; line breaks inside a cell are kept. Each of these sections has its own '
                  'columns, so each row is reported as COLUMN: value pairs in the order produced. The PAYMENT '
                  'CARD (LEGACY) section holds two tables; the header row of each is reported with its rows. User '
                  "ID is the USER ID from the report's USER ATTRIBUTES section, repeated on each row so rows from "
                  'several reports in one case stay separable; it is constant when one report is parsed. Source '
                  "File is the report's path within the input. A production can hold the same report more than "
                  'once, and each copy is reported, so compare Source File before counting rows as separate '
                  'records. Layouts are those of synthetic returns and one 2025 production; other production '
                  'years and layouts may differ. After blank lines, repeated headers and uppercase header-like '
                  'rows with at least two known column labels start a new table. Uncertain header-like blocks are '
                  'retained in Other Sections as unmapped table blocks; other blocks continue the preceding '
                  'table. This heuristic does not establish support for every future layout.'),
        'paths': ('*compliance_report*.csv',),
        'output_types': 'standard',
        'artifact_icon': 'credit-card',
    },
    'coinbaseCRCryptoAddresses': {
        'name': 'Coinbase Compliance Report - Crypto Addresses',
        'description': ('Rows from the section whose title lists asset symbols and ends in '
                        'ADDRESSES.'),
        'author': '@CyberMike81',
        'creation_date': '2026-09-23',
        'last_update_date': '2026-09-24',
        'requirements': 'none',
        'category': 'Coinbase Compliance Report',
        'notes': ('Cell text is reported with leading and trailing spaces removed and runs of spaces inside a '
                  'line reduced to one; line breaks inside a cell are kept. The section title is a long list of '
                  'asset symbols that changes between productions, so the section is found by its ending and its '
                  'columns (ADDRESS and NETWORK). Timestamp (UTC) is converted only when the value states an '
                  'offset (-0800, Z) or a zone abbreviation; abbreviations are read as fixed North American '
                  'offsets as printed (PST = UTC-8). Values with no zone are left unconverted and Time Basis says '
                  'so. Fractions beyond microseconds are truncated in the UTC column; the column as produced '
                  'keeps every digit. Other Columns (as produced) is empty unless the file carries columns this '
                  'artifact does not name; any such column is kept there as JSON, so a new column in a later '
                  "production is not dropped. User ID is the USER ID from the report's USER ATTRIBUTES section, "
                  'repeated on each row so rows from several reports in one case stay separable; it is constant '
                  "when one report is parsed. Source File is the report's path within the input. A production can "
                  'hold the same report more than once, and each copy is reported, so compare Source File before '
                  'counting rows as separate records. Layouts are those of synthetic returns and one 2025 '
                  'production; other production years and layouts may differ. After blank lines, repeated headers '
                  'and uppercase header-like rows with at least two known column labels start a new table. '
                  'Uncertain header-like blocks are retained in Other Sections as unmapped table blocks; other '
                  'blocks continue the preceding table. This heuristic does not establish support for every '
                  'future layout.'),
        'paths': ('*compliance_report*.csv',),
        'output_types': 'standard',
        'artifact_icon': 'key',
    },
    'coinbaseCRTotals': {
        'name': 'Coinbase Compliance Report - Totals',
        'description': 'Grid rows from the TOTALS and EXCHANGE TOTALS sections.',
        'author': '@CyberMike81',
        'creation_date': '2026-09-23',
        'last_update_date': '2026-09-24',
        'requirements': 'none',
        'category': 'Coinbase Compliance Report',
        'notes': ('Cell text is reported with leading and trailing spaces removed and runs of spaces inside a '
                  'line reduced to one; line breaks inside a cell are kept. These sections are grids: a row with '
                  'an empty first cell names the asset and the value columns, and the rows under it give a metric '
                  'and its values. Asset and Value Columns come from that naming row. Amounts are as produced. '
                  "User ID is the USER ID from the report's USER ATTRIBUTES section, repeated on each row so rows "
                  'from several reports in one case stay separable; it is constant when one report is parsed. '
                  "Source File is the report's path within the input. A production can hold the same report more "
                  'than once, and each copy is reported, so compare Source File before counting rows as separate '
                  'records. Layouts are those of synthetic returns and one 2025 production; other production '
                  'years and layouts may differ. After blank lines, repeated headers and uppercase header-like '
                  'rows with at least two known column labels start a new table. Uncertain header-like blocks are '
                  'retained in Other Sections as unmapped table blocks; other blocks continue the preceding '
                  'table. This heuristic does not establish support for every future layout.'),
        'paths': ('*compliance_report*.csv',),
        'output_types': 'standard',
        'artifact_icon': 'bar-chart-2',
    },
    'coinbaseCRTransactions': {
        'name': 'Coinbase Compliance Report - Transactions',
        'description': 'Rows from the TRANSACTIONS section of the report.',
        'author': '@CyberMike81',
        'creation_date': '2026-09-23',
        'last_update_date': '2026-09-24',
        'requirements': 'none',
        'category': 'Coinbase Compliance Report',
        'notes': ('Cell text is reported with leading and trailing spaces removed and runs of spaces inside a '
                  'line reduced to one; line breaks inside a cell are kept. Amounts, balances and USD values are '
                  'as produced. Timestamp (UTC) is converted only when the value states an offset (-0800, Z) or a '
                  'zone abbreviation; abbreviations are read as fixed North American offsets as printed (PST = '
                  'UTC-8). Values with no zone are left unconverted and Time Basis says so. Fractions beyond '
                  'microseconds are truncated in the UTC column; the column as produced keeps every digit. Other '
                  'Columns (as produced) is empty unless the file carries columns this artifact does not name; '
                  'any such column is kept there as JSON, so a new column in a later production is not dropped. '
                  "User ID is the USER ID from the report's USER ATTRIBUTES section, repeated on each row so rows "
                  'from several reports in one case stay separable; it is constant when one report is parsed. '
                  "Source File is the report's path within the input. A production can hold the same report more "
                  'than once, and each copy is reported, so compare Source File before counting rows as separate '
                  'records. Layouts are those of synthetic returns and one 2025 production; other production '
                  'years and layouts may differ. After blank lines, repeated headers and uppercase header-like '
                  'rows with at least two known column labels start a new table. Uncertain header-like blocks are '
                  'retained in Other Sections as unmapped table blocks; other blocks continue the preceding '
                  'table. This heuristic does not establish support for every future layout.'),
        'paths': ('*compliance_report*.csv',),
        'output_types': 'standard',
        'artifact_icon': 'dollar-sign',
    },
    'coinbaseCRExchangeActivity': {
        'name': 'Coinbase Compliance Report - Exchange Activity',
        'description': 'Rows from the EXCHANGE TRANSFERS and EXCHANGE TRANSACTIONS sections.',
        'author': '@CyberMike81',
        'creation_date': '2026-09-23',
        'last_update_date': '2026-09-24',
        'requirements': 'none',
        'category': 'Coinbase Compliance Report',
        'notes': ('Cell text is reported with leading and trailing spaces removed and runs of spaces inside a '
                  'line reduced to one; line breaks inside a cell are kept. Each row is reported as COLUMN: value '
                  'pairs in the order produced, because the two sections have different columns. Timestamp (UTC) '
                  'is converted only when the value states an offset (-0800, Z) or a zone abbreviation; '
                  'abbreviations are read as fixed North American offsets as printed (PST = UTC-8). Values with '
                  'no zone are left unconverted and Time Basis says so. Fractions beyond microseconds are '
                  'truncated in the UTC column; the column as produced keeps every digit. User ID is the USER ID '
                  "from the report's USER ATTRIBUTES section, repeated on each row so rows from several reports "
                  'in one case stay separable; it is constant when one report is parsed. Source File is the '
                  "report's path within the input. A production can hold the same report more than once, and each "
                  'copy is reported, so compare Source File before counting rows as separate records. Layouts are '
                  'those of synthetic returns and one 2025 production; other production years and layouts may '
                  'differ. After blank lines, repeated headers and uppercase header-like rows with at least two '
                  'known column labels start a new table. Uncertain header-like blocks are retained in Other '
                  'Sections as unmapped table blocks; other blocks continue the preceding table. This heuristic '
                  'does not establish support for every future layout.'),
        'paths': ('*compliance_report*.csv',),
        'output_types': 'standard',
        'artifact_icon': 'repeat',
    },
    'coinbaseCREvents': {
        'name': 'Coinbase Compliance Report - Account Events',
        'description': 'Rows from the EVENTS section of the report.',
        'author': '@CyberMike81',
        'creation_date': '2026-09-23',
        'last_update_date': '2026-09-24',
        'requirements': 'none',
        'category': 'Coinbase Compliance Report',
        'notes': ('Cell text is reported with leading and trailing spaces removed and runs of spaces inside a '
                  'line reduced to one; line breaks inside a cell are kept. IP, FINGERPRINT and LOCATION are '
                  'reported as produced. Timestamp (UTC) is converted only when the value states an offset '
                  '(-0800, Z) or a zone abbreviation; abbreviations are read as fixed North American offsets as '
                  'printed (PST = UTC-8). Values with no zone are left unconverted and Time Basis says so. '
                  'Fractions beyond microseconds are truncated in the UTC column; the column as produced keeps '
                  'every digit. Other Columns (as produced) is empty unless the file carries columns this '
                  'artifact does not name; any such column is kept there as JSON, so a new column in a later '
                  "production is not dropped. User ID is the USER ID from the report's USER ATTRIBUTES section, "
                  'repeated on each row so rows from several reports in one case stay separable; it is constant '
                  "when one report is parsed. Source File is the report's path within the input. A production can "
                  'hold the same report more than once, and each copy is reported, so compare Source File before '
                  'counting rows as separate records. Layouts are those of synthetic returns and one 2025 '
                  'production; other production years and layouts may differ. After blank lines, repeated headers '
                  'and uppercase header-like rows with at least two known column labels start a new table. '
                  'Uncertain header-like blocks are retained in Other Sections as unmapped table blocks; other '
                  'blocks continue the preceding table. This heuristic does not establish support for every '
                  'future layout.'),
        'paths': ('*compliance_report*.csv',),
        'output_types': 'standard',
        'artifact_icon': 'activity',
    },
    'coinbaseCRManualReviews': {
        'name': 'Coinbase Compliance Report - Manual Reviews',
        'description': 'Rows from the MANUAL REVIEWS section of the report.',
        'author': '@CyberMike81',
        'creation_date': '2026-09-23',
        'last_update_date': '2026-09-24',
        'requirements': 'none',
        'category': 'Coinbase Compliance Report',
        'notes': ('Cell text is reported with leading and trailing spaces removed and runs of spaces inside a '
                  'line reduced to one; line breaks inside a cell are kept. Timestamp (UTC) is derived from '
                  'CREATED. Timestamp (UTC) is converted only when the value states an offset (-0800, Z) or a '
                  'zone abbreviation; abbreviations are read as fixed North American offsets as printed (PST = '
                  'UTC-8). Values with no zone are left unconverted and Time Basis says so. Fractions beyond '
                  'microseconds are truncated in the UTC column; the column as produced keeps every digit. Other '
                  'Columns (as produced) is empty unless the file carries columns this artifact does not name; '
                  'any such column is kept there as JSON, so a new column in a later production is not dropped. '
                  "User ID is the USER ID from the report's USER ATTRIBUTES section, repeated on each row so rows "
                  'from several reports in one case stay separable; it is constant when one report is parsed. '
                  "Source File is the report's path within the input. A production can hold the same report more "
                  'than once, and each copy is reported, so compare Source File before counting rows as separate '
                  'records. Layouts are those of synthetic returns and one 2025 production; other production '
                  'years and layouts may differ. After blank lines, repeated headers and uppercase header-like '
                  'rows with at least two known column labels start a new table. Uncertain header-like blocks are '
                  'retained in Other Sections as unmapped table blocks; other blocks continue the preceding '
                  'table. This heuristic does not establish support for every future layout.'),
        'paths': ('*compliance_report*.csv',),
        'output_types': 'standard',
        'artifact_icon': 'clipboard',
    },
    'coinbaseCROtherSections': {
        'name': 'Coinbase Compliance Report - Other Sections',
        'description': 'Rows of report sections that no other artifact in this module reports.',
        'author': '@CyberMike81',
        'creation_date': '2026-09-23',
        'last_update_date': '2026-09-24',
        'requirements': 'none',
        'category': 'Coinbase Compliance Report',
        'notes': ('Cell text is reported with leading and trailing spaces removed and runs of spaces inside a '
                  'line reduced to one; line breaks inside a cell are kept. Rows are reported cell for cell, '
                  "joined with ' | ', with the section title and the CSV record number. The first row of each "
                  "block is usually that section's header row. Sections present with no rows are listed with an "
                  "empty Cells value. User ID is the USER ID from the report's USER ATTRIBUTES section, repeated "
                  'on each row so rows from several reports in one case stay separable; it is constant when one '
                  "report is parsed. Source File is the report's path within the input. A production can hold the "
                  'same report more than once, and each copy is reported, so compare Source File before counting '
                  'rows as separate records. Layouts are those of synthetic returns and one 2025 production; '
                  'other production years and layouts may differ. After blank lines, repeated headers and '
                  'uppercase header-like rows with at least two known column labels start a new table. Uncertain '
                  'header-like blocks are retained in Other Sections as unmapped table blocks; other blocks '
                  'continue the preceding table. This heuristic does not establish support for every future '
                  'layout.'),
        'paths': ('*compliance_report*.csv',),
        'output_types': 'standard',
        'artifact_icon': 'file-text',
    },
}

import csv
import io
import json
import os
import re
from datetime import datetime, timedelta, timezone

from scripts.ilapfuncs import artifact_processor, logfunc

_KV_SECTIONS = ("USER ATTRIBUTES", "IDENTITY", "PERSONAL DETAILS")
_SUBTABLE_FIRST_CELLS = {"PAN"}     # second table inside PAYMENT CARD (LEGACY)
_PAYMENT_SECTIONS = ("PAYMENT CARDS", "PAYMENT CARD (LEGACY) PAYMENT METHOD", "PAYPAL ACCOUNTS",
                     "SEPA PAYMENT METHOD", "FEDWIRE PAYMENT METHOD", "SWIFT PAYMENT METHOD",
                     "UK PAYMENT METHOD", "BANKWIRE PAYMENT METHOD", "INTRABANK PAYMENT METHOD")
_EXCHANGE_SECTIONS = ("EXCHANGE TRANSFERS", "EXCHANGE TRANSACTIONS")
_TOTALS_SECTIONS = ("TOTALS", "EXCHANGE TOTALS")

_COLUMNS = {
    "JUMIO PROFILES": ("DATE", "TYPE", "ID NUMBER", "STATUS", "NAME", "DOB", "ADDRESS", "UNIT NUMBER",
                       "CITY", "STATE", "ZIP", "COUNTRY"),
    "PHONE NUMBERS": ("NUMBER", "COUNTRY", "VERIFIED"),
    "PREVIOUS EMAILS": ("CHANGED FROM", "CHANGED TO", "CHANGED AT", "CONFIRMED AT"),
    "BILLING ADDRESSES": ("ADDRESS 1", "ADDRESS 2", "ADDRESS 3", "CITY", "STATE", "POSTAL CODE",
                          "COUNTRY"),
    "BANK ACCOUNTS": ("CUSTOMER NAME", "BANK NAME", "ACCOUNT NUMBER", "ROUTING NUMBER",
                      "ACCOUNT TYPE", "VERIFIED", "VERIFICATION METHOD"),
    "ADDRESSES": ("CREATED", "ACCOUNT", "NETWORK", "ADDRESS", "LABEL", "CALLBACK URL"),
    "TRANSACTIONS": ("TIMESTAMP", "ACCOUNT NAME", "TYPE", "STATUS", "BALANCE", "AMOUNT", "CURRENCY",
                     "TO", "PRO TRANSFER", "NOTES", "EQUIV USD", "TRANSACTION HASH",
                     "PAYMENT METHOD DETAILS", "TRANSACTION ID", "NETWORK"),
    "EVENTS": ("TIMESTAMP", "ACTION", "IP", "FINGERPRINT", "USER AGENT", "LOCATION", "SOURCE",
               "DETAILS"),
    "MANUAL REVIEWS": ("CREATED", "UPDATED", "STATUS", "REASON", "REASON VALUE"),
}


# ------------------------------------------------------------------ timestamps
_MONTHS = {m: i + 1 for i, m in enumerate(("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug",
                                           "sep", "oct", "nov", "dec"))}
_TZ_ABBR = {"PST": -8, "PDT": -7, "MST": -7, "MDT": -6, "CST": -6, "CDT": -5, "EST": -5, "EDT": -4,
            "AKST": -9, "AKDT": -8, "HST": -10, "UTC": 0, "GMT": 0, "Z": 0}
_ISO = re.compile(r"^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2})(?::(\d{2})(?:\.(\d+))?)?\s*"
                  r"(Z|[+-]\d{2}:?\d{2})?$")
_MONTH_FIRST = re.compile(r"^([A-Za-z]+),?\s+(\d{1,2}),?\s+(\d{4}),?\s+(\d{1,2}):(\d{2})(?::(\d{2}))?"
                          r"\s*([aApP][mM])?\s*([A-Z]{1,4})?$")


def _hour12(hour, ampm):
    hour = int(hour)
    if ampm:
        if not 1 <= hour <= 12:
            raise ValueError("bad 12-hour value")
        hour = (hour % 12) + (12 if ampm.lower() == "pm" else 0)
    return hour


def _to_utc(value):
    """(aware UTC datetime or '', time basis). Only a stated offset or zone is converted."""
    text = " ".join(str(value or "").split())
    if not text:
        return "", ""
    try:
        m = _ISO.match(text)
        if m:
            parts = [int(x) for x in m.group(1, 2, 3, 4, 5)]
            base = datetime(*parts, int(m.group(6) or 0), int((m.group(7) or "0")[:6].ljust(6, "0")))
            zone = m.group(8)
            if not zone:
                return "", "zone not stated"
            if zone == "Z":
                return base.replace(tzinfo=timezone.utc), "stated offset"
            zz = zone.replace(":", "")
            minutes = (1 if zz[0] == "+" else -1) * (int(zz[1:3]) * 60 + int(zz[3:5]))
            return (base - timedelta(minutes=minutes)).replace(tzinfo=timezone.utc), "stated offset"
        m = _MONTH_FIRST.match(text)
        if m and m.group(1)[:3].lower() in _MONTHS:
            base = datetime(int(m.group(3)), _MONTHS[m.group(1)[:3].lower()], int(m.group(2)),
                            _hour12(m.group(4), m.group(7)), int(m.group(5)), int(m.group(6) or 0))
            zone = m.group(8)
            if not zone:
                return "", "zone not stated"
            if zone not in _TZ_ABBR:
                return "", f"zone '{zone}' not recognized"
            return ((base - timedelta(hours=_TZ_ABBR[zone])).replace(tzinfo=timezone.utc),
                    "stated zone abbreviation (fixed offset)")
    except ValueError:
        return "", "unparsed"
    return "", "unparsed"


# ------------------------------------------------------------------ report reading
def _decode(data):
    for enc in ("utf-8-sig", "cp1252"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("latin-1")


def _clean(value):
    text = str(value or "").replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(" ".join(part.split()) for part in text.split("\n")).strip()


def _read_report(path):
    """Returns None when the file is not an IdvComplianceReport, else
    {'user_id', 'order': [titles], 'sections': {title: [block]}, 'pre': [block]};
    block = [(csv_record_number, cells)]."""
    with open(path, "rb") as handle:
        text = _decode(handle.read())
    parsed_rows = list(csv.reader(io.StringIO(text, newline="")))
    first = next((cells for cells in parsed_rows if any(c.strip() for c in cells)), [])
    if not first or first[0].strip().upper() != "USER ATTRIBUTES ***":
        return None
    sections, order, pre = {}, [], []
    title, block = None, []

    def flush():
        if block:
            (sections[title] if title is not None else pre).append(list(block))
        block.clear()

    for number, cells in enumerate(parsed_rows, start=1):
        nonempty = [c for c in cells if c.strip()]
        if len(nonempty) == 1 and cells and cells[0].strip().endswith("***"):
            flush()
            title = cells[0].strip()[:-3].strip()
            if title not in sections:
                sections[title] = []
                order.append(title)
            continue
        if not nonempty:
            flush()
            continue
        block.append((number, cells))
    flush()
    user_id = ""
    for blk in sections.get("USER ATTRIBUTES", []):
        for _, cells in blk:
            if cells and cells[0].strip() == "USER ID" and len(cells) > 1:
                user_id = cells[1].strip()
    return {"user_id": user_id, "order": order, "sections": sections, "pre": pre}


def _reports(context):
    """(source path, parsed report) for every matched file that is a compliance report."""
    out = []
    for file_found in sorted(str(f) for f in context.get_files_found()):
        try:
            report = _read_report(file_found)
        except (OSError, csv.Error) as err:
            logfunc(f"Coinbase compliance report: skipped {os.path.basename(file_found)}: {type(err).__name__}")
            continue
        if report is not None:
            out.append((file_found, report))
        else:
            logfunc(f"Coinbase compliance report: skipped {os.path.basename(file_found)}: "
                    "first nonempty CSV row does not start with USER ATTRIBUTES ***")
    return out


def _tables(blocks, unmapped=None):
    """Read repeated/recognisable headers; retain uncertain header-like blocks unmapped.

    A header-like row contains at least two distinct uppercase column-label strings.
    At least two labels must be known to use a changed header. Otherwise its block and
    following continuation blocks stay unmapped until a recognisable header resumes.
    """
    tables, uncertain = [], False
    vocabulary = {c for columns in _COLUMNS.values() for c in columns}
    for blk in blocks:
        first = [c.strip() for c in blk[0][1]]
        labels = [c for c in first if c]
        looks_header = (len(labels) >= 2 and len(set(labels)) == len(labels) and
                        all(re.fullmatch(r"[A-Z][A-Z0-9 _/()#.$-]*", c) for c in labels))
        known_header = looks_header and len(set(labels) & vocabulary) >= 2
        if not tables or first[0] in _SUBTABLE_FIRST_CELLS or first == tables[-1][0] or known_header:
            tables.append((first, list(blk[1:])))
            uncertain = False
        elif looks_header or uncertain:
            uncertain = True
            if unmapped is not None:
                unmapped.extend(blk)
        else:
            tables[-1][1].extend(blk)
    return tables


def _record(header, cells):
    return {header[i]: _clean(cells[i]) if i < len(cells) else "" for i in range(len(header)) if header[i]}


def _extra(header, cells, known):
    extra = {}
    for i, cell in enumerate(cells):
        name = header[i] if i < len(header) and header[i] else f"(column {i + 1})"
        if name not in known and cell.strip():
            extra[name] = _clean(cell)
    return json.dumps(extra, ensure_ascii=False) if extra else ""


def _pairs(header, cells):
    return "; ".join(f"{header[i] if i < len(header) and header[i] else f'(column {i + 1})'}: {_clean(c)}"
                     for i, c in enumerate(cells) if c.strip())


def _crypto_address_titles(report):
    titles = []
    for title in report["order"]:
        if title.endswith("ADDRESSES") and title != "BILLING ADDRESSES":
            tables = _tables(report["sections"].get(title, []))
            if tables and all("ADDRESS" in h and "NETWORK" in h for h, _ in tables):
                titles.append(title)
    return titles


def _table_artifact(context, section, time_column=None):
    """Rows of one table section: User ID, [UTC, as produced, basis], named columns, other
    columns, CSV record."""
    known = _COLUMNS[section]
    headers = ["User ID"]
    if time_column:
        headers += [("Timestamp (UTC)", "datetime"), f"{time_column} (as produced)", "Time Basis"]
    headers += [c for c in known if c != time_column]      # column names as produced
    headers += ["Other Columns (as produced)", "CSV Record", "Source File"]
    rows, sources = [], set()
    for source, report in _reports(context):
        titles = _crypto_address_titles(report) if section == "ADDRESSES" else [section]
        for title in titles:
            for header, records in _tables(report["sections"].get(title, [])):
                for number, cells in records:
                    rec = _record(header, cells)
                    line = [report["user_id"]]
                    if time_column:
                        utc, basis = _to_utc(rec.get(time_column, ""))
                        line += [utc, rec.get(time_column, ""), basis]
                    line += [rec.get(c, "") for c in known if c != time_column]
                    line += [_extra(header, cells, known), number, context.get_relative_path(source)]
                    rows.append(line)
                    sources.add(source)
    return tuple(headers), rows, "\n".join(sorted(sources))


# ------------------------------------------------------------------ artifacts
@artifact_processor
def coinbaseCRSubscriber(context):
    rows, sources = [], set()
    for source, report in _reports(context):
        for section in _KV_SECTIONS:
            for blk in report["sections"].get(section, []):
                for number, cells in blk:
                    extra = [_clean(c) for c in cells[2:] if c.strip()]
                    rows.append([report["user_id"], section.title(), _clean(cells[0]) if cells else "",
                                 _clean(cells[1]) if len(cells) > 1 else "", " | ".join(extra), number,
                                 context.get_relative_path(source)])
                    sources.add(source)
    headers = ("User ID", "Section", "Field", "Value", "Further Cells (as produced)", "CSV Record", "Source File")
    return headers, rows, "\n".join(sorted(sources))


@artifact_processor
def coinbaseCRIdVerification(context):
    return _table_artifact(context, "JUMIO PROFILES", "DATE")


@artifact_processor
def coinbaseCRPhoneNumbers(context):
    return _table_artifact(context, "PHONE NUMBERS")


@artifact_processor
def coinbaseCRPreviousEmails(context):
    return _table_artifact(context, "PREVIOUS EMAILS", "CHANGED AT")


@artifact_processor
def coinbaseCRBillingAddresses(context):
    return _table_artifact(context, "BILLING ADDRESSES")


@artifact_processor
def coinbaseCRBankAccounts(context):
    return _table_artifact(context, "BANK ACCOUNTS")


@artifact_processor
def coinbaseCRCryptoAddresses(context):
    return _table_artifact(context, "ADDRESSES", "CREATED")


@artifact_processor
def coinbaseCRTransactions(context):
    return _table_artifact(context, "TRANSACTIONS", "TIMESTAMP")


@artifact_processor
def coinbaseCREvents(context):
    return _table_artifact(context, "EVENTS", "TIMESTAMP")


@artifact_processor
def coinbaseCRManualReviews(context):
    return _table_artifact(context, "MANUAL REVIEWS", "CREATED")


@artifact_processor
def coinbaseCRPaymentMethods(context):
    rows, sources = [], set()
    for source, report in _reports(context):
        for section in _PAYMENT_SECTIONS:
            for header, records in _tables(report["sections"].get(section, [])):
                for number, cells in records:
                    rows.append([report["user_id"], section.title(), " | ".join(header), _pairs(header, cells),
                                 number, context.get_relative_path(source)])
                    sources.add(source)
    headers = ("User ID", "Section", "Header Row (as produced)", "Record", "CSV Record", "Source File")
    return headers, rows, "\n".join(sorted(sources))


@artifact_processor
def coinbaseCRExchangeActivity(context):
    rows, sources = [], set()
    for source, report in _reports(context):
        for section in _EXCHANGE_SECTIONS:
            for header, records in _tables(report["sections"].get(section, [])):
                for number, cells in records:
                    raw = _record(header, cells).get("TIMESTAMP", "")
                    utc, basis = _to_utc(raw)
                    rows.append([report["user_id"], utc, raw, basis, section.title(), _pairs(header, cells),
                                 number, context.get_relative_path(source)])
                    sources.add(source)
    headers = ("User ID", ("Timestamp (UTC)", "datetime"), "TIMESTAMP (as produced)", "Time Basis",
               "Section", "Record", "CSV Record", "Source File")
    return headers, rows, "\n".join(sorted(sources))


@artifact_processor
def coinbaseCRTotals(context):
    rows, sources = [], set()
    for source, report in _reports(context):
        for section in _TOTALS_SECTIONS:
            for blk in report["sections"].get(section, []):
                asset, value_names = "", []
                for number, cells in blk:
                    clean = [_clean(c) for c in cells]
                    if clean and not clean[0] and len(clean) > 1 and clean[1]:
                        asset, value_names = clean[1], clean[1:]
                        continue
                    if clean and clean[0]:
                        values = clean[1:]
                        rows.append([report["user_id"], section.title(), asset, clean[0],
                                     values[0] if values else "", values[1] if len(values) > 1 else "",
                                     " | ".join(values[2:]), " | ".join(value_names), number,
                                     context.get_relative_path(source)])
                        sources.add(source)
    headers = ("User ID", "Section", "Asset", "Metric", "First Value", "Second Value",
               "Further Values", "Value Columns (as produced)", "CSV Record", "Source File")
    return headers, rows, "\n".join(sorted(sources))


@artifact_processor
def coinbaseCROtherSections(context):
    reported = set(_KV_SECTIONS) | set(_PAYMENT_SECTIONS) | set(_EXCHANGE_SECTIONS) | set(_TOTALS_SECTIONS)
    reported |= {"JUMIO PROFILES", "PHONE NUMBERS", "PREVIOUS EMAILS", "BILLING ADDRESSES",
                 "BANK ACCOUNTS", "TRANSACTIONS", "EVENTS", "MANUAL REVIEWS"}
    rows, sources = [], set()
    for source, report in _reports(context):
        skip = reported | set(_crypto_address_titles(report))
        for blk in report["pre"]:
            for number, cells in blk:
                rows.append([report["user_id"], "(before first section)", " | ".join(_clean(c) for c in cells),
                             number, context.get_relative_path(source)])
                sources.add(source)
        for title in report["order"]:
            if title in skip:
                if title not in set(_KV_SECTIONS) | set(_TOTALS_SECTIONS):
                    unmapped = []
                    _tables(report["sections"].get(title, []), unmapped)
                    for number, cells in unmapped:
                        rows.append([report["user_id"], title.title() + " (unmapped table block)",
                                     " | ".join(_clean(c) for c in cells), number,
                                     context.get_relative_path(source)])
                        sources.add(source)
                continue
            blocks = report["sections"].get(title, [])
            if not blocks:
                rows.append([report["user_id"], title.title(), "", "", context.get_relative_path(source)])
                sources.add(source)
            for blk in blocks:
                for number, cells in blk:
                    rows.append([report["user_id"], title.title(), " | ".join(_clean(c) for c in cells), number,
                                 context.get_relative_path(source)])
                    sources.add(source)
    headers = ("User ID", "Section", "Cells (as produced)", "CSV Record", "Source File")
    return headers, rows, "\n".join(sorted(sources))

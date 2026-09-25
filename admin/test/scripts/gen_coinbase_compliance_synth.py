"""
Generate a synthetic Coinbase IdvComplianceReport return for the coinbaseComplianceReport tests.

Every value here is fabricated. A compliance report is a provider legal return: subscriber
PII, government ID numbers and bank details end to end, so no real return can be sanitised
into a fixture. The shape follows real reports, including the parts a parser can get wrong:

  - two reports for two users, plus a byte-identical second copy of the first report in a
    nested folder, which real productions contain; each copy must be reported separately
  - key/value sections (USER ATTRIBUTES, IDENTITY, PERSONAL DETAILS), one row with a stray
    third cell
  - timestamps with a numeric offset, a trailing Z with milliseconds, a North American zone
    abbreviation ("January, 5 2021 04:28pm PST"), and one with no zone at all, which must be
    left unconverted
  - a quoted cell with an embedded line break (BANK NAME)
  - a table split into two blocks by a blank row, which is one table, and PAYMENT CARD
    (LEGACY), whose second block starts a second table with its own header (PAN ...)
  - a crypto-address section whose title is a list of asset symbols
  - TOTALS grids with two asset blocks, and an EXCHANGE TOTALS grid
  - an extra column the module does not name (TRANSACTIONS "SURPLUS COL"), which must land
    in Other Columns rather than be dropped
  - an unmapped section with rows, one with only a header row, and one that is empty
  - an all-quoted report, a reordered second transaction header, an unknown table block,
    and abbreviated timestamps in the converted transaction and event columns
  - a decoy file matching the path pattern that is not a compliance report

Usage:
    python admin/test/scripts/gen_coinbase_compliance_synth.py [output_dir]

Then zip the output folder and feed it to make_test_data.py.
"""
import csv
import io
import os
import shutil
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "synth_coinbase_return")


def csv_text(rows):
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\r\n")
    for row in rows:
        writer.writerow(row)
    return buf.getvalue()


def report(user_id, name, email, extra_rows=True):
    rows = [
        ["USER ATTRIBUTES ***"], ["USER ID", user_id], ["NAME", name], ["EMAIL", email],
        ["CREATED", "January, 5 2021 04:28pm PST"], ["NOTE", "synthetic", "stray third cell"], [], [],
        ["IDENTITY ***"], ["FIRST NAME", name.split()[0]], ["LAST NAME", name.split()[-1]],
        ["SSN", "900-00-0001"], ["ADDRESS1", "100 Synthetic Way"], ["CITY", "Testville"],
        ["STATE", "KY"], ["ZIP", "40000"], ["BIRTHDATE M/D/Y", "01/02/1990"], [], [],
        ["PERSONAL DETAILS ***"], ["OCCUPATION", "Tester"], [], [],
        ["JUMIO PROFILES ***"],
        ["DATE", "TYPE", "ID NUMBER", "STATUS", "NAME", "DOB", "ADDRESS", "UNIT NUMBER", "CITY",
         "STATE", "ZIP", "COUNTRY"],
        ["2021-01-05T12:00:00.123Z", "Driver's License", "S0000001", "completed", name,
         "1990-01-02", "100 SYNTHETIC WAY", "", "TESTVILLE", "KY", "40000", "US"],
        [], [],
        ["PREVIOUS EMAILS ***"], ["CHANGED FROM", "CHANGED TO", "CHANGED AT", "CONFIRMED AT"],
        ["old@example.test", email, "2021-02-01 10:00:00 -0800", "2021-02-01 10:05:00 -0800"], [], [],
        ["PHONE NUMBERS ***"], ["NUMBER", "COUNTRY", "VERIFIED"], ["5550100001", "US", "true"], [], [],
        ["BILLING ADDRESSES ***"],
        ["ADDRESS 1", "ADDRESS 2", "ADDRESS 3", "CITY", "STATE", "POSTAL CODE", "COUNTRY"],
        ["100 Synthetic Way", "", "", "Testville", "KY", "40000", "US"], [], [],
        ["BANK ACCOUNTS ***"],
        ["CUSTOMER NAME", "BANK NAME", "ACCOUNT NUMBER", "ROUTING NUMBER", "ACCOUNT TYPE", "VERIFIED",
         "VERIFICATION METHOD"],
        [name.upper(), "Example Bank\r\n   Branch 2", "000000000001", "000000001", "checking", "true",
         "micro_deposits"], [], [],
        ["PAYMENT CARD (LEGACY) PAYMENT METHOD ***"], ["CARD PART", "TYPE", "EXP", "NAME", "VERIFIED"],
        ["400000", "visa", "01/2030", name, "true"], [],
        ["PAN", "TYPE", "EXP", "NAME", "STATUS"], ["4000********0001", "Card visa debit", "11/2030", name,
                                                   "cdv_required"], [], [],
        ["PAYPAL ACCOUNTS ***"], ["EMAIL", "VERIFIED"], [email, "false"], [], [],
        ["BTC/ETH/USDC ADDRESSES ***"], ["CREATED", "ACCOUNT", "NETWORK", "ADDRESS", "LABEL", "CALLBACK URL"],
        ["2021-02-01 10:00:00 -0800", "BTC Wallet", "bitcoin", "bc1qsynthetic000000000000000000000001", "", ""],
        [], [],
        ["TOTALS ***"], ["", "BTC", "EQUIV USD"], ["BALANCE", "0.00000000", "0.00"],
        ["BOUGHT", "0.01000000", "400.00"], [], ["", "USD"], ["DEPOSITED", "100.00", "100.00"], [], [],
        ["EXCHANGE TOTALS ***"], ["", "ETH", "EQUIV USD"], ["DEPOSITED", "0.5", "900.00"], [], [],
        ["TRANSACTIONS ***"],
        ["TIMESTAMP", "ACCOUNT NAME", "TYPE", "STATUS", "BALANCE", "AMOUNT", "CURRENCY", "TO",
         "PRO TRANSFER", "NOTES", "EQUIV USD", "TRANSACTION HASH", "PAYMENT METHOD DETAILS",
         "TRANSACTION ID", "NETWORK", "SURPLUS COL"],
        ["2021-03-14 01:59:59 -0800", "BTC Wallet", "Buy", "Complete", "0.01", "0.01000000", "BTC", "",
         "Not a Pro Transfer", "", "400.00", "", "Example Bank", "SYNTX0001", "bitcoin", "kept"],
        [],
        ["2021-03-14 03:00:00 -0700", "ETH Wallet", "Send", "Complete", "0", "-1.23E-7", "ETH",
         "0x0000000000000000000000000000000000000001", "Not a Pro Transfer", "gift", "0.00",
         "AA" * 32, "", "SYNTX0002", "ethereum", ""],
        ["2021-03-15 12:00:00", "BTC Wallet", "Receive", "Complete", "0.02", "0.01", "BTC", "", "", "",
         "410.00", "", "", "SYNTX0003", "bitcoin", ""],
        [], [],
        ["AMOUNT", "CURRENCY", "TIMESTAMP", "TYPE", "STATUS", "TRANSACTION ID", "NEW COLUMN"],
        ["2", "ETH", "March 9, 2025, 01:30am PST", "Receive", "Complete", "SYNTX0004", "extra"], [],
        ["CUSTOM LABEL", "CUSTOM VALUE"], ["alpha", "beta"], [], [],
        ["EXCHANGE TRANSFERS ***"], ["TIMESTAMP", "AMOUNT", "CURRENCY", "TYPE"],
        ["2021-04-01T00:00:00Z", "0.5", "ETH", "deposit"], [], [],
        ["EXCHANGE TRANSACTIONS ***"],
        ["TIMESTAMP", "ACCOUNT NAME", "TYPE", "BALANCE", "AMOUNT", "CURRENCY", "EQUIV USD", "ID"],
        ["2021-04-02T00:00:00Z", "ETH", "match", "0.4", "-0.1", "ETH", "180.00", "SYNEX0001"], [], [],
        ["EVENTS ***"], ["TIMESTAMP", "ACTION", "IP", "FINGERPRINT", "USER AGENT", "LOCATION", "SOURCE",
                         "DETAILS"],
        ["2021-01-05 16:28:04 -0800", "signin", "2001:db8::1", "SYNFP1", "", "", "web", ""],
        ["January 6, 2021, 04:28pm PST", "signin", "198.51.100.7", "SYNFP1", "", "Testville, US", "web", ""],
        [], [],
        ["MANUAL REVIEWS ***"], ["CREATED", "UPDATED", "STATUS", "REASON", "REASON VALUE"],
        ["2021-05-01 09:00:00 -0700", "2021-05-02 09:00:00 -0700", "resolved", "synthetic", "1"], [], [],
    ]
    if extra_rows:
        rows += [["MYSTERY SECTION ***"], ["KEY A", "VALUE A"], ["KEY B", "VALUE B", "THIRD COL"], [], [],
                 ["WIRES ***"], ["CREATED", "AMOUNT"], [], [],
                 ["EMPTY THING ***"], [], []]
    return csv_text(rows)


def write(rel, text):
    path = os.path.join(BASE, *rel.split("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def main():
    if os.path.exists(BASE):
        shutil.rmtree(BASE)
    first = report("SYNTHUSER000000000000000A", "Alex Sample", "alex@example.test")
    write("0000aaaa/compliance_report.csv", first)
    write("0000aaaa/Coinbase-SYNTHUSER-IdvComplianceReport-2025-01-01/compliance_report.csv", first)
    second = report("SYNTHUSER000000000000000B", "Blair Example", "blair@example.test", extra_rows=False)
    quoted = io.StringIO(newline="")
    csv.writer(quoted, quoting=csv.QUOTE_ALL, lineterminator="\n").writerows(csv.reader(io.StringIO(second)))
    write("0000bbbb/compliance_report.csv", quoted.getvalue())
    write("0000cccc/not_a_compliance_report.csv", "col1,col2\r\nx,y\r\n")
    print(f"Wrote synthetic Coinbase return to {BASE}")


if __name__ == "__main__":
    main()

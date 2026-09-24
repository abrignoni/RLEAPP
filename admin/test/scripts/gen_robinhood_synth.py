"""
Generate a synthetic Robinhood return for the robinhoodReturns tests.

Every value here is fabricated. A Robinhood production is subscriber PII, account numbers
and IP history end to end, so no real return can be sanitised into a fixture. The CSVs use
the column layouts of real exports and the PDFs are small hand-written PDF files that place
text where the real layouts place it, so the page-position readers are exercised without
any real document. Covered:

  - crypto transfers and orders with the trailing notice line real exports carry, which must
    be listed in Parsing Notes and not reported as a record; padded cells in the orders file
  - an IP log and a 1099 CSV
  - an Account Master whose Employment labels end page 1 with their values on page 2, a
    section outside the known label vocabulary, and a print footer URL carrying the full UUID
  - an Account Master with a row mixing known and unknown labels, an edit log where one
    wrapped line could belong to either neighbouring record and one is joined to no record
    (both must be kept as unattached text with a warning), and a section after the edit log
  - an Account Master printing every residential address component on its own row
  - an RHC crypto statement with holdings and activity on one page, and an RHF brokerage
    statement whose activity description wraps onto a second line

Synthetic PDF builders by Cyber Agents, Inc.

Usage:
    python admin/test/scripts/gen_robinhood_synth.py [output_dir]

Then zip the output folder and feed it to make_test_data.py.
"""
import csv
import io
import os
import shutil
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "synth_robinhood_return")


RH_TRANSFER_HDR = ["id", "created_at", "withdrawal_submitted_timestamp", "currency_code", "transfer_type", "amount", "network",
                   "network_fee", "native_network_fee", "usd_amount_at_request", "fiat_amount_at_request", "state", "to_address",
                   "address_tag", "blockchain_txn_id", "blockchain_txn_state"]


def csv_text(rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    for r in rows:
        w.writerow(r)
    return buf.getvalue()


def rh_transfers(rows=None, footer=True):
    rows = rows or [["T1", "2025-03-24T08:20:29.92436-04:00", "", "ETH", "deposit", "0.5", "ETHEREUM", "0", "0.0000012",
                     "23.5144288476887836", "23.5144288476887836", "succeeded", "0xabcdef0000000000000000000000000000000001", "",
                     "0X" + "AA" * 32, "confirmed"]]
    out = [RH_TRANSFER_HDR] + rows
    if footer:
        out.append(["Synthetic notice line for the transfers export, written to sit after the last record. Generated 01/01/2025."])
    return csv_text(out)


def rh_orders():
    hdr = ["UUID", "Time Entered", "Symbol", "Side", "Quantity", "State", "Order Type", "Leaves Quantity", "Entered Price", "Average Price", "Notional"]
    return csv_text([hdr,
                     ["O1", "03/24/2025, 08:17:57", "BTC", "Buy", " 0.001 ", "Filled", "Market", "0E-18", " $1.00 ", " $1.00 ", "($100.00)"],
                     ["O2", "03/24/2025, 08:18:57", "BTC", "Buy", " 1 ", "Canceled", "Limit", "1", " $100.00 ", "", "($100.00)"],
                     ["O3", "03/24/2025, 08:19:57", "BTC", "Sell", " 1 ", "Filled", "Limit", "0.5", " $100.00 ", " $100.00 ", " $50.00 "]])


def rh_iplog(acct="SYNTH00001"):
    hdr = ["account_number", "user__secret", "user__username", "device_platform", "user_agent", "event_date_time", "client_ip",
           "geo_ip", "geo_ip_timezone", "geo_ip_city_name", "geo_ip_country_name"]
    return csv_text([hdr, [acct, "SYNTHSECRET-0001", "synthuser", "iOS", "", "2024-03-21 09:30:02", "203.0.113.9", "203.0.113.9",
                           "Pacific/Honolulu", "Testcity", "United States"]])


def rh_1099(acct="SYNTH00001C"):
    hdr = ["1099-B", "ACCOUNT NUMBER", "TAX YEAR", "DATE ACQUIRED", "SALE DATE", "DESCRIPTION", "SHARES", "COST BASIS", "SALES PRICE",
           "TERM", "ORDINARY", "FED TAX WITHHELD", "WASH AMT DISALLOWED", "ACCRDMKTDISCOUNT", "FORM8949CODE", "GROSSPROCEEDSINDICATOR",
           "LOSSNOTALLOWED", "NON COVERED", "BASIS NOT SHOWN", "PAYER NAME1", "PAYER NAME2"]
    return csv_text([hdr,
                     ["1099-B", acct, "2024", "", "20240821", "Bitcoin", "0.1", "0", "150.00", "", "N", "", "0", "", "X", "", "", "1", "Y", "Payer", "Agent"],
                     ["1099-B", acct, "2024", "20241002", "20241215", "Ethereum", "0.02", "0", "77.31", "SHORT", "N", "", "0", "", "B", "", "", "", "N", "Payer", "Agent"]])


def make_pdf(pages, width=612, height=792):
    """pages: list of lists of (x, top, size, text). Helvetica text placed with baseline at height - top."""
    objs = []

    def add(body):
        objs.append(body)
        return len(objs)

    font = add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    pages_id = len(objs) + 1 + 2 * len(pages)
    kids = []
    for items in pages:
        ops = []
        for x, top, size, text in items:
            t = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            ops.append(f"BT /F1 {size} Tf 1 0 0 1 {x} {height - top} Tm ({t}) Tj ET")
        stream = "\n".join(ops).encode("latin-1")
        cid = add(b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream")
        pid = add(f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 {width} {height}] "
                  f"/Resources << /Font << /F1 {font} 0 R >> >> /Contents {cid} 0 R >>".encode())
        kids.append(pid)
    add(f"<< /Type /Pages /Kids [{' '.join(f'{k} 0 R' for k in kids)}] /Count {len(kids)} >>".encode())
    cat = add(f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode())
    out = io.BytesIO()
    out.write(b"%PDF-1.4\n")
    offsets = []
    for i, body in enumerate(objs, start=1):
        offsets.append(out.tell())
        out.write(f"{i} 0 obj\n".encode() + body + b"\nendobj\n")
    xref = out.tell()
    out.write(f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode())
    for o in offsets:
        out.write(f"{o:010d} 00000 n \n".encode())
    out.write(f"trailer\n<< /Size {len(objs) + 1} /Root {cat} 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    return out.getvalue()


def account_master_pdf(page_break=True, unknown_label=True):
    """Two-page synthetic Account Master. Employment labels end page 1; values start page 2."""
    L, V = 51, 57
    p1 = [(24, 16, 8, "1/1/25, 9:00 AM Accounts | Major Oak"),
          (67, 55, 13.6, "Accounts : Account Master"),
          (51, 189, 10.2, "Identification Information"),
          (L, 210, 6.3, "First Name"), (198, 210, 6.3, "Last Name"), (453, 210, 6.3, "Email"),
          (V, 228, 6.3, "Test"), (205, 228, 6.3, "Person"), (459, 228, 6.3, "tester@example.test"),
          (51, 363, 10.2, "Account Information"),
          (L, 383, 6.3, "Account Number"), (183, 383, 6.3, "UUID"), (316, 383, 6.3, "Account Status"),
          (V, 401, 6.3, "SYNTH00001"), (190, 401, 6.3, "00000000-1111-2222-3333-4444"), (322, 401, 6.3, "Open")]
    if unknown_label:
        p1 += [(51, 440, 10.2, "Novel Section"), (L, 460, 6.3, "Brand New Label"), (V, 478, 6.3, "surprising value")]
    p1 += [(51, 735, 10.2, "Employment"),
           (L, 757, 6.3, "Status"), (183, 757, 6.3, "Occupation"), (316, 757, 6.3, "Employer"),
           (24, 769, 8, "https://oak.robinhood.com/accounts/master/v3/00000000-1111-2222-3333-444455556666?x=1")]
    p2 = [(24, 16, 8, "1/1/25, 9:00 AM Accounts | Major Oak"),
          (V, 35, 6.3, "Employed"), (190, 35, 6.3, "tester"), (322, 35, 6.3, "Example Employer"),
          (51, 80, 10.2, "Cash Management Agreements"),
          (51, 100, 7.3, "CASH MANAGEMENT CUSTOMER AGREEMENT"), (51, 118, 7.3, "ACCEPTED"), (200, 118, 7.3, "No")]
    return make_pdf([p1, p2] if page_break else [p1 + p2])


def account_master_edit_pdf():
    """Mixed known/unknown label row, an edit log with irregular wrapping, then a normal section after it."""
    L, V = 51, 57
    hx = [51, 120, 200, 290, 380, 480]
    hdr = ["Model", "Field", "Previous Value", "New Value", "Author", "Timestamp"]
    def erow(top, vals):
        return [(hx[k] + 2, top, 6.3, v) for k, v in enumerate(vals) if v]
    p = [(24, 16, 8, "1/1/25, 9:00 AM Accounts | Major Oak"),
         (67, 55, 13.6, "Accounts : Account Master"),
         (51, 100, 10.2, "Identification Information"),
         (L, 120, 6.3, "First Name"), (198, 120, 6.3, "Mystery Label"), (453, 120, 6.3, "Email"),
         (V, 138, 6.3, "Test"), (205, 138, 6.3, "mystery value"), (459, 138, 6.3, "tester@example.test"),
         (51, 170, 10.2, "Brokeback edit logs")]
    p += [(hx[k], 186, 6.3, h) for k, h in enumerate(hdr)]
    p += erow(200, ["user", "first_name", "Old", "Test", "a@example.test", "Jan 2, 2025, 10:00:00 AM EST"])
    p += [(hx[2] + 2, 212, 6.3, "ambiguous line")]
    p += erow(224, ["user", "last_name", "Prev", "Person", "a@example.test", "Jan 3, 2025, 10:00:00 AM EST"])
    p += erow(260, ["address", "street", "1 Old", "2 New", "a@example.test", "Jan 4, 2025, 10:00:00 AM EST"])
    p += [(hx[3] + 2, 269, 6.3, "Street Apt 5")]
    p += [(hx[1] + 2, 320, 6.3, "stranded text")]
    p += [(51, 360, 10.2, "Employment"),
          (L, 380, 6.3, "Status"), (183, 380, 6.3, "Employer"),
          (V, 398, 6.3, "Employed"), (190, 398, 6.3, "After Edit Employer")]
    return make_pdf([p])


def account_master_address_pdf():
    """Residential address with every component on its own label/value row."""
    L, V = 51, 57
    p = [(24, 16, 8, "1/1/25, 9:00 AM Accounts | Major Oak"),
         (67, 55, 13.6, "Accounts : Account Master"),
         (51, 100, 10.2, "Account Information"),
         (L, 120, 6.3, "Account Number"), (V, 138, 6.3, "SYNTH00009"),
         (51, 170, 10.2, "Residential Address")]
    top = 190
    for lab, val in (("Line1", "100 Example Street"), ("Line2", "Apt 7"), ("City", "Testville"),
                     ("State", "KY"), ("Postal Code", "40324"), ("Country", "US")):
        p += [(L, top, 6.3, lab), (V, top + 18, 6.3, val)]
        top += 40
    return make_pdf([p])


def rhc_statement_pdf():
    """Holdings and activity on the same page."""
    p = [(312, 24, 12, "Crypto Statement"),
         (26, 66, 9, "NAME"), (144, 64, 12, "Test Person"),
         (26, 86, 9, "ACCOUNT NUMBER"), (144, 84, 12, "SYNTHRHC01"),
         (26, 106, 9, "RHS ACCOUNT NUMBER"), (144, 104, 12, "SYNTH00001"),
         (26, 126, 9, "PERIOD END"), (144, 124, 12, "2025-01-31"),
         (25, 283, 12, "PORTFOLIO ALLOCATION"),
         (24, 433, 8, "CRYPTOCURRENCY HELD IN ACCOUNT"), (253, 433, 8, "QUANTITY"), (302, 433, 8, "SYMBOL"), (388, 433, 8, "MARKET VALUE ON 2025/01/31"),
         (24, 454, 8, "Bitcoin"), (246, 454, 8, "0.001"), (302, 454, 8, "BTC"), (477, 454, 8, "$100.00"),
         (30, 500, 10, "ACCOUNT ACTIVITY"),
         (24, 520, 8, "DATE"), (87, 520, 8, "TRANSACTION TYPE"), (234, 520, 8, "DEBIT"), (320, 520, 8, "CREDIT"), (408, 520, 8, "PRICE"), (475, 520, 8, "VALUE"),
         (24, 541, 8, "2025-01-04"), (87, 541, 8, "Crypto Purchase"), (249, 541, 8, "--"), (304, 541, 8, "0.001 BTC"), (368, 541, 8, "$100000.00"), (472, 541, 8, "$100.00")]
    return make_pdf([p])


def rhf_statement_pdf():
    """Activity table with a wrapped description line followed by another valid row."""
    p1 = [(665, 85, 8.7, "Test Person Account #:900000001"), (701, 71, 8.7, "01/01/2025 to 01/31/2025"),
          (36, 128, 8.7, "Account Summary"), (36, 211, 10.1, "Portfolio Value"), (211, 211, 10.1, "$1.00"), (298, 211, 10.1, "$2.00"),
          (36, 250, 8.7, "AAPL 2 shares $300.00"),
          (36, 330, 8.7, "Robinhood Securities, LLC")]
    p3 = [(36, 75, 8.1, "Account Activity"),
          (36, 112, 6.9, "Description"), (248, 112, 6.9, "Symbol"), (313, 112, 6.9, "Acct Type"), (394, 112, 6.9, "Transaction"),
          (488, 112, 6.9, "Date"), (577, 112, 6.9, "Qty"), (616, 112, 6.9, "Price"), (666, 112, 6.9, "Debit"), (736, 112, 6.9, "Credit"),
          (36, 137, 6.9, "ACH Deposit from a"), (313, 137, 6.9, "Margin"), (394, 137, 6.9, "ACH"), (488, 137, 6.9, "01/02/2025"), (736, 137, 6.9, "$50.00"),
          (36, 147, 6.9, "long named bank"),
          (36, 170, 6.9, "Crypto Money Movement"), (313, 170, 6.9, "Margin"), (394, 170, 6.9, "COIN"), (488, 170, 6.9, "01/03/2025"), (666, 170, 6.9, "$10.00"),
          (36, 200, 6.9, "Total Funds Paid and Received"), (666, 200, 6.9, "$10.00"), (736, 200, 6.9, "$50.00")]
    return make_pdf([p1, p3], width=800)


def write(rel, data):
    path = os.path.join(BASE, *rel.split("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(data if isinstance(data, bytes) else data.encode("utf-8"))


def main():
    if os.path.exists(BASE):
        shutil.rmtree(BASE)
    prod = "Final Production-SYNTH"
    write(f"{prod}/RHC/crypto_account_transfers.csv", rh_transfers())
    write(f"{prod}/RHC/crypto_account_orders.csv", rh_orders() + "\r\n" + '"' + "Synthetic notice line. " * 4 + '"\r\n')
    write(f"{prod}/data_request_ip_timestamps_account_number__00000001__1__1.csv", rh_iplog("SYNTH00001"))
    write(f"{prod}/SYNTH00001 (RHF)/bulk_edocs_SYNTH00001/SYNTH00001_1099_2025-02-06.csv", rh_1099())
    write(f"{prod}/Account Master; AC Document.pdf", account_master_pdf())
    write(f"{prod}/Account Master edit logs.pdf", account_master_edit_pdf())
    write(f"{prod}/Account Master address.pdf", account_master_address_pdf())
    write(f"{prod}/RHC/00000000-0000-0000-0000-000000000001_rhc_statement_"
          f"00000000-0000-0000-0000-000000000002_2025-01-31.pdf", rhc_statement_pdf())
    write(f"{prod}/SYNTH00001 (RHF)/bulk_edocs_SYNTH00001/SYNTH00001_account_statement_2025-01-31.pdf",
          rhf_statement_pdf())
    print(f"Wrote synthetic Robinhood return to {BASE}")


if __name__ == "__main__":
    main()

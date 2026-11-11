"""
Generate a synthetic Binance return for the binanceReturns tests.

Every value here is fabricated. A Binance production is subscriber PII, identity documents,
wallet addresses and IP history end to end, so no real return can be sanitised into a
fixture. The workbooks use the sheet names, block titles and column headers observed in real
returns; the values are invented (documentation IP ranges, example.com addresses, SYNTH
identifiers) and the embedded images are plain colour squares.

Covered:

  - an 18-sheet workbook and an 8-sheet one, recognised by their sheets, not their names
  - a Customer Information heading with an ASCII and with a full-width parenthesis, a Basic
    Information record, and an API Information block with and without records
  - Account Balance blocks with records for every known layout, two blocks sharing one
    layout under different titles (one in Chinese), 'Note: empty data' blocks, blank rows
    inside a block, and an unrecognised block with records
  - plain sheets with records, header-only sheets followed by empty rows, an extra column
    the module does not name, a header with a trailing space, and the sheet name cut at
    Excel's 31-character limit
  - Access Logs with a timestamp that is not in the expected form
  - Approved Devices with bilingual and English-only headers, Key/Value pairs on and under
    each device row, a pair with an empty value and a pair above the first device
  - images anchored on KYC Documents, an image stored in the workbook but anchored on no
    sheet, and PNG bytes stored under a .jpeg name
  - a sheet the module does not recognise, and a decoy .xlsx without the Binance sheets

Usage:
    python admin/test/scripts/gen_binance_synth.py [output_dir]

Then zip the output folder and feed it to make_test_data.py.
"""
import io
import os
import shutil
import sys
import zipfile

import openpyxl
from openpyxl.drawing.image import Image as XLImage
from PIL import Image

BASE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "synth_binance_return")

CUSTOMER_HDR = ["User ID", "Email", "Mobile", "Registration time", "Name", "User nationality", "User ID number",
                "User authentication type", "User authentication time", "Status", "2FA", "2FA Opening time", "SMS",
                "SMS Opening time", "2FA Reset Information"]
API_HDR = ["Rule ID", "API Name", "Trade IP", "Withdraw IP", "Create Time", "Update Time"]
ASSETS_HDR = ["Asset Ticker", "Asset Name", "Total Position", "Estimated BTC Value", "Deposit Wallet Address",
              "Label/Tag/Memo"]
DEPOSIT_HDR = ["User ID", "Currency", "Amount", "BUSD", "Deposit Address", "Source Address", "TXID", "Create Time",
               "Status", "Network", "CounterParty ID"]
WITHDRAW_HDR = ["User ID", "Currency", "Amount", "BUSD", "Destination Address", "Label/Tag/Memo", "txId",
                "Apply Time", "Status", "Network", "CounterParty ID"]
ORDER_HDR = ["User ID", "Market ID", "Price", "Qty", "Average Price", "Remain Qty", "Trade Qty", "Time",
             "Update Time", "Side", "Status", "Type", "Stop Price", "Price Unit", "Amount Unit"]
FIAT_DEP_HDR = ["Status", "Create Time", "UserID", "Email", "Amount", "Currency", "Internal Serial Number",
                "External Serial Number", "Second External Serial Number", "Source Account Id",
                "Source Account Name", "Golden Channel", "Remark", "Is Replacement Order?", "Abnormal Reason",
                "Error Code", "Error Reason", "Channel Fee", "Platform Fee", "Completed Time", "Update Time",
                "Network Provider", "Expect Recharge Amount", "Narrative", "Source Account", "Arrived Time",
                "Order Type"]
FIAT_WD_HDR = ["Status", "Create Time", "UserID", "Email", "Amount", "Currency", "Internal Serial Number",
               "External Serial Number", "Target Account Id", "Target Name", "Withdraw Channel", "Remark",
               "Is Replacement Order?", "Abnormal Reason", "Error Reason", "Channel Fee", "Platform Fee",
               "Completed Time", "Update Time", "Network Provider", "Withdrawer", "Narrative", "Target Account",
               "Arrived Time", "Bic", "Bank", "Country", "Sortcode", "Bank Address", "Bank City", "Iban",
               "Flutterwave Proof"]
ACCESS_HDR = ["User ID", "Operation", "Client", "Client Version", "Real IP", "Geolocation", "Browser",
              "Timestamp (UTC)"]
DEVICE_HDR_EN = ["Device Name", "Client", "IP Address", "Geolocation", "Recent Usage Timestamp (UTC)", "Status",
                 "Key", "Value"]
DEVICE_HDR_BI = ["Device Name 设备名称", "Client 客户端", "IP Address IP地址", "Geolocation 地理位置",
                 "Recent Usage Timestamp (UTC) 最近使用时间戳（UTC）", "Status 状态", "Key 程序键", "Value 键值"]
OTC_PAY_HDR = ["User ID", "Receiving Payment ID", "Name", "Payment method", "Bank account number", "Bank name",
               "Account opening branch"]
FUNDING_HDR = ["User ID", "TotalAsset", "TotalAsset BUSD", "AssetCode", "AssetName", "Freeze", "Withdrawing",
               "Free", "Locked"]
SEND_HDR = ["Send number", "Payer account type", "Payer type", "Payee account type", "Amount", "Asset",
            "Assets BTC rate", "Send note", "Send type", "Send source", "Send status", "Send time", "Complete time",
            "Update time"]
PAY_HDR = ["User ID", "Merchant Name", "Transaction Type", "Currency", "Amount", "Transaction Time"]
OTC_TRADE_HDR = ["OrderId", "UserId", "ChannelCode", "QuoteId", "PayType", "UserStatus", "UserCurrentPhase",
                 "ChannelStatus", "ChannelCurrentPhase", "symbol", "BaseCoin", "QuoteCoin", "BaseCoinAmount",
                 "QuoteCoinAmount", "SpreadAmount", "SpreadCoin", "UserQuotePrice", "UserSpreadPrice",
                 "ChannelQuotePrice", "RequestAmount", "RequestAmountCoin", "TransId", "OtcUserId", "SpreadUserId",
                 "ChannelUserId", "CreateTime", "UpdateTime", "UserCompletedTime", "ChannelCompletedTime",
                 "UserRemark", "ChannelRemark"]
CARD_HDR = ["Swipe Card ID", "Swipe User ID", "Card Number", "Card Type", "Locked", "Freeze", "Activated",
            "Card Status", "Create Date"]
CARD_TX_HDR = ["Swipe Card ID", "Transaction ID", "Merchant Name", "Status", "Type", "Currency", "Channel",
               "Approved", "Total", "Created date"]

SPOT_HDR = ["Currency Name", "Currency Code", "All Positions", "Available Positions", "In Withdrawal",
            "Pending Order", "BTC Equivalent"]
FUT_POS_HDR = ["Symbol", "Position Amount", "Entry Price", "Mark Price", "Unrealized Profit"]
FUT_BAL_HDR = ["Asset", "Wallet Balance", "Unrealized Profit", "Available For Order"]
FUT_COL_HDR = ["asset", "locked", "Loan Amount(USDT)", "Total Principal For Interest(USDT)", "Current Rate",
               "Initial Rate", "Liquidation Collateral Rate", "Liquidation Price", "Total Interest(USDT)"]
CROSS_HDR = ["Currency", "Total Balance", "Available Balance", "Borrowed", "Interest"]
ISOLATED_HDR = ["Trading Pair", "Risk Ratio", "Effective Multiple", "Currency", "Total Balance",
                "Available Balance", "Borrowed"]

EMPTY_TITLES = ["Earn - 币安宝账户 - 活期", "Earn - 币安宝账户 - 定期", "Earn - 币安宝账户 - 活动",
                "Earn - 币安宝账户 - 体验金", "Earn - 锁仓收益 - 活期", "Earn - 锁仓收益 - 定期",
                "Earn - defi挖矿 - 活期", "Earn - defi挖矿 - 定期", "Fiat"]


def put(ws, rows):
    for r, row in enumerate(rows, 1):
        for c, value in enumerate(row or [], 1):
            if value is not None:
                ws.cell(row=r, column=c, value=value)


def table(wb, name, header, records, trailing_blank=0):
    ws = wb.create_sheet(name)
    put(ws, [header] + records)
    if trailing_blank:
        # Real returns carried header-only sheets whose dimension ran several rows past
        # the header; an empty-string cell reproduces the extra rows.
        ws.cell(row=1 + len(records) + trailing_blank, column=1, value="")
    return ws


def balance_rows(blocks):
    rows = [None]
    for title, header, records in blocks:
        rows.append([title])
        if header is None:
            rows.append(["Note: empty data"])
        else:
            rows.append(header)
            rows.extend(records)
        rows.extend([None, None])
    return rows


def jpeg(colour):
    out = io.BytesIO()
    Image.new("RGB", (64, 48), colour).save(out, "JPEG")
    out.seek(0)
    return out


def png_bytes(colour):
    out = io.BytesIO()
    Image.new("RGB", (32, 32), colour).save(out, "PNG")
    return out.getvalue()


def customer(wb, user_id, email, fullwidth, api_rows):
    ws = wb.active
    ws.title = "Customer Information"
    paren = "（" if fullwidth else "("
    heading = (f"User Basic Information{paren}id: {user_id}  email: {email} "
               f"time: 2021-01-01 00:00:00 - 2022-01-01 00:00:00)")
    put(ws, [[heading], None, ["Basic Information"], CUSTOMER_HDR,
             [user_id, email, "", "2020-05-06 07:08:09", "SYNTH PERSON ONE", "", "SYNTH-ID-0001", "SYNTH_KYC",
              "2020-05-07 08:09:10", "Normal", "true", "", "false", "", "[]"],
             None, None, None, ["API Information"], API_HDR] + api_rows)


def devices(wb, header, rows):
    ws = wb.create_sheet("Approved Devices")
    put(ws, [header] + rows)


def access(wb, user_id, records):
    table(wb, "Access Logs", ACCESS_HDR, [[user_id] + r for r in records])


def kyc(wb, colours):
    ws = wb.create_sheet("KYC Documents")
    for i, colour in enumerate(colours):
        img = XLImage(jpeg(colour))
        ws.add_image(img, f"A{1 + i * 20}")


def add_orphan_media(path):
    """Store PNG bytes under xl/media/ with a .jpeg name, referenced by no drawing."""
    tmp = path + ".tmp"
    with zipfile.ZipFile(path) as src, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            dst.writestr(item, src.read(item.filename))
        dst.writestr("xl/media/image90.jpeg", png_bytes((10, 120, 200)))
    os.replace(tmp, path)


def workbook_18(path):
    uid = "90000001"
    wb = openpyxl.Workbook()
    customer(wb, uid, "synth.one@example.com", False,
             [["SYNTH-RULE-1", "synth-api", "192.0.2.10", "192.0.2.11", "2021-03-04 05:06:07",
               "2021-03-05 05:06:07"]])
    ws = wb.create_sheet("Account Balance")
    put(ws, balance_rows([
        ("Spot", SPOT_HDR, [["SynthCoin", "SYC", "1.50000000", "1.00000000", "0.50000000", "0", "0.00010000"],
                            ["TestToken", "TST", "20", "20", "0", "0", "0.00000100"]]),
        ("Futures USDT position", FUT_POS_HDR, [["SYCUSDT", "0.010", "100.0", "101.5", "0.015"], None, None,
                                                ["TSTUSDT", "-2", "3.00", "2.90", "0.20"]]),
        ("Futures USDT balance", FUT_BAL_HDR, [["USDT", "10.00000000", "0.21712345", "9.00000000"]]),
        ("Futures USDT Collateral", FUT_COL_HDR, [["SYC", "0.5", "20", "20", "0.0001", "0.65", "0.91", "40",
                                                   "0.01"]]),
        ("Futures 币本位 position", FUT_POS_HDR, [["SYCUSD_PERP", "1", "100", "99", "-0.0001"]]),
        ("Futures 币本位 balance", FUT_BAL_HDR, [["SYC", "0.20000000", "-0.00010000", "0.19000000"]]),
    ] + [(t, None, []) for t in EMPTY_TITLES] + [
        ("Margin - Cross", CROSS_HDR, [["SYC", "1", "1", "0", "0"]]),
        ("Margin - Isolated", ISOLATED_HDR, [["SYCUSDT", "999", "1", "SYC", "1", "1", "0"]]),
        ("Pool", ["SYNTH Pool Name", "SYNTH Pool Amount"], [["synth-pool", "3.0"]]),
    ]))
    table(wb, "Current Assets & Wallets", ASSETS_HDR,
          [["SYC", "SynthCoin", "1.5", "0.0001", "synthaddr0000000000000000000001", ""],
           ["TST", "TestToken", "20", "0.000001", "synthaddr0000000000000000000002", "SYNTHMEMO1"]])
    table(wb, "Order History", ORDER_HDR,
          [[uid, "SYCUSDT", "100", "0.01", "100", "0", "0.01", "2021-06-01 10:00:00", "2021-06-01 10:00:01",
            "BUY", "FILLED", "LIMIT", "0", "USDT", "SYC"]])
    table(wb, "Deposit History", DEPOSIT_HDR + ["SYNTH Extra Column"],
          [[uid, "SYC", "1.5", "150", "synthaddr0000000000000000000001", "synthsrc0000000000000000000009",
            "synthtx0000000000000000000000000000000000000000000000000000000001", "2021-05-01 12:00:00",
            "Completed", "SYNTHNET", "", "extra-value-1"],
           [uid, "TST", "20", "0.2", "synthaddr0000000000000000000002", "",
            "synthtx0000000000000000000000000000000000000000000000000000000002", "2021-05-02 12:00:00",
            "Completed", "SYNTHNET", "SYNTH-CP-1", ""]])
    table(wb, "Fiat Deposit History", FIAT_DEP_HDR,
          [["Successful", "2021-04-01 09:00:00", uid, "synth.one@example.com", "100", "EUR", "SYNTH-IN-1",
            "SYNTH-EX-1", "", "SYNTH-SRC-ACC-1", "SYNTH HOLDER", "SYNTHCHANNEL", "", "false", "", "", "", "0",
            "0", "2021-04-01 09:05:00", "2021-04-01 09:05:00", "SYNTHPROVIDER", "100", "", "SYNTH-ACC-1",
            "2021-04-01 09:04:00", "SYNTHTYPE"]])
    wd = table(wb, "Withdrawal History", WITHDRAW_HDR,
               [[uid, "SYC", "0.5", "50", "synthdest000000000000000000001", "",
                 "synthtx0000000000000000000000000000000000000000000000000000000003", "2021-07-01 08:00:00",
                 "Completed", "SYNTHNET", ""]])
    wd.cell(row=1, column=5, value="Destination Address ")
    table(wb, "Fiat Withdrawal History", FIAT_WD_HDR, [], trailing_blank=9)
    access(wb, uid, [["User login", "web", "1.0", "198.51.100.7", "Synthland", "SynthBrowser",
                      "2021-08-01 01:02:03"],
                     ["Authorized device", "android", "2.0", "198.51.100.8", "Synthland", "", "2021-08-02 01:02:03"],
                     ["User login", "web", "1.0", "198.51.100.9", "Synthland", "SynthBrowser", "not-a-timestamp"]])
    devices(wb, DEVICE_HDR_BI, [
        [None, None, None, None, None, None, "orphan_key", "orphan-value"],
        ["SYNTH-PHONE", "android", "203.0.113.5", "Synthland", "2021-08-02 01:02:03", "Normal", "a_sdk", "30"],
        [None, None, None, None, None, None, "device_name", "SYNTH-PHONE"],
        [None, None, None, None, None, None, "a_imei", ""],
        ["SYNTH-BROWSER", "web", "203.0.113.6", "Synthland", "2021-08-01 01:02:03", "Deleted", "user_agent",
         "SynthBrowser/1.0"],
        [None, None, None, None, None, None, "screen_resolution", "640,480"],
    ])
    kyc(wb, [(200, 40, 40), (40, 200, 40)])
    table(wb, "OTC Payment", OTC_PAY_HDR, [], trailing_blank=9)
    table(wb, "Funding Wallet", FUNDING_HDR, [[uid, "1", "1", "SYC", "SynthCoin", "0", "0", "1", "0"]])
    table(wb, "Binance Send", SEND_HDR,
          [["SYNTH-SEND-1", "SPOT", "USER", "SPOT", "1", "SYC", "0.0001", "", "TRANSFER", "APP", "SUCCESS",
            "2021-09-01 00:00:00", "2021-09-01 00:00:05", "2021-09-01 00:00:05"]])
    table(wb, "Binance Pay", PAY_HDR, [[uid, "SYNTH MERCHANT", "PAY", "TST", "5", "2021-09-02 00:00:00"]])
    table(wb, "OTC Trading", OTC_TRADE_HDR,
          [["SYNTH-OTC-1", uid, "SYNTHCH", "SYNTH-Q-1", "CARD", "DONE", "FINAL", "DONE", "FINAL", "SYCEUR",
            "SYC", "EUR", "1", "100", "1", "EUR", "100", "1", "99", "100", "EUR", "SYNTH-T-1", "SYNTH-U-1",
            "SYNTH-U-2", "SYNTH-U-3", "2021-10-01 00:00:00", "2021-10-01 00:01:00", "2021-10-01 00:01:00",
            "2021-10-01 00:01:00", "", ""]])
    table(wb, "Binance Card", CARD_HDR,
          [["SYNTH-CARD-1", uid, "0000-SYNTH-0000", "VIRTUAL", "false", "false", "true", "ACTIVE",
            "2021-11-01 00:00:00"]])
    table(wb, "Binance Card transaction histor", CARD_TX_HDR,
          [["SYNTH-CARD-1", "SYNTH-CTX-1", "SYNTH SHOP", "APPROVED", "PURCHASE", "EUR", "POS", "true", "9.99",
            "2021-11-02 00:00:00"]])
    extra = wb.create_sheet("SYNTH Unknown Sheet")
    put(extra, [["SYNTH Label", "SYNTH Value"], ["synth-a", "1"]])
    wb.save(path)
    add_orphan_media(path)


def workbook_8(path):
    uid = "90000002"
    wb = openpyxl.Workbook()
    customer(wb, uid, "synth.two@example.com", True, [])
    ws = wb.create_sheet("Account Balance")
    put(ws, balance_rows([
        ("Spot", None, []), ("Futures USDT position", None, []), ("Futures USDT balance", None, []),
        ("Futures USDT Collateral", None, []), ("Futures 币本位 position", None, []),
        ("Futures 币本位 balance", None, []),
    ] + [(t, None, []) for t in EMPTY_TITLES] + [
        ("Margin - Cross", None, []), ("Margin - Isolated", None, []), ("Pool", None, []),
    ]))
    table(wb, "Current Assets & Wallets", ASSETS_HDR,
          [["SYC", "SynthCoin", "0", "0", "synthaddr0000000000000000000003", ""]])
    table(wb, "Deposit History", DEPOSIT_HDR,
          [[uid, "SYC", "2", "200", "synthaddr0000000000000000000003", "",
            "synthtx0000000000000000000000000000000000000000000000000000000004", "2021-02-01 12:00:00",
            "Completed", "SYNTHNET", ""]])
    table(wb, "Withdrawal History", WITHDRAW_HDR,
          [[uid, "SYC", "2", "200", "synthdest000000000000000000002", "",
            "synthtx0000000000000000000000000000000000000000000000000000000005", "2021-02-02 12:00:00",
            "Completed", "SYNTHNET", ""]])
    access(wb, uid, [["User login", "ios", "3.0", "192.0.2.50", "Synthland", "", "2021-02-01 11:59:00"]])
    devices(wb, DEVICE_HDR_EN, [
        ["SYNTH-TABLET", "ios", "192.0.2.50", "Synthland", "2021-02-01 11:59:00", "Normal", "platform", "ios"],
        [None, None, None, None, None, None, "system_lang", "xx"],
    ])
    kyc(wb, [(40, 40, 200)])
    wb.save(path)


def decoy(path):
    wb = openpyxl.Workbook()
    wb.active.title = "Customer Information"
    put(wb.active, [["Not a Binance return"], ["SYNTH", "decoy"]])
    wb.save(path)


def main():
    if os.path.isdir(BASE):
        shutil.rmtree(BASE)
    os.makedirs(os.path.join(BASE, "account_one"))
    os.makedirs(os.path.join(BASE, "account_two"))
    workbook_18(os.path.join(BASE, "account_one", "SYNTH_binance_return_18_sheets.xlsx"))
    workbook_8(os.path.join(BASE, "account_two", "SYNTH_binance_return_8_sheets.xlsx"))
    decoy(os.path.join(BASE, "SYNTH_not_a_binance_return.xlsx"))
    print(f"Synthetic Binance return written to {BASE}")


if __name__ == "__main__":
    main()

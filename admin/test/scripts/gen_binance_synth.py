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
  - a workbook in the 2024 layout: First/Last Name, Tax ID and TnC columns, the KYC Approved
    Info, Address Validation and Sub-accounts blocks and an unrecognised block in Customer
    Information; Assets Overview with its total overview lines above the first block and every
    block layout seen there; asset logs, P2P, attempted withdrawals, margin orders, gift cards,
    loans and repayments; the camel-case Fiat layout on two sheets and a Fiat sheet whose header
    matches no layout; extra columns on the sheets the 2022 layout already had; an empty KYC
    Documents sheet; and Approved Devices with English-only headers and two empty columns

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


# ------------------------------------------------------------------ the 2024 layout
FIAT_ORDER_HDR = ["userId", "userEmail", "userName", "orderId", "businessType", "currency", "cryptoCurrency",
                  "grossAmount", "cryptoAmount", "cryptoObtainAmount", "orderExecutePrice", "cryptoNetwork",
                  "cryptoAddress", "cryptoAddressMemo", "userFee", "merchantFee", "networkFee", "channelName",
                  "transactionMethod", "cardBin", "cardLast4Digital", "statusName", "viban", "orderCreateTime",
                  "channelOrderId", "iban", "accountNumber", "receivableAccount", "payableAccount",
                  "cryptoTransactionHash", "grossAmountUsd"]
ASSET_LOG_HDR = ["Order Number", "Commission ID", "User ID", "Currency", "Type", "Amount", "Available", "Locked",
                 "Freeze", "Processing", "Description", "Time"]
ORDER24_HDR = ORDER_HDR + ["USDT equivalent", "Operation Source"]


def customer_2024(wb, user_id, email):
    ws = wb.active
    ws.title = "Customer Information"
    heading = (f"User Basic Information(id: {user_id}  email: {email} "
               f"time: 2023-01-01 00:00:00 - 2024-01-01 00:00:00)")
    put(ws, [[heading], None, ["Basic Information"],
             ["User ID", "Email", "Mobile", "Registration time", "First Name", "Last Name", "User nationality",
              "User ID number", "User authentication type", "User authentication time", "Status", "2FA",
              "2FA Opening time", "SMS", "SMS Opening time", "2FA Reset Information", "Tax ID", "TnC",
              "TnC Sign Date"],
             [user_id, email, "'+000000000000", "2022-03-04 05:06:07", "SYNTH", "PERSON THREE", "XX",
              "SYNTH-ID-0003", "SYNTH_KYC", "2022-03-05 06:07:08", "Normal", "true", "", "0000000000", "", "",
              "SYNTH-TAX-3", "true", "2022-03-04 05:06:07"],
             None, None, None, ["API Information"], API_HDR, None, None, None,
             ["KYC Approved Info"],
             ["Birthday", "ID issue Country", "ID Address", "ID type", "ID Sub-type", "issuing Authority",
              "Issuing Date", "ID expiry Date"],
             ["1900-01-01", "XX", "", "SYNTH_ID", "SYNTH_SUB", "", "", "2099-12-31"],
             None, None, None,
             ["Address Validation"], ["Residence", "Region/State", "City", "Address", "Postal/Zip Code"],
             None, None, None,
             ["Sub-accounts"], ["Has Sub-account", "Sub-account Number"], ["false", "0"],
             None, None,
             ["SYNTH Extra Block"], ["SYNTH Field A", "SYNTH Field B"], ["synth-value-a", "synth-value-b"]])


def assets_overview(wb):
    ws = wb.create_sheet("Assets Overview")
    rows = [None, None, ["total overview"], ["Estimate Total Balance(BTC)"], ["0.123456789"], None, None, None,
            ["single overview"],
            ["Spot(BTC)", "Futures(BTC)", "Earn(BTC)", "MARGIN(BTC)", "Pool(BTC)", "Funding(BTC)", "Option(BTC)"],
            ["0.1", "0", "0.02", "0", "0", "0.003", "0"]]
    rows += balance_rows([
        ("Spot", SPOT_HDR + ["USDT Equivalent"],
         [["SynthCoin", "SYC", "2.5", "2.0", "0.5", "0", "0.0002", "25.5"]]),
        ("Futures USDT balance", FUT_BAL_HDR + ["USDT Equivalent"], [["USDT", "5", "0", "5", "5"]]),
        ("Futures USDT Collateral", None, []),
        ("Futures USDT position", FUT_POS_HDR + ["USDT Equivalent"], [["SYCUSDT", "0.5", "10", "11", "0.5", "5.5"]]),
        ("Futures Coin balance", FUT_BAL_HDR + ["USDT Equivalent"], [["SYC", "0.1", "0", "0.1", "1.1"]]),
        ("Futures Coin position", FUT_POS_HDR + ["USDT Equivalent"], [["SYCUSD_PERP", "1", "10", "10", "0", "0"]]),
        ("Earn - flexible savings",
         ["Product Name", "Total Amount", "Accruing Interest", "Today Purchased Amount", "Redeeming Amount",
          "Total Interest", "Average Annual Interest Rate", "USDT Equivalent"],
         [["SYC", "3.0", "3.0", "", "0", "0.001", "", "33"]]),
        ("Earn - Saving - Locked Staking",
         ["Currency Name", "Currency Code", "All Positions", "BTC Equivalent", "USDT Equivalent",
          "Position Status"], [["SynthCoin", "SYC", "100.5", "0.01", "110.5", "HOLDING"]]),
        ("Earn - fixed savings", None, []),
        ("Earn - Autoinvest - My Index-Linked",
         ["Currency Name", "Currency Code", "All Positions", "BTC Equivalent", "USDT Equivalent"],
         [["TestToken", "TST", "7", "0", "0.7"]]),
        ("Fiat", None, []),
        ("Margin - Cross", CROSS_HDR + ["USDT Equivalent"], [["SYC", "", "1", "0", "0", "11"]]),
        ("Margin - Isolated", ISOLATED_HDR + ["USDT Equivalent"],
         [["SYC/USDT", "'-", "'-", "'-", "'-", "'-", "'-", "'-"]]),
        ("Pool", None, []),
        ("Funding", ["Currency Name", "Currency Code", "All Positions", "BTC Equivalent", "USDT Equivalent"],
         [["TestToken", "TST", "1", "0", "0.1"]]),
    ])
    put(ws, rows)


def workbook_2024(path):
    uid = "90000003"
    wb = openpyxl.Workbook()
    customer_2024(wb, uid, "synth.three@example.com")
    wb.create_sheet("KYC Documents")
    table(wb, "Funding Wallet", ["User ID", "TotalAsset", "TotalAsset USDT", "AssetCode", "AssetName", "Freeze",
                                 "Withdrawing", "Free", "Locked"],
          [[uid, "1.5E-5", "1.5E-5", "TST", "TestToken", "0", "0", "1.5E-5", "0"]], trailing_blank=8)
    assets_overview(wb)
    table(wb, "Spot Asset Log", ASSET_LOG_HDR,
          [["900000000001", "", uid, "SYC", "SYNTH TRANSFER", "1", "1", "0", "0", "0", "synth note",
            "2023-02-01 10:00:00"],
           ["900000000002", "", uid, "TST", "SYNTH TRADE", "-2", "8", "0", "0", "0", "",
            "2023-02-02 10:00:00"]])
    table(wb, "Funding Asset Log", ASSET_LOG_HDR,
          [["900000000003", "", uid, "TST", "SYNTH P2P", "-5", "3", "0", "0", "0", "SYNTH-P2P-1",
            "2023-02-03 10:00:00"]])
    table(wb, "Fiat payment methods",
          ["User ID", "Card ID", "Card Number", "First Name", "Family Name", "Card Country", "Card Scheme",
           "Bind Type", "Security Type", "expired date", "bank", "cardType", "Create Time", "Update Time"],
          [[uid, "SYNTH-CARD-ID", "0000-SYNTH", "SYNTH", "PERSON", "XX", "SYNTHSCHEME", "SYNTH", "SYNTH",
            "2099-01", "SYNTH BANK", "DEBIT", "2023-01-01 00:00:00", "2023-01-02 00:00:00"]])
    fiat_record = [uid, "synth.three@example.com", "SYNTH PERSON", "SYNTH-ORDER-1", "BUY", "EUR", "SYC", "10",
                   "1", "1", "10", "SYNTHNET", "synthaddr0000000000000000000004", "", "0.1", "0", "0",
                   "SYNTHCHANNEL", "CARD", "000000", "0000", "Completed", "", "2023-03-01 00:00:00",
                   "SYNTH-CH-1", "", "", "", "", "synthtx0000000000000000000000000000000000000000000000000000000006",
                   "11"]
    table(wb, "Fiat Deposit History", FIAT_ORDER_HDR, [fiat_record])
    table(wb, "Fiat Withdrawal History", ["SYNTH Unknown Fiat Header", "SYNTH Other"], [["synth-x", "1"]])
    table(wb, "Fiat Trades", FIAT_ORDER_HDR, [fiat_record[:3] + ["SYNTH-ORDER-2"] + fiat_record[4:]])
    table(wb, "Deposit History",
          ["User ID", "Currency", "Amount", "Account Type", "USDT", "Deposit Address", "Source Address", "TXID",
           "Create Time", "Status", "Network", "CounterParty ID"],
          [[uid, "SYC", "3", "Spot Account", "30", "synthaddr0000000000000000000005", "synthsrc000000000000000002",
            "synthtx0000000000000000000000000000000000000000000000000000000007", "2023-04-01 00:00:00",
            "Completed", "SYNTHNET", ""]])
    table(wb, "Withdrawal History",
          ["User ID", "Currency", "Amount", "Account Type", "USDT", "Destination Address", "Label/Tag/Memo",
           "txId", "Apply Time", "Status", "Network", "CounterParty ID"],
          [[uid, "SYC", "1", "Funding Account", "10", "synthdest000000000000000000003", "",
            "synthtx0000000000000000000000000000000000000000000000000000000008", "2023-04-02 00:00:00",
            "Completed", "SYNTHNET", ""]])
    table(wb, "ATTEMPTED WITHDRAWAL HISTORY",
          ["User ID", "Asset", "Network", "Amount", "Address", "Date", "Business Type", "Source", "DecisionCode",
           "USDT Equivalent"],
          [[uid, "SYC", "SYNTHNET", "9", "synthdest000000000000000000004", "2023-04-03 00:00:00", "WITHDRAW",
            "APP", "SYNTH-CODE", "90"]])
    table(wb, "Binance Pay",
          ["User ID", "Transaction wallet ID", "Merchant Name", "Counterparty Wallet ID", "Counterparty Binance ID",
           "Order ID", "Transaction ID", "Transaction Type", "Currency", "Amount", "Transaction Time",
           "USDT equivalent"],
          [[uid, "900000001", "", "900000002", "900000003", "900000000000000001", "S_P_900000000000000001", "C2C",
            "TST", "-1.5", "2023-05-01 00:00:00", "-0.15"]])
    table(wb, "P2P",
          ["Target UID", "Order ID", "Ad number", "Buy or Sell", "Crypto", "Amount", "Fiat Currency",
           "Total Amount", "Unit Price", "Take ID", "Ad publisher ID", "Create Time", "Status", "Payment method",
           "Client", "Payment Time", "Release time", "Update time", "USDT equivalent"],
          [["90000009", "90000000000000000001", "90000000000000000002", "Buy", "TST", "100", "XXX", "1000.5",
            "10.005", "90000008", "900000007", "2023-06-01 00:00:00", "Completed", "SYNTHPAY", "web",
            "2023-06-01 00:05:00", "2023-06-01 00:10:00", "2023-06-01 00:10:00", "100"]])
    table(wb, "Order History", ORDER24_HDR,
          [[uid, "SYCUSDT", "11", "1", "11", "0", "1", "2023-07-01 00:00:00", "2023-07-01 00:00:01", "SELL",
            "FILLED", "LIMIT_MAKER", "0", "USDT", "SYC", "11", "WEB"]])
    table(wb, "OTC Payment ID History",
          ["User Id", "Payment ID", "Action", "Client", "Status", "Handler", "Update time", "Payment Method",
           "Payment Detail"],
          [[uid, "90000010", "ADD", "web", "Active", "90000011", "2023-08-01 00:00:00(UTC+0)", "SYNTH TRANSFER",
            "Name:SYNTH PERSON,Account:00000000000,"]])
    table(wb, "OTC Trading",
          ["OrderId", "UserId", "ChannelCode", "QuoteId", "PayType", "UserStatus", "UserCurrentPhase",
           "ChannelStatus", "ChannelCurrentPhase", "symbol", "BaseCoin", "QuoteCoin", "BaseCoinAmount",
           "QuoteCoinAmount", "USDT Equivalent", "SpreadAmount", "SpreadCoin", "UserQuotePrice", "UserSpreadPrice",
           "ChannelQuotePrice", "RequestAmount", "RequestAmountCoin", "TransId", "CreateTime", "UpdateTime",
           "UserCompletedTime", "ChannelCompletedTime", "UserRemark", "ChannelRemark"],
          [["9000000000000000001", uid, "SYNTHCH", "SYNTHQUOTE0001", "WALLET", "DONE", "FINAL_PHASE", "DONE_OK",
            "FINAL_OK", "SYCTST", "SYC", "TST", "0.1", "1.0", "1.1", "0", "TST", "10", "10", "10", "0.1", "SYC",
            "", "2023-09-01 00:00:00(UTC)", "2023-09-01 00:00:01(UTC)", "2023-09-01 00:00:01(UTC)",
            "2023-09-01 00:00:01(UTC)", "", ""]])
    table(wb, "Binance Card", ["UID"] + CARD_HDR,
          [[uid, "SYNTH-CARD-2", uid, "0000-SYNTH-0002", "VIRTUAL", "false", "false", "true", "ACTIVE",
            "2023-10-01 00:00:00"]])
    table(wb, "Binance Card transactions",
          ["UID", "Swipe Card ID", "Transaction ID", "Merchant Name", "Status", "Type", "Currency", "Channel",
           "Approved", "Total", "USDT equivalent", "Created date"],
          [[uid, "SYNTH-CARD-2", "SYNTH-CTX-2", "SYNTH SHOP", "APPROVED", "PURCHASE", "EUR", "POS", "true", "5",
            "5.5", "2023-10-02 00:00:00"]])
    table(wb, "Margin Order", ORDER24_HDR,
          [[uid, "SYCTST", "1", "1", "1", "0", "1", "2023-11-01 00:00:00", "2023-11-01 00:00:01", "BUY",
            "FILLED", "MARKET", "0", "TST", "SYC", "0.1", "APP"]])
    table(wb, "Gift Card Creation",
          ["minter_id", "card_no", "card_assets", "token", "card_status_text", "mint_time", "redeemer_id",
           "redeemed_time", "amt_usd", "asset_quantity"],
          [[uid, "SYNTH-GIFT-1", "TST", "SYNTHTOKEN", "Redeemed", "2023-12-01 00:00:00", "90000012",
            "2023-12-02 00:00:00", "5", "50"]])
    table(wb, "Gift Card Transfer",
          ["user_id", "card_no", "is_redeemed", "counterparty_user_id", "token", "card_redeem_time", "amt_usd",
           "asset_quantity"],
          [[uid, "SYNTH-GIFT-1", "true", "90000012", "SYNTHTOKEN", "2023-12-02 00:00:00", "5", "50"]])
    access(wb, uid, [["User login", "web", "2.0", "203.0.113.20", "Synthland", "SynthBrowser/2.0", "",
                      "2023-01-15 08:00:00"],
                     ["User login", "web", "2.0", "203.0.113.21", "Synthland", "SynthBrowser/2.0", "50000",
                      "2023-01-16 08:00:00"]])
    ws = wb["Access Logs"]
    ws.delete_rows(1, ws.max_row)
    put(ws, [["User ID", "Operation", "Client", "Client Version", "Real IP", "Geolocation", "Browser",
              "Port Number", "Timestamp (UTC)"],
             [uid, "User login", "web", "2.0", "203.0.113.20", "Synthland", "SynthBrowser/2.0", "",
              "2023-01-15 08:00:00"],
             [uid, "User login", "web", "2.0", "203.0.113.21", "Synthland", "SynthBrowser/2.0", "50000",
              "2023-01-16 08:00:00"]])
    devices(wb, DEVICE_HDR_EN + [None, None], [
        ["SYNTH-LAPTOP", "web", "203.0.113.20", "Synthland", "2023-01-16 08:00:00", "Normal", "fvideo_id",
         "SYNTHFV"],
        [None, None, None, None, None, None, "macintosh_uuid", "SYNTH-UUID-0001"],
    ])
    table(wb, "Loan Order",
          ["Seq", "Order ID", "User ID", "Confirmed Time[UTC]", "Collateral Level", "Loan Coin",
           "Left Repay Amount", "Init Loan Amount", "USDT equivalent", "Left Repay Interest", "Interest Accrual",
           "Daily Interest Rate", "Collateral Coin", "Initial Collateral Amount", "Remaining Collateral Amount",
           "Duration", "Deadline[UTC)", "ActualInterestDays", "OverdueDays", "Type", "Init Collateral Rate",
           "Margin Call Collateral Rate", "liquidation Collateral Rate", "Order Status", "Status Details",
           "Late Editor"],
          [["1", "SYNTH-LOAN-1", uid, "2023-12-10 00:00:00", "1", "TST", "0", "10", "1", "0", "0.01", "0.0001",
            "SYC", "1", "0", "7", "2023-12-17 00:00:00", "7", "0", "FLEXIBLE", "0.65", "0.8", "0.9", "Repaid",
            "", ""]])
    table(wb, "Repayment History",
          ["Seq", "UID", "Repaid Time[UTC + 8]", "Order ID", "Order Group Id", "Event No", "Coin", "Amount",
           "USDT equivalent", "Interest", "Principal", "Borrowed Time[UTC + 8]", "CollateralCoin",
           "Repay Collateral", "Loan / Collateral Price", "Released Collateral", "LTV after repayment",
           "Repay Type", "Status", "Staking Order"],
          [["1", uid, "2023-12-17 08:00:00", "SYNTH-LOAN-1", "SYNTH-GROUP-1", "SYNTH-EVENT-1", "TST", "10", "1",
            "0.01", "10", "2023-12-10 08:00:00", "SYC", "0", "10", "1", "0", "MANUAL", "SUCCESS", "false"]])
    table(wb, "Binance Send",
          ["Send number", "Payer ID", "Payer account type", "Payer nickname", "Payer phone area code",
           "Payer phone number", "Payer email", "Payer type", "Payee ID", "Payee account type", "Payee nickname",
           "Payee phone area code", "Payee phone number", "Payee email", "Amount", "Asset", "Assets BTC rate",
           "Send note", "Send type", "Send source", "Send status", "Send time", "Complete time", "Update time",
           "USDT equivalent"],
          [["SYNTH-SEND-2", uid, "SPOT", "synthnick", "+00", "0000000000", "synth.three@example.com", "USER",
            "90000013", "SPOT", "synthnick2", "+00", "0000000001", "synth.four@example.com", "2", "TST", "0.0001",
            "", "TRANSFER", "APP", "SUCCESS", "2024-01-01 00:00:00", "2024-01-01 00:00:05",
            "2024-01-01 00:00:05", "0.2"]])
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
    os.makedirs(os.path.join(BASE, "account_three"))
    workbook_18(os.path.join(BASE, "account_one", "SYNTH_binance_return_18_sheets.xlsx"))
    workbook_8(os.path.join(BASE, "account_two", "SYNTH_binance_return_8_sheets.xlsx"))
    workbook_2024(os.path.join(BASE, "account_three", "SYNTH_binance_return_2024_layout.xlsx"))
    decoy(os.path.join(BASE, "SYNTH_not_a_binance_return.xlsx"))
    print(f"Synthetic Binance return written to {BASE}")


if __name__ == "__main__":
    main()

"""
Binance law enforcement returns: one .xlsx workbook per account.

A workbook is recognised by its content, not its file name: it is read as a Binance return
when it holds both a 'Customer Information' and an 'Access Logs' sheet. The layouts handled
are the ones observed in three returns produced in 2022, one with 8 sheets and two with 18.
Every value in those workbooks was stored as text, numbers and dates included, and is
reported as text with leading and trailing spaces removed.

Most sheets are a plain table with a header row. Customer Information and Account Balance
are made of blocks (a one-cell title row, then a header row and records, or a
'Note: empty data' row). Approved Devices lists a device on one row and its Key/Value pairs
on that row and the rows under it. KYC Documents holds no cells, only embedded images.

Nothing in a recognised workbook is dropped: columns this module does not name go to
'Other Columns (as produced)', blocks it does not recognise to 'Account Balance - Other
Blocks', sheets it does not recognise to 'Other Sheets', and anything it could not place is
listed in 'Parsing Notes'.
"""

__artifacts_v2__ = {
    "binanceCustomerInfo": {
        "name": "Binance - Customer Information",
        "description": "Records from the Basic Information block of the Customer Information sheet, "
                       "with the sheet's heading line.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "Columns are named as the return names them. Heading (as produced) is the sheet's first "
                 "line; Heading ID, Heading Email and Heading Time (as produced) are the values that line "
                 "labels id, email and time, split from it as written. The module does not interpret the "
                 "heading time range. The return does not state a time zone for Registration time or the "
                 "other times in this block, so they are reported as produced and not converted. "
                 "In the observed returns the heading used an ASCII or a full-width opening parenthesis; "
                 "both are read. Mobile, User nationality, 2FA Opening time and SMS were empty in every observed "
                 "return; Heading ID and Heading Email matched User ID and Email.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "user",
    },
    "binanceApiInfo": {
        "name": "Binance - API Information",
        "description": "Records from the API Information block of the Customer Information sheet.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "The block held a header row and no records in every observed return, so this artifact "
                 "has only been exercised on synthetic data. Times carry no zone in the return and are "
                 "reported as produced.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "key",
    },
    "binanceBalanceSpot": {
        "name": "Binance - Account Balance - Spot",
        "description": "Records from Account Balance blocks with the Spot column layout.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "A block is assigned to this artifact by its header row, not its title; Block (as "
                 "produced) is the block's title row. Amounts are reported as the text the return holds. "
                 "The return does not say at what time the balances were taken. In the observed returns All "
                 "Positions equalled Available Positions on every row, and In Withdrawal and Pending Order held "
                 "one value throughout, as in the source.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "wallet",
    },
    "binanceBalanceFuturesPositions": {
        "name": "Binance - Account Balance - Futures Positions",
        "description": "Records from Account Balance blocks with the futures position column layout.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "Two blocks in the observed returns share this layout, titled 'Futures USDT position' and "
                 "'Futures 币本位 position'; Block (as produced) keeps the title untranslated. A block is "
                 "assigned by its header row. Amounts are reported as the text the return holds.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "trending-up",
    },
    "binanceBalanceFuturesBalances": {
        "name": "Binance - Account Balance - Futures Balances",
        "description": "Records from Account Balance blocks with the futures balance column layout.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "Two blocks in the observed returns share this layout, titled 'Futures USDT balance' and "
                 "'Futures 币本位 balance'; Block (as produced) keeps the title untranslated. A block is "
                 "assigned by its header row. Amounts are reported as the text the return holds.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "scale",
    },
    "binanceBalanceFuturesCollateral": {
        "name": "Binance - Account Balance - Futures Collateral",
        "description": "Records from Account Balance blocks with the futures collateral column layout.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "Columns are named as the return names them, lower-case asset and locked included. A block "
                 "is assigned by its header row. Amounts and rates are reported as the text the return "
                 "holds.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "lock",
    },
    "binanceBalanceMarginCross": {
        "name": "Binance - Account Balance - Margin Cross",
        "description": "Records from Account Balance blocks with the Margin - Cross column layout.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "A block is assigned by its header row. Amounts are reported as the text the return holds. "
                 "In the one observed return with records, Total Balance held a single space on every row and "
                 "is reported blank; Borrowed and Interest held one value throughout.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "stack-2",
    },
    "binanceBalanceMarginIsolated": {
        "name": "Binance - Account Balance - Margin Isolated",
        "description": "Records from Account Balance blocks with the Margin - Isolated column layout.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "A block is assigned by its header row. Amounts and ratios are reported as the text the "
                 "return holds. In the one observed return with records, Total Balance, Available Balance and "
                 "Borrowed held the same value on every row, as in the source.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "stack-2",
    },
    "binanceBalanceBlocks": {
        "name": "Binance - Account Balance - Block Index",
        "description": "One row per block of the Account Balance sheet: its title, its header, how many "
                       "records it held and which artifact reports them.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "Titles are kept as produced, untranslated. Note (as produced) is the text of a block that "
                 "holds a note instead of records, such as 'Note: empty data'. A block with no records "
                 "says only that the return listed none for it. Earn, Fiat and Pool blocks held only that "
                 "note in every observed return, so their column layout is unknown; when one holds "
                 "records they are reported under Account Balance - Other Blocks.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "list",
    },
    "binanceBalanceOther": {
        "name": "Binance - Account Balance - Other Blocks",
        "description": "Records from Account Balance blocks whose header this module does not recognise, "
                       "reported cell for cell under their own header.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "Record (as produced) is every non-empty cell of the row as 'header: value' pairs, named by "
                 "the block's own header row. No observed return had such a block, so this artifact has "
                 "only been exercised on synthetic data.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "layout-grid",
    },
    "binanceCurrentAssets": {
        "name": "Binance - Current Assets & Wallets",
        "description": "Records from the Current Assets & Wallets sheet.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "Columns are named as the return names them. Amounts are reported as the text the return "
                 "holds. Other Columns (as produced) is empty unless the sheet carries columns this "
                 "artifact does not name; such columns are kept there as JSON.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "wallet",
    },
    "binanceDeposits": {
        "name": "Binance - Deposit History",
        "description": "Records from the Deposit History sheet.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "Columns are named as the return names them. The return does not state a time zone for "
                 "Create Time, so it is reported as produced and not converted. Other Columns (as "
                 "produced) is empty unless the sheet carries columns this artifact does not name.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "download",
    },
    "binanceWithdrawals": {
        "name": "Binance - Withdrawal History",
        "description": "Records from the Withdrawal History sheet.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "Columns are named as the return names them; a header with a trailing space ('Destination "
                 "Address ', seen in two observed returns) is read the same as one without. The return "
                 "does not state a time zone for Apply Time, so it is reported as produced and not "
                 "converted. Label/Tag/Memo was empty on every row of the observed returns.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "upload",
    },
    "binanceOrders": {
        "name": "Binance - Order History",
        "description": "Records from the Order History sheet.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "Columns are named as the return names them. The return does not state a time zone for Time "
                 "or Update Time, so they are reported as produced and not converted. The sheet was absent "
                 "from one observed return. In the one observed return with records, Type held a single space "
                 "on every row and is reported blank.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "shopping-cart",
    },
    "binanceFiatDeposits": {
        "name": "Binance - Fiat Deposit History",
        "description": "Records from the Fiat Deposit History sheet.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "The sheet held a header row and no records in every observed return, so this artifact has "
                 "only been exercised on synthetic data. Times carry no zone in the return and are reported "
                 "as produced.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "download",
    },
    "binanceFiatWithdrawals": {
        "name": "Binance - Fiat Withdrawal History",
        "description": "Records from the Fiat Withdrawal History sheet.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "The sheet held a header row and no records in every observed return, so this artifact has "
                 "only been exercised on synthetic data. Times carry no zone in the return and are reported "
                 "as produced.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "upload",
    },
    "binanceAccessLogs": {
        "name": "Binance - Access Logs",
        "description": "Records from the Access Logs sheet.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "Timestamp (UTC) is converted from the column the return labels 'Timestamp (UTC)'; it is "
                 "blank when the value is not in the form YYYY-MM-DD HH:MM:SS, and Timestamp (as produced) "
                 "holds the value as written on every row. Operation, Geolocation and the other columns are "
                 "reported as produced.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "login",
    },
    "binanceDevices": {
        "name": "Binance - Approved Devices",
        "description": "One row per device listed on the Approved Devices sheet.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "A device starts on a row with any of the device columns filled; the Key/Value pairs on that "
                 "row and on the rows below it, up to the next device, are listed under Approved Devices - "
                 "Attributes with the same Device Number. In some observed returns each header also "
                 "carried a Chinese label after the English one; columns are matched on the English words. "
                 "Recent Usage Timestamp (UTC) is converted from the column the return labels UTC and is "
                 "blank when the value is not in the form YYYY-MM-DD HH:MM:SS.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "device-mobile",
    },
    "binanceDeviceAttributes": {
        "name": "Binance - Approved Devices - Attributes",
        "description": "Key/Value pairs listed for each device on the Approved Devices sheet.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "Keys and values are reported as produced; the module does not interpret any key. The set "
                 "of keys differed between devices in the observed returns. A pair found above the first "
                 "device is kept with a blank Device Number and listed in Parsing Notes.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "list-details",
    },
    "binanceOtcPayment": {
        "name": "Binance - OTC Payment",
        "description": "Records from the OTC Payment sheet.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "The sheet held a header row and no records in every observed return in which it appeared, "
                 "so this artifact has only been exercised on synthetic data.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "credit-card",
    },
    "binanceFundingWallet": {
        "name": "Binance - Funding Wallet",
        "description": "Records from the Funding Wallet sheet.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "The sheet held a header row and no records in every observed return in which it appeared, "
                 "so this artifact has only been exercised on synthetic data.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "wallet",
    },
    "binanceSend": {
        "name": "Binance - Binance Send",
        "description": "Records from the Binance Send sheet.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "The sheet held a header row and no records in every observed return in which it appeared, "
                 "so this artifact has only been exercised on synthetic data. Times carry no zone in the "
                 "return and are reported as produced.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "send",
    },
    "binancePay": {
        "name": "Binance - Binance Pay",
        "description": "Records from the Binance Pay sheet.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "The sheet held a header row and no records in every observed return in which it appeared, "
                 "so this artifact has only been exercised on synthetic data. Times carry no zone in the "
                 "return and are reported as produced.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "cash",
    },
    "binanceOtcTrading": {
        "name": "Binance - OTC Trading",
        "description": "Records from the OTC Trading sheet.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "The sheet held a header row and no records in every observed return in which it appeared, "
                 "so this artifact has only been exercised on synthetic data. Times carry no zone in the "
                 "return and are reported as produced.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "arrows-exchange",
    },
    "binanceCards": {
        "name": "Binance - Binance Card",
        "description": "Records from the Binance Card sheet.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "The sheet held a header row and no records in every observed return in which it appeared, "
                 "so this artifact has only been exercised on synthetic data.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "credit-card",
    },
    "binanceCardTransactions": {
        "name": "Binance - Binance Card Transactions",
        "description": "Records from the Binance Card transaction history sheet.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "In the observed returns the sheet was named 'Binance Card transaction histor', cut at "
                 "Excel's 31-character limit; any sheet whose name starts with 'Binance Card transaction' "
                 "is read. It held a header row and no records in every observed return in which it "
                 "appeared, so this artifact has only been exercised on synthetic data.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "receipt",
    },
    "binanceEmbeddedImages": {
        "name": "Binance - Embedded Images",
        "description": "Images embedded in the workbook, with the sheet and cell each is anchored on.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "Images are read from the workbook's own drawing parts, not from the sheet's cells. In every "
                 "observed return they were JPEG images anchored on the KYC Documents sheet, which held no "
                 "cells. The module does not say what an image shows. An image stored in the workbook but "
                 "not anchored on any sheet is reported with a blank Sheet.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "photo",
    },
    "binanceOtherSheets": {
        "name": "Binance - Other Sheets",
        "description": "Rows of sheets this module does not recognise, reported cell for cell.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "Cells (as produced) is every non-empty cell of the row as 'column letter: value' pairs, "
                 "because the module does not know which row of an unknown sheet is its header. No "
                 "observed return had such a sheet.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "table",
    },
    "binanceParsingNotes": {
        "name": "Binance - Parsing Notes",
        "description": "What the module could not read or place, per workbook.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-09",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "notes": "Lists every .xlsx matched that was not read as a Binance return and why, workbooks that "
                 "could not be opened, the sheets of each recognised workbook, and any row the module "
                 "could not place. Review the source workbook for each note.",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "alert-triangle",
    },
}

import functools
import json
import os
import posixpath
import re
import zipfile
from xml.etree import ElementTree

from scripts.ilapfuncs import artifact_processor, check_in_embedded_media, convert_ts_human_to_utc, logfunc

import openpyxl
from openpyxl.utils.exceptions import InvalidFileException

_REQUIRED_SHEETS = ("Customer Information", "Access Logs")
_CARD_TX_PREFIX = "Binance Card transaction"

# Plain table sheets: sheet name -> columns as the return names them.
_TABLE_SHEETS = {
    "Current Assets & Wallets": (
        "Asset Ticker", "Asset Name", "Total Position", "Estimated BTC Value", "Deposit Wallet Address",
        "Label/Tag/Memo"),
    "Deposit History": (
        "Create Time", "User ID", "Currency", "Amount", "BUSD", "Deposit Address", "Source Address", "TXID",
        "Status", "Network", "CounterParty ID"),
    "Withdrawal History": (
        "Apply Time", "User ID", "Currency", "Amount", "BUSD", "Destination Address", "Label/Tag/Memo",
        "txId", "Status", "Network", "CounterParty ID"),
    "Order History": (
        "Time", "Update Time", "User ID", "Market ID", "Side", "Type", "Status", "Price", "Qty",
        "Average Price", "Remain Qty", "Trade Qty", "Stop Price", "Price Unit", "Amount Unit"),
    "Fiat Deposit History": (
        "Create Time", "Completed Time", "Arrived Time", "Update Time", "Status", "UserID", "Email", "Amount",
        "Currency", "Internal Serial Number", "External Serial Number", "Second External Serial Number",
        "Source Account Id", "Source Account Name", "Source Account", "Golden Channel", "Remark",
        "Is Replacement Order?", "Abnormal Reason", "Error Code", "Error Reason", "Channel Fee",
        "Platform Fee", "Network Provider", "Expect Recharge Amount", "Narrative", "Order Type"),
    "Fiat Withdrawal History": (
        "Create Time", "Completed Time", "Arrived Time", "Update Time", "Status", "UserID", "Email", "Amount",
        "Currency", "Internal Serial Number", "External Serial Number", "Target Account Id", "Target Name",
        "Target Account", "Withdraw Channel", "Remark", "Is Replacement Order?", "Abnormal Reason",
        "Error Reason", "Channel Fee", "Platform Fee", "Network Provider", "Withdrawer", "Narrative", "Bic",
        "Bank", "Country", "Sortcode", "Bank Address", "Bank City", "Iban", "Flutterwave Proof"),
    "Access Logs": (
        "Timestamp (UTC)", "User ID", "Operation", "Client", "Client Version", "Real IP", "Geolocation",
        "Browser"),
    "OTC Payment": (
        "User ID", "Receiving Payment ID", "Name", "Payment method", "Bank account number", "Bank name",
        "Account opening branch"),
    "Funding Wallet": (
        "User ID", "TotalAsset", "TotalAsset BUSD", "AssetCode", "AssetName", "Freeze", "Withdrawing", "Free",
        "Locked"),
    "Binance Send": (
        "Send time", "Complete time", "Update time", "Send number", "Payer account type", "Payer type",
        "Payee account type", "Amount", "Asset", "Assets BTC rate", "Send note", "Send type", "Send source",
        "Send status"),
    "Binance Pay": (
        "Transaction Time", "User ID", "Merchant Name", "Transaction Type", "Currency", "Amount"),
    "OTC Trading": (
        "CreateTime", "UpdateTime", "UserCompletedTime", "ChannelCompletedTime", "OrderId", "UserId",
        "ChannelCode", "QuoteId", "PayType", "UserStatus", "UserCurrentPhase", "ChannelStatus",
        "ChannelCurrentPhase", "symbol", "BaseCoin", "QuoteCoin", "BaseCoinAmount", "QuoteCoinAmount",
        "SpreadAmount", "SpreadCoin", "UserQuotePrice", "UserSpreadPrice", "ChannelQuotePrice",
        "RequestAmount", "RequestAmountCoin", "TransId", "OtcUserId", "SpreadUserId", "ChannelUserId",
        "UserRemark", "ChannelRemark"),
    "Binance Card": (
        "Create Date", "Swipe Card ID", "Swipe User ID", "Card Number", "Card Type", "Locked", "Freeze",
        "Activated", "Card Status"),
    _CARD_TX_PREFIX: (
        "Created date", "Swipe Card ID", "Transaction ID", "Merchant Name", "Status", "Type", "Currency",
        "Channel", "Approved", "Total"),
}

# Columns the return labels UTC: reported converted and as produced.
_UTC_COLUMNS = ("Timestamp (UTC)", "Recent Usage Timestamp (UTC)")

# Account Balance block layouts, matched on the header row. The key is the artifact.
_BALANCE_LAYOUTS = {
    "binanceBalanceSpot": (
        "Currency Name", "Currency Code", "All Positions", "Available Positions", "In Withdrawal",
        "Pending Order", "BTC Equivalent"),
    "binanceBalanceFuturesPositions": (
        "Symbol", "Position Amount", "Entry Price", "Mark Price", "Unrealized Profit"),
    "binanceBalanceFuturesBalances": (
        "Asset", "Wallet Balance", "Unrealized Profit", "Available For Order"),
    "binanceBalanceFuturesCollateral": (
        "asset", "locked", "Loan Amount(USDT)", "Total Principal For Interest(USDT)", "Current Rate",
        "Initial Rate", "Liquidation Collateral Rate", "Liquidation Price", "Total Interest(USDT)"),
    "binanceBalanceMarginCross": (
        "Currency", "Total Balance", "Available Balance", "Borrowed", "Interest"),
    "binanceBalanceMarginIsolated": (
        "Trading Pair", "Risk Ratio", "Effective Multiple", "Currency", "Total Balance", "Available Balance",
        "Borrowed"),
}

_CUSTOMER_COLUMNS = (
    "Registration time", "User ID", "Email", "Mobile", "Name", "User nationality", "User ID number",
    "User authentication type", "User authentication time", "Status", "2FA", "2FA Opening time", "SMS",
    "SMS Opening time", "2FA Reset Information")
_API_COLUMNS = ("Create Time", "Update Time", "Rule ID", "API Name", "Trade IP", "Withdraw IP")
_DEVICE_COLUMNS = ("Device Name", "Client", "IP Address", "Geolocation", "Recent Usage Timestamp (UTC)",
                   "Status")

_KNOWN_SHEETS = set(_TABLE_SHEETS) | {"Customer Information", "Account Balance", "Approved Devices",
                                      "KYC Documents"}

_HEADING = re.compile(r"^User Basic Information\s*[(（]\s*id:\s*(?P<id>\S*)\s+email:\s*(?P<email>\S*)"
                      r"\s+time:\s*(?P<time>.*?)\s*[)）]?\s*$", re.DOTALL)
_UTC_FORM = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")

_NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "xdr": "http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}
_R_ID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
_R_EMBED = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"
_IMAGE_MAGIC = ((b"\xff\xd8\xff", "JPEG", "jpg"), (b"\x89PNG\r\n\x1a\n", "PNG", "png"),
                (b"GIF8", "GIF", "gif"), (b"BM", "BMP", "bmp"))

# ElementTree.ParseError subclasses SyntaxError; naming the base keeps pylint's inference sound.
_READ_ERRORS = (OSError, zipfile.BadZipFile, KeyError, ValueError, InvalidFileException, SyntaxError)


# ------------------------------------------------------------------ cell and header helpers
def _cell(value):
    if value is None:
        return ""
    return str(value).strip()


def _header(value):
    """The English words of a header; some returns follow them with a Chinese label."""
    words = []
    for word in _cell(value).split():
        if any(ord(ch) > 127 for ch in word):
            break
        words.append(word)
    return " ".join(words)


def _column_letter(index):
    letters = ""
    index += 1
    while index:
        index, rem = divmod(index - 1, 26)
        letters = chr(65 + rem) + letters
    return letters


def _utc(value):
    """A value the return labels UTC, as an aware datetime; None when not YYYY-MM-DD HH:MM:SS."""
    if not _UTC_FORM.match(value):
        return None
    try:
        return convert_ts_human_to_utc(value)
    except ValueError:
        return None


def _blank(cells):
    return not any(cells)


def _at(cells, index):
    return cells[index] if index is not None and index < len(cells) else ""


def _record(header, cells):
    return {name: cells[i] if i < len(cells) else "" for i, name in enumerate(header) if name}


def _extra(header, cells, known):
    extra = {}
    for i, value in enumerate(cells):
        name = header[i] if i < len(header) and header[i] else f"(column {_column_letter(i)})"
        if name not in known and value:
            extra[name] = value
    return json.dumps(extra, ensure_ascii=False) if extra else ""


def _pairs(header, cells):
    out = []
    for i, value in enumerate(cells):
        if value:
            name = header[i] if i < len(header) and header[i] else f"(column {_column_letter(i)})"
            out.append(f"{name}: {value}")
    return "; ".join(out)


# ------------------------------------------------------------------ workbook reading
@functools.lru_cache(maxsize=16)
def _load(path, _stamp):
    """(sheets, note): sheets maps name -> list of row tuples, or None when not a Binance return."""
    workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
    try:
        names = list(workbook.sheetnames)
        missing = [name for name in _REQUIRED_SHEETS if name not in names]
        if missing:
            return None, "not read as a Binance return: no sheet named " + " or ".join(
                f"'{name}'" for name in missing)
        sheets = {}
        for sheet in workbook.worksheets:
            sheets[sheet.title] = [tuple(_cell(c) for c in row) for row in sheet.iter_rows(values_only=True)]
        return sheets, ""
    finally:
        workbook.close()


def _workbooks(context, notes=None):
    """(source path, sheets) for every matched file that is a Binance return."""
    out = []
    for file_found in sorted({str(f) for f in context.get_files_found()}):
        if not file_found.lower().endswith(".xlsx") or os.path.basename(file_found).startswith("~$"):
            continue
        try:
            stat = os.stat(file_found)
            sheets, note = _load(file_found, (stat.st_mtime_ns, stat.st_size))
        except _READ_ERRORS as err:
            sheets, note = None, f"could not be opened as a workbook ({type(err).__name__})"
        if sheets is None:
            if notes is not None:
                notes.append((file_found, "", "", note))
            continue
        out.append((file_found, sheets))
    return out


def _sheet(sheets, name):
    if name == _CARD_TX_PREFIX:
        for title, rows in sheets.items():
            if title.startswith(_CARD_TX_PREFIX):
                return title, rows
        return None, None
    return (name, sheets[name]) if name in sheets else (None, None)


def _blocks(rows):
    """Split a block sheet into {'title', 'row', 'header', 'records', 'note'} dicts.

    A title is a row with one non-empty cell, in column A, that is the first row of the
    sheet or follows an empty row, and whose next non-empty row is a note or has more than
    one cell. Rows before the first title are returned as the preamble.
    """
    blocks, preamble, current = [], [], None
    for index, cells in enumerate(rows):
        number = index + 1
        if _blank(cells):
            continue
        filled = [c for c in cells if c]
        previous_blank = index == 0 or _blank(rows[index - 1])
        if len(filled) == 1 and cells[0] and previous_blank:
            following = next((r for r in rows[index + 1:] if not _blank(r)), None)
            if following is not None and (following[0].startswith("Note:")
                                          or len([c for c in following if c]) > 1):
                current = {"title": cells[0], "row": number, "header": None, "header_raw": None,
                           "records": [], "note": ""}
                blocks.append(current)
                continue
        if current is None:
            preamble.append((number, cells))
        elif current["header"] is None and not current["records"] and len(filled) == 1 \
                and cells[0].startswith("Note:"):
            current["note"] = cells[0]
        elif current["header"] is None:
            current["header_raw"] = cells
            current["header"] = [_header(c) for c in cells]
        else:
            current["records"].append((number, cells))
    return preamble, blocks


def _layout_for(header):
    names = set(header or ())
    for artifact, columns in _BALANCE_LAYOUTS.items():
        if set(columns) <= names:
            return artifact
    return None


# ------------------------------------------------------------------ artifact builders
def _table_artifact(context, sheet_name):
    known = _TABLE_SHEETS[sheet_name]
    headers = []
    for column in known:
        if column in _UTC_COLUMNS:
            headers += [(column, "datetime"), column.replace("(UTC)", "(as produced)")]
        else:
            headers.append(column)
    headers += ["Other Columns (as produced)", "Sheet Row", "Source File"]
    rows, sources = [], set()
    for source, sheets in _workbooks(context):
        _title, sheet_rows = _sheet(sheets, sheet_name)
        if sheet_rows is None:
            continue
        sources.add(source)
        header_index = next((i for i, r in enumerate(sheet_rows) if not _blank(r)), None)
        if header_index is None:
            continue
        header = [_header(c) for c in sheet_rows[header_index]]
        for index in range(header_index + 1, len(sheet_rows)):
            cells = sheet_rows[index]
            if _blank(cells):
                continue
            record = _record(header, cells)
            line = []
            for column in known:
                value = record.get(column, "")
                if column in _UTC_COLUMNS:
                    line += [_utc(value), value]
                else:
                    line.append(value)
            line += [_extra(header, cells, known), index + 1, context.get_relative_path(source)]
            rows.append(tuple(line))
    return tuple(headers), rows, "\n".join(sorted(sources))


def _customer_blocks(sheets):
    rows = sheets.get("Customer Information", [])
    preamble, blocks = _blocks(rows)
    heading = next((cells[0] for _n, cells in preamble if cells[0].startswith("User Basic Information")), "")
    return heading, preamble, blocks


def _block_artifact(context, title, known):
    headers = list(known) + ["Other Columns (as produced)", "Sheet Row", "Source File"]
    if title == "Basic Information":
        headers = ["Heading (as produced)", "Heading ID", "Heading Email", "Heading Time (as produced)"] + headers
    rows, sources = [], set()
    for source, sheets in _workbooks(context):
        heading, _preamble, blocks = _customer_blocks(sheets)
        sources.add(source)
        match = _HEADING.match(heading)
        parsed = [match.group("id"), match.group("email"), match.group("time")] if match else ["", "", ""]
        for block in blocks:
            if block["title"] != title or not block["header"]:
                continue
            for number, cells in block["records"]:
                record = _record(block["header"], cells)
                line = [heading] + parsed if title == "Basic Information" else []
                line += [record.get(c, "") for c in known]
                line += [_extra(block["header"], cells, known), number, context.get_relative_path(source)]
                rows.append(tuple(line))
    return tuple(headers), rows, "\n".join(sorted(sources))


def _balance_artifact(context, artifact):
    known = _BALANCE_LAYOUTS[artifact]
    headers = ["Block (as produced)"] + list(known) + ["Other Columns (as produced)", "Sheet Row",
                                                        "Source File"]
    rows, sources = [], set()
    for source, sheets in _workbooks(context):
        if "Account Balance" not in sheets:
            continue
        sources.add(source)
        _preamble, blocks = _blocks(sheets["Account Balance"])
        for block in blocks:
            if _layout_for(block["header"]) != artifact:
                continue
            for number, cells in block["records"]:
                record = _record(block["header"], cells)
                rows.append(tuple([block["title"]] + [record.get(c, "") for c in known]
                                  + [_extra(block["header"], cells, known), number,
                                     context.get_relative_path(source)]))
    return tuple(headers), rows, "\n".join(sorted(sources))


def _device_rows(sheet_rows):
    """(devices, attributes, orphans) from the Approved Devices sheet."""
    header_index = next((i for i, r in enumerate(sheet_rows) if not _blank(r)), None)
    if header_index is None:
        return [], [], []
    header = [_header(c) for c in sheet_rows[header_index]]
    key_col = header.index("Key") if "Key" in header else None
    value_col = header.index("Value") if "Value" in header else None
    device_cols = [i for i in range(len(header)) if i not in (key_col, value_col)]
    devices, attributes, orphans = [], [], []
    for index in range(header_index + 1, len(sheet_rows)):
        cells = sheet_rows[index]
        if _blank(cells):
            continue
        number = index + 1
        if any(_at(cells, i) for i in device_cols):
            record = _record(header, cells)
            devices.append({"number": len(devices) + 1, "record": record, "row": number,
                            "extra": _extra(header, cells, set(_DEVICE_COLUMNS) | {"Key", "Value"}),
                            "pairs": 0})
        key, value = _at(cells, key_col), _at(cells, value_col)
        if key or value:
            if devices:
                devices[-1]["pairs"] += 1
                attributes.append((devices[-1], key, value, number))
            else:
                attributes.append((None, key, value, number))
                orphans.append(number)
    return devices, attributes, orphans


def _embedded_images(path):
    """[(sheet or '', member, anchor cell, order)] for every image part in the workbook."""
    found, anchored = [], set()
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())

        def rels(part):
            folder, base = posixpath.split(part)
            rel_part = posixpath.join(folder, "_rels", base + ".rels")
            if rel_part not in names:
                return {}
            root = ElementTree.fromstring(archive.read(rel_part))
            out = {}
            for rel in root.findall("rel:Relationship", _NS):
                target = rel.get("Target", "")
                # A target is relative to the part's folder, or absolute from the package root.
                resolved = target.lstrip("/") if target.startswith("/") else posixpath.join(folder, target)
                out[rel.get("Id")] = posixpath.normpath(resolved)
            return out

        workbook_rels = rels("xl/workbook.xml")
        workbook = ElementTree.fromstring(archive.read("xl/workbook.xml"))
        for sheet in workbook.findall("main:sheets/main:sheet", _NS):
            sheet_part = workbook_rels.get(sheet.get(_R_ID))
            if not sheet_part or sheet_part not in names:
                continue
            sheet_root = ElementTree.fromstring(archive.read(sheet_part))
            sheet_rels = rels(sheet_part)
            for drawing in sheet_root.findall("main:drawing", _NS):
                drawing_part = sheet_rels.get(drawing.get(_R_ID))
                if not drawing_part or drawing_part not in names:
                    continue
                drawing_rels = rels(drawing_part)
                drawing_root = ElementTree.fromstring(archive.read(drawing_part))
                order = 0
                for anchor in list(drawing_root):
                    blip = anchor.find(".//a:blip", _NS)
                    if blip is None:
                        continue
                    member = drawing_rels.get(blip.get(_R_EMBED))
                    if not member or member not in names:
                        continue
                    order += 1
                    start = anchor.find("xdr:from", _NS)
                    cell = ""
                    if start is not None:
                        col, row = start.findtext("xdr:col", "", _NS), start.findtext("xdr:row", "", _NS)
                        if col.isdigit() and row.isdigit():
                            cell = f"{_column_letter(int(col))}{int(row) + 1}"
                    found.append((sheet.get("name", ""), member, cell, order))
                    anchored.add(member)
        for member in sorted(n for n in names if n.startswith("xl/media/") and n not in anchored):
            found.append(("", member, "", ""))
        data = {member: archive.read(member) for _s, member, _c, _o in found}
    return found, data


def _image_type(data):
    """(type name, extension) sniffed from the bytes; the member's own extension is not trusted."""
    for magic, name, extension in _IMAGE_MAGIC:
        if data.startswith(magic):
            return name, extension
    return "unrecognised", None


# ------------------------------------------------------------------ artifacts
@artifact_processor
def binanceCustomerInfo(context):
    return _block_artifact(context, "Basic Information", _CUSTOMER_COLUMNS)


@artifact_processor
def binanceApiInfo(context):
    return _block_artifact(context, "API Information", _API_COLUMNS)


@artifact_processor
def binanceBalanceSpot(context):
    return _balance_artifact(context, "binanceBalanceSpot")


@artifact_processor
def binanceBalanceFuturesPositions(context):
    return _balance_artifact(context, "binanceBalanceFuturesPositions")


@artifact_processor
def binanceBalanceFuturesBalances(context):
    return _balance_artifact(context, "binanceBalanceFuturesBalances")


@artifact_processor
def binanceBalanceFuturesCollateral(context):
    return _balance_artifact(context, "binanceBalanceFuturesCollateral")


@artifact_processor
def binanceBalanceMarginCross(context):
    return _balance_artifact(context, "binanceBalanceMarginCross")


@artifact_processor
def binanceBalanceMarginIsolated(context):
    return _balance_artifact(context, "binanceBalanceMarginIsolated")


@artifact_processor
def binanceBalanceBlocks(context):
    names = {artifact: __artifacts_v2__[artifact]["name"] for artifact in _BALANCE_LAYOUTS}
    headers = ("Block (as produced)", "Header (as produced)", "Records", "Note (as produced)",
               "Reported In", "Sheet Row", "Source File")
    rows, sources = [], set()
    for source, sheets in _workbooks(context):
        if "Account Balance" not in sheets:
            continue
        sources.add(source)
        _preamble, blocks = _blocks(sheets["Account Balance"])
        for block in blocks:
            layout = _layout_for(block["header"])
            if layout:
                reported = names[layout]
            elif block["records"]:
                reported = __artifacts_v2__["binanceBalanceOther"]["name"]
            else:
                reported = ""
            header = "; ".join(c for c in (block["header_raw"] or ()) if c)
            rows.append((block["title"], header, len(block["records"]), block["note"], reported,
                         block["row"], context.get_relative_path(source)))
    return headers, rows, "\n".join(sorted(sources))


@artifact_processor
def binanceBalanceOther(context):
    headers = ("Block (as produced)", "Record (as produced)", "Sheet Row", "Source File")
    rows, sources = [], set()
    for source, sheets in _workbooks(context):
        if "Account Balance" not in sheets:
            continue
        sources.add(source)
        _preamble, blocks = _blocks(sheets["Account Balance"])
        for block in blocks:
            if _layout_for(block["header"]):
                continue
            for number, cells in block["records"]:
                rows.append((block["title"], _pairs(block["header"] or [], cells), number,
                             context.get_relative_path(source)))
    return headers, rows, "\n".join(sorted(sources))


@artifact_processor
def binanceCurrentAssets(context):
    return _table_artifact(context, "Current Assets & Wallets")


@artifact_processor
def binanceDeposits(context):
    return _table_artifact(context, "Deposit History")


@artifact_processor
def binanceWithdrawals(context):
    return _table_artifact(context, "Withdrawal History")


@artifact_processor
def binanceOrders(context):
    return _table_artifact(context, "Order History")


@artifact_processor
def binanceFiatDeposits(context):
    return _table_artifact(context, "Fiat Deposit History")


@artifact_processor
def binanceFiatWithdrawals(context):
    return _table_artifact(context, "Fiat Withdrawal History")


@artifact_processor
def binanceAccessLogs(context):
    return _table_artifact(context, "Access Logs")


@artifact_processor
def binanceOtcPayment(context):
    return _table_artifact(context, "OTC Payment")


@artifact_processor
def binanceFundingWallet(context):
    return _table_artifact(context, "Funding Wallet")


@artifact_processor
def binanceSend(context):
    return _table_artifact(context, "Binance Send")


@artifact_processor
def binancePay(context):
    return _table_artifact(context, "Binance Pay")


@artifact_processor
def binanceOtcTrading(context):
    return _table_artifact(context, "OTC Trading")


@artifact_processor
def binanceCards(context):
    return _table_artifact(context, "Binance Card")


@artifact_processor
def binanceCardTransactions(context):
    return _table_artifact(context, _CARD_TX_PREFIX)


@artifact_processor
def binanceDevices(context):
    headers = (("Recent Usage Timestamp (UTC)", "datetime"), "Recent Usage Timestamp (as produced)",
               "Device Number", "Device Name", "Client", "IP Address", "Geolocation", "Status",
               "Attribute Pairs", "Other Columns (as produced)", "Sheet Row", "Source File")
    rows, sources = [], set()
    for source, sheets in _workbooks(context):
        if "Approved Devices" not in sheets:
            continue
        sources.add(source)
        devices, _attributes, _orphans = _device_rows(sheets["Approved Devices"])
        for device in devices:
            record = device["record"]
            stamp = record.get("Recent Usage Timestamp (UTC)", "")
            rows.append((_utc(stamp), stamp, device["number"], record.get("Device Name", ""),
                         record.get("Client", ""), record.get("IP Address", ""), record.get("Geolocation", ""),
                         record.get("Status", ""), device["pairs"], device["extra"], device["row"],
                         context.get_relative_path(source)))
    return headers, rows, "\n".join(sorted(sources))


@artifact_processor
def binanceDeviceAttributes(context):
    headers = ("Device Number", "Device Name", "Key", "Value", "Sheet Row", "Source File")
    rows, sources = [], set()
    for source, sheets in _workbooks(context):
        if "Approved Devices" not in sheets:
            continue
        sources.add(source)
        _devices, attributes, _orphans = _device_rows(sheets["Approved Devices"])
        for device, key, value, number in attributes:
            rows.append((device["number"] if device else "", device["record"].get("Device Name", "") if device
                         else "", key, value, number, context.get_relative_path(source)))
    return headers, rows, "\n".join(sorted(sources))


@artifact_processor
def binanceEmbeddedImages(context):
    headers = ("Sheet", "Anchor Cell", "Order on Sheet", ("Image", "media"), "Workbook Member",
               "Detected Type", "Size (bytes)", "Source File")
    rows, sources = [], set()
    for source, _sheets in _workbooks(context):
        try:
            found, data = _embedded_images(source)
        except _READ_ERRORS as err:
            logfunc(f"Binance returns: images of {os.path.basename(source)} not read: {type(err).__name__}")
            continue
        sources.add(source)
        for sheet, member, cell, order in found:
            blob = data.get(member, b"")
            name = posixpath.basename(member)
            kind, extension = _image_type(blob)
            ref = check_in_embedded_media(source, blob, name, force_extension=extension)
            rows.append((sheet, cell, order, ref, member, kind, len(blob),
                         context.get_relative_path(source)))
    return headers, rows, "\n".join(sorted(sources))


@artifact_processor
def binanceOtherSheets(context):
    headers = ("Sheet", "Sheet Row", "Cells (as produced)", "Source File")
    rows, sources = [], set()
    for source, sheets in _workbooks(context):
        sources.add(source)
        for title, sheet_rows in sheets.items():
            if title in _KNOWN_SHEETS or title.startswith(_CARD_TX_PREFIX):
                continue
            for index, cells in enumerate(sheet_rows):
                if not _blank(cells):
                    letters = [_column_letter(i) for i in range(len(cells))]
                    rows.append((title, index + 1, _pairs(letters, cells), context.get_relative_path(source)))
    return headers, rows, "\n".join(sorted(sources))


@artifact_processor
def binanceParsingNotes(context):
    headers = ("Sheet", "Sheet Row", "Note", "Source File")
    notes = []
    workbooks = _workbooks(context, notes)
    for source, sheets in workbooks:
        titles = list(sheets)
        notes.append((source, "", "", f"read as a Binance return; {len(titles)} sheets: " + "; ".join(titles)))
        unknown = [t for t in titles if t not in _KNOWN_SHEETS and not t.startswith(_CARD_TX_PREFIX)]
        if unknown:
            notes.append((source, "", "", "sheets not recognised, reported under Other Sheets: "
                          + "; ".join(unknown)))
        heading, preamble, blocks = _customer_blocks(sheets)
        if "Customer Information" in sheets and not _HEADING.match(heading):
            notes.append((source, "Customer Information", "",
                          "heading line not found or not in the expected form; Heading ID, Heading Email "
                          "and Heading Time are blank"))
        for number, cells in preamble:
            if not cells[0].startswith("User Basic Information"):
                notes.append((source, "Customer Information", number,
                              "row before the first block not placed: " + _pairs([], cells)))
        for block in blocks:
            if block["title"] not in ("Basic Information", "API Information"):
                notes.append((source, "Customer Information", block["row"],
                              f"block '{block['title']}' not recognised; its rows are not reported"))
        if "Account Balance" in sheets:
            preamble, _blocks_found = _blocks(sheets["Account Balance"])
            for number, cells in preamble:
                notes.append((source, "Account Balance", number,
                              "row before the first block not placed: " + _pairs([], cells)))
        if "Approved Devices" in sheets:
            _devices, _attributes, orphans = _device_rows(sheets["Approved Devices"])
            for number in orphans:
                notes.append((source, "Approved Devices", number,
                              "Key/Value pair above the first device; reported with a blank Device Number"))
    rows = [(sheet, number, note, context.get_relative_path(source)) for source, sheet, number, note in notes]
    sources = sorted({source for source, _s, _n, _t in notes})
    return headers, rows, "\n".join(sources)

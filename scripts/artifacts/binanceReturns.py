"""
Binance law enforcement returns: one .xlsx workbook per account.

A workbook is recognised by its content, not its file name: it is read as a Binance return
when it holds both a 'Customer Information' and an 'Access Logs' sheet. Two layouts have been
observed. Returns produced in 2022 had 8 or 18 sheets, with balances on an 'Account Balance'
sheet. A return produced in 2024 had 30 sheets: balances on an 'Assets Overview' sheet,
asset logs, P2P, loans and gift cards, new blocks in Customer Information, and extra
columns on sheets the 2022 layout already had. Every value in those workbooks was stored as
text, numbers and dates included, and is reported as text with leading and trailing spaces
removed.

Most sheets are a plain table with a header row. Customer Information, Account Balance and
Assets Overview are made of blocks (a one-cell title row, then a header row and records, or
a 'Note: empty data' row). Approved Devices lists a device on one row and its Key/Value
pairs on that row and the rows under it. KYC Documents holds no cells, only embedded images.

Nothing in a recognised workbook is dropped: columns this module does not name go to
'Other Columns (as produced)', blocks it does not recognise to the 'Other Blocks' artifacts,
sheets it does not recognise, or whose header matches no known layout, to 'Other Sheets',
and every such placement is listed in 'Parsing Notes'.
"""

__artifacts_v2__ = {
    "binanceCustomerInfo": {
        "name": "Binance - Customer Information",
        "description": "Records from the Basic Information block of the Customer Information sheet, with the sheet's "
                 "heading line.",
        "notes": "Columns are named as the return names them and are the union of the layouts observed: Name in "
                 "the 2022 returns; First Name, Last Name, Tax ID, TnC and TnC Sign Date in the 2024 return. A "
                 "column a workbook lacks is blank. Heading (as produced) is the sheet's first line; Heading ID, "
                 "Heading Email and Heading Time (as produced) are the values that line labels id, email and time,"
                 " split from it as written. The module does not interpret the heading time range. The return does"
                 " not state a time zone for Registration time or the other times in this block, so they are "
                 "reported as produced and not converted. The heading used an ASCII or a full-width opening "
                 "parenthesis in the observed returns; both are read. In the 2022 returns compared cell by cell, "
                 "Mobile, User nationality, 2FA Opening time and SMS were empty, and Heading ID and Heading Email "
                 "matched User ID and Email.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "user",
    },
    "binanceApiInfo": {
        "name": "Binance - API Information",
        "description": "Records from the API Information block of the Customer Information sheet.",
        "notes": "The block held a header row and no records in every observed return, so this artifact has only "
                 "been exercised on synthetic data. Times carry no zone in the return and are reported as "
                 "produced.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "key",
    },
    "binanceKycInfo": {
        "name": "Binance - KYC Approved Info",
        "description": "Records from the KYC Approved Info block of the Customer Information sheet.",
        "notes": "Seen only in the 2024 return. Columns are named as the return names them and dates are reported "
                 "as produced. Heading ID is the id from the sheet's heading line, so rows from several workbooks "
                 "stay separable.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-11",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "id",
    },
    "binanceAddressValidation": {
        "name": "Binance - Address Validation",
        "description": "Records from the Address Validation block of the Customer Information sheet.",
        "notes": "Seen only in the 2024 return, where the block held a header and no records, so this artifact has"
                 " only been exercised on synthetic data. Heading ID is the id from the sheet's heading line.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-11",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "home",
    },
    "binanceSubAccounts": {
        "name": "Binance - Sub-accounts",
        "description": "Records from the Sub-accounts block of the Customer Information sheet.",
        "notes": "Seen only in the 2024 return. Values are reported as produced. Heading ID is the id from the "
                 "sheet's heading line.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-11",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "users",
    },
    "binanceCustomerOther": {
        "name": "Binance - Customer Information - Other Blocks",
        "description": "Records from Customer Information blocks this module does not recognise, reported cell for cell.",
        "notes": "Record (as produced) is every non-empty cell of the row as 'header: value' pairs, named by the "
                 "block's own header row. Rows above the first block, other than the heading line, are listed with"
                 " Block '(before the first block)' and column letters. No observed return had such a block.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-11",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "layout-grid",
    },
    "binanceBalanceOverview": {
        "name": "Binance - Account Balance - Overview",
        "description": "Records from Assets Overview blocks with the per-account BTC overview layout.",
        "notes": "Seen only in the Assets Overview sheet of the 2024 return, in the block titled 'single "
                 "overview'. The estimated total balance lines above the first block are reported under Account "
                 "Balance - Other Blocks. Values are reported as the text the return holds. The return does not "
                 "say at what time the balances were taken.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-11",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "chart-pie",
    },
    "binanceBalanceSpot": {
        "name": "Binance - Account Balance - Spot",
        "description": "Records from Account Balance and Assets Overview blocks with the Spot column layout.",
        "notes": "A block is assigned to this artifact by its header row, not its title. Sheet is the sheet it "
                 "came from (Account Balance in the 2022 returns, Assets Overview in the 2024 return) and Block "
                 "(as produced) its title row. USDT Equivalent appears only in the 2024 layout. Amounts are "
                 "reported as the text the return holds. The return does not say at what time the balances were "
                 "taken. In the 2022 returns compared cell by cell, All Positions equalled Available Positions on "
                 "every row, and In Withdrawal and Pending Order held one value throughout, as in the source.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "wallet",
    },
    "binanceBalanceHoldings": {
        "name": "Binance - Account Balance - Asset Positions",
        "description": "Records from Assets Overview blocks whose header has currency and BTC Equivalent columns "
                       "but no Available Positions column.",
        "notes": "In the 2024 return this layout held the blocks titled 'Earn - Saving - Locked Staking', 'Earn - "
                 "Autoinvest - My Index-Linked' and 'Funding'; Block (as produced) names which. Position Status "
                 "appears in some of those blocks only. Amounts are reported as the text the return holds.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-11",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "coins",
    },
    "binanceBalanceEarnProducts": {
        "name": "Binance - Account Balance - Earn Products",
        "description": "Records from Assets Overview blocks with the Earn product layout.",
        "notes": "Seen only in the 2024 return, in the block titled 'Earn - flexible savings'. Rates and amounts "
                 "are reported as the text the return holds.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-11",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "percentage",
    },
    "binanceBalanceFuturesPositions": {
        "name": "Binance - Account Balance - Futures Positions",
        "description": "Records from Account Balance and Assets Overview blocks with the futures position column layout.",
        "notes": "Blocks with this layout were titled 'Futures USDT position' and 'Futures 币本位 position' in the "
                 "2022 returns, and 'Futures USDT position' and 'Futures Coin position' in the 2024 return; Block "
                 "(as produced) keeps the title untranslated. A block is assigned by its header row. USDT "
                 "Equivalent appears only in the 2024 layout. Amounts are reported as the text the return holds.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "trending-up",
    },
    "binanceBalanceFuturesBalances": {
        "name": "Binance - Account Balance - Futures Balances",
        "description": "Records from Account Balance and Assets Overview blocks with the futures balance column layout.",
        "notes": "Blocks with this layout were titled 'Futures USDT balance' and 'Futures 币本位 balance' in the 2022"
                 " returns, and 'Futures USDT balance' and 'Futures Coin balance' in the 2024 return; Block (as "
                 "produced) keeps the title untranslated. A block is assigned by its header row. USDT Equivalent "
                 "appears only in the 2024 layout. Amounts are reported as the text the return holds.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "scale",
    },
    "binanceBalanceFuturesCollateral": {
        "name": "Binance - Account Balance - Futures Collateral",
        "description": "Records from Account Balance and Assets Overview blocks with the futures collateral column "
                 "layout.",
        "notes": "Columns are named as the return names them, lower-case asset and locked included. A block is "
                 "assigned by its header row. Amounts and rates are reported as the text the return holds.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "lock",
    },
    "binanceBalanceMarginCross": {
        "name": "Binance - Account Balance - Margin Cross",
        "description": "Records from Account Balance and Assets Overview blocks with the Margin - Cross column layout.",
        "notes": "A block is assigned by its header row. USDT Equivalent appears only in the 2024 layout. Amounts "
                 "are reported as the text the return holds. In the 2022 returns compared cell by cell, the one "
                 "with records held a single space in Total Balance on every row, reported blank, and one value "
                 "throughout in Borrowed and Interest.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "stack-2",
    },
    "binanceBalanceMarginIsolated": {
        "name": "Binance - Account Balance - Margin Isolated",
        "description": "Records from Account Balance and Assets Overview blocks with the Margin - Isolated column "
                 "layout.",
        "notes": "A block is assigned by its header row. USDT Equivalent appears only in the 2024 layout. Amounts "
                 "and ratios are reported as the text the return holds. In the 2022 returns compared cell by cell,"
                 " the one with records held the same value in Total Balance, Available Balance and Borrowed on "
                 "every row, as in the source.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "stack-2",
    },
    "binanceBalanceBlocks": {
        "name": "Binance - Account Balance - Block Index",
        "description": "One row per block of the Account Balance and Assets Overview sheets, with its record count and "
                 "the artifact that reports it.",
        "notes": "Titles are kept as produced, untranslated. Note (as produced) is the text of a block that holds "
                 "a note instead of records, such as 'Note: empty data'. A block with no records says only that "
                 "the return listed none for it. A block whose header matches no known layout is reported under "
                 "Account Balance - Other Blocks.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "list",
    },
    "binanceBalanceOther": {
        "name": "Binance - Account Balance - Other Blocks",
        "description": "Records from Account Balance and Assets Overview blocks whose header no known layout matches, "
                 "and rows above the first block.",
        "notes": "Record (as produced) is every non-empty cell of the row as 'header: value' pairs, named by the "
                 "block's own header row, or by column letter for rows above the first block, which are listed "
                 "with Block '(before the first block)'. In the 2024 return those were the total overview lines of"
                 " Assets Overview.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "layout-grid",
    },
    "binanceCurrentAssets": {
        "name": "Binance - Current Assets & Wallets",
        "description": "Records from the Current Assets & Wallets sheet.",
        "notes": "Columns are named as the return names them. Other Columns (as produced) is empty unless the "
                 "sheet carries columns this artifact does not name; such columns are kept there as JSON. Amounts "
                 "are reported as the text the return holds. Seen in the 2022 returns only.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "wallet",
    },
    "binanceDeposits": {
        "name": "Binance - Deposit History",
        "description": "Records from the Deposit History sheet.",
        "notes": "Columns are named as the return names them. Other Columns (as produced) is empty unless the "
                 "sheet carries columns this artifact does not name; such columns are kept there as JSON. Columns "
                 "are the union of the layouts observed: BUSD in the 2022 returns; Account Type and USDT in the "
                 "2024 return. A column a workbook lacks is blank. Create Time and the other times carry no zone "
                 "in the return and are reported as produced.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "download",
    },
    "binanceWithdrawals": {
        "name": "Binance - Withdrawal History",
        "description": "Records from the Withdrawal History sheet.",
        "notes": "Columns are named as the return names them. Other Columns (as produced) is empty unless the "
                 "sheet carries columns this artifact does not name; such columns are kept there as JSON. Columns "
                 "are the union of the layouts observed: BUSD in the 2022 returns; Account Type and USDT in the "
                 "2024 return. A header with a trailing space ('Destination Address ') is read the same as one "
                 "without. Apply Time carries no zone in the return and is reported as produced. Label/Tag/Memo "
                 "was empty on every row of the 2022 returns compared cell by cell.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "upload",
    },
    "binanceAttemptedWithdrawals": {
        "name": "Binance - Attempted Withdrawal History",
        "description": "Records from the ATTEMPTED WITHDRAWAL HISTORY sheet.",
        "notes": "Columns are named as the return names them. Other Columns (as produced) is empty unless the "
                 "sheet carries columns this artifact does not name; such columns are kept there as JSON. Seen "
                 "only in the 2024 return, where the sheet held a header and no records, so this artifact has only"
                 " been exercised on synthetic data. DecisionCode is reported as produced; the module does not "
                 "interpret it. Date carries no zone in the return and is reported as produced.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-11",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "ban",
    },
    "binanceOrders": {
        "name": "Binance - Order History",
        "description": "Records from the Order History sheet.",
        "notes": "Columns are named as the return names them. Other Columns (as produced) is empty unless the "
                 "sheet carries columns this artifact does not name; such columns are kept there as JSON. USDT "
                 "equivalent and Operation Source appear only in the 2024 layout. Time and Update Time carry no "
                 "zone in the return and are reported as produced. In the 2022 returns compared cell by cell, the "
                 "one with records held a single space in Type on every row, reported blank.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "shopping-cart",
    },
    "binanceMarginOrders": {
        "name": "Binance - Margin Order",
        "description": "Records from the Margin Order sheet.",
        "notes": "Columns are named as the return names them. Other Columns (as produced) is empty unless the "
                 "sheet carries columns this artifact does not name; such columns are kept there as JSON. The "
                 "sheet has the same columns as Order History. Seen only in the 2024 return, where the sheet held "
                 "a header and no records, so this artifact has only been exercised on synthetic data.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-11",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "shopping-cart",
    },
    "binanceAssetLogs": {
        "name": "Binance - Asset Logs",
        "description": "Records from the Spot Asset Log and Funding Asset Log sheets.",
        "notes": "Columns are named as the return names them. Other Columns (as produced) is empty unless the "
                 "sheet carries columns this artifact does not name; such columns are kept there as JSON. Sheet "
                 "names the log each row came from. Seen only in the 2024 return. Time carries no zone in the "
                 "return and is reported as produced. Type and Description are reported as produced; the module "
                 "does not interpret them.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-11",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "list",
    },
    "binanceP2P": {
        "name": "Binance - P2P",
        "description": "Records from the P2P sheet.",
        "notes": "Columns are named as the return names them. Other Columns (as produced) is empty unless the "
                 "sheet carries columns this artifact does not name; such columns are kept there as JSON. Seen "
                 "only in the 2024 return. Times carry no zone in the return and are reported as produced. Buy or "
                 "Sell is reported as produced.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-11",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "arrows-exchange",
    },
    "binanceFiatDeposits": {
        "name": "Binance - Fiat Deposit History",
        "description": "Records from the Fiat Deposit History sheet in the layout with an Internal Serial Number column.",
        "notes": "Columns are named as the return names them. Other Columns (as produced) is empty unless the "
                 "sheet carries columns this artifact does not name; such columns are kept there as JSON. The "
                 "sheet held a header row and no records in every 2022 return checked, so this artifact has only "
                 "been exercised on synthetic data. Times carry no zone in the return and are reported as "
                 "produced. In the 2024 return the sheet had another layout, reported under Fiat Orders.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "download",
    },
    "binanceFiatWithdrawals": {
        "name": "Binance - Fiat Withdrawal History",
        "description": "Records from the Fiat Withdrawal History sheet in the layout with an Internal Serial Number "
                 "column.",
        "notes": "Columns are named as the return names them. Other Columns (as produced) is empty unless the "
                 "sheet carries columns this artifact does not name; such columns are kept there as JSON. The "
                 "sheet held a header row and no records in every 2022 return checked, so this artifact has only "
                 "been exercised on synthetic data. Times carry no zone in the return and are reported as "
                 "produced. In the 2024 return the sheet had another layout, reported under Fiat Orders.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "upload",
    },
    "binanceFiatOrders": {
        "name": "Binance - Fiat Orders",
        "description": "Records from the Fiat Deposit History, Fiat Withdrawal History and Fiat Trades sheets in the "
                 "layout with an orderId column.",
        "notes": "Columns are named as the return names them. Other Columns (as produced) is empty unless the "
                 "sheet carries columns this artifact does not name; such columns are kept there as JSON. Sheet "
                 "names the sheet each row came from. This layout, with camel-case column names, was seen only in "
                 "the 2024 return, where the three sheets shared one header and held no records, so this artifact "
                 "has only been exercised on synthetic data. orderCreateTime carries no zone in the return and is "
                 "reported as produced. A Fiat sheet whose header matches neither layout is reported under Other "
                 "Sheets.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-11",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "building-bank",
    },
    "binanceFiatPaymentMethods": {
        "name": "Binance - Fiat Payment Methods",
        "description": "Records from the Fiat payment methods sheet.",
        "notes": "Columns are named as the return names them. Other Columns (as produced) is empty unless the "
                 "sheet carries columns this artifact does not name; such columns are kept there as JSON. Seen "
                 "only in the 2024 return, where the sheet held a header and no records, so this artifact has only"
                 " been exercised on synthetic data.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-11",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "credit-card",
    },
    "binanceAccessLogs": {
        "name": "Binance - Access Logs",
        "description": "Records from the Access Logs sheet.",
        "notes": "Timestamp (UTC) is converted from the column the return labels 'Timestamp (UTC)'; it is blank "
                 "when the value is not in the form YYYY-MM-DD HH:MM:SS, and Timestamp (as produced) holds the "
                 "value as written on every row. Port Number appears only in the 2024 layout. Operation, "
                 "Geolocation and the other columns are reported as produced.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "login",
    },
    "binanceOtcPayment": {
        "name": "Binance - OTC Payment",
        "description": "Records from the OTC Payment sheet.",
        "notes": "Columns are named as the return names them. Other Columns (as produced) is empty unless the "
                 "sheet carries columns this artifact does not name; such columns are kept there as JSON. Seen in "
                 "the 2022 returns; the 2024 return had an OTC Payment ID History sheet instead.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "credit-card",
    },
    "binanceOtcPaymentIdHistory": {
        "name": "Binance - OTC Payment ID History",
        "description": "Records from the OTC Payment ID History sheet.",
        "notes": "Columns are named as the return names them. Other Columns (as produced) is empty unless the "
                 "sheet carries columns this artifact does not name; such columns are kept there as JSON. Seen "
                 "only in the 2024 return. Update time values there carried a zone suffix in parentheses inside "
                 "the value; they are reported as produced and not converted. Payment Detail is reported as "
                 "produced.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-11",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "history",
    },
    "binanceFundingWallet": {
        "name": "Binance - Funding Wallet",
        "description": "Records from the Funding Wallet sheet.",
        "notes": "Columns are named as the return names them. Other Columns (as produced) is empty unless the "
                 "sheet carries columns this artifact does not name; such columns are kept there as JSON. Columns "
                 "are the union of the layouts observed: TotalAsset BUSD in the 2022 returns, TotalAsset USDT in "
                 "the 2024 return. Amounts are reported as the text the return holds.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "wallet",
    },
    "binanceSend": {
        "name": "Binance - Binance Send",
        "description": "Records from the Binance Send sheet.",
        "notes": "Columns are named as the return names them. Other Columns (as produced) is empty unless the "
                 "sheet carries columns this artifact does not name; such columns are kept there as JSON. Payer "
                 "and payee ID, nickname, phone and email columns and USDT equivalent appear only in the 2024 "
                 "layout. The sheet held a header row and no records in every observed return, so this artifact "
                 "has only been exercised on synthetic data. Times carry no zone in the return and are reported as"
                 " produced.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "send",
    },
    "binancePay": {
        "name": "Binance - Binance Pay",
        "description": "Records from the Binance Pay sheet.",
        "notes": "Columns are named as the return names them. Other Columns (as produced) is empty unless the "
                 "sheet carries columns this artifact does not name; such columns are kept there as JSON. Wallet, "
                 "counterparty, order and transaction ID columns and USDT equivalent appear only in the 2024 "
                 "layout. Times carry no zone in the return and are reported as produced.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "cash",
    },
    "binanceOtcTrading": {
        "name": "Binance - OTC Trading",
        "description": "Records from the OTC Trading sheet.",
        "notes": "Columns are named as the return names them. Other Columns (as produced) is empty unless the "
                 "sheet carries columns this artifact does not name; such columns are kept there as JSON. USDT "
                 "Equivalent appears only in the 2024 layout. Times carry no zone in the return and are reported "
                 "as produced; in the 2024 return they carried a suffix in parentheses inside the value.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "arrows-exchange",
    },
    "binanceCards": {
        "name": "Binance - Binance Card",
        "description": "Records from the Binance Card sheet.",
        "notes": "Columns are named as the return names them. Other Columns (as produced) is empty unless the "
                 "sheet carries columns this artifact does not name; such columns are kept there as JSON. UID "
                 "appears only in the 2024 layout. The sheet held a header row and no records in every observed "
                 "return, so this artifact has only been exercised on synthetic data.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "credit-card",
    },
    "binanceCardTransactions": {
        "name": "Binance - Binance Card Transactions",
        "description": "Records from the Binance Card transaction history sheet.",
        "notes": "Columns are named as the return names them. Other Columns (as produced) is empty unless the "
                 "sheet carries columns this artifact does not name; such columns are kept there as JSON. The "
                 "sheet was named 'Binance Card transaction histor' (cut at Excel's 31-character limit) in the "
                 "2022 returns and 'Binance Card transactions' in the 2024 return; any sheet whose name starts "
                 "with 'Binance Card transaction' is read. UID and USDT equivalent appear only in the 2024 layout."
                 " The sheet held a header row and no records in every observed return, so this artifact has only "
                 "been exercised on synthetic data.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "receipt",
    },
    "binanceGiftCardCreation": {
        "name": "Binance - Gift Card Creation",
        "description": "Records from the Gift Card Creation sheet.",
        "notes": "Columns are named as the return names them. Other Columns (as produced) is empty unless the "
                 "sheet carries columns this artifact does not name; such columns are kept there as JSON. Seen "
                 "only in the 2024 return, where the sheet held a header and no records, so this artifact has only"
                 " been exercised on synthetic data. Times carry no zone in the return and are reported as "
                 "produced.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-11",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "gift",
    },
    "binanceGiftCardTransfer": {
        "name": "Binance - Gift Card Transfer",
        "description": "Records from the Gift Card Transfer sheet.",
        "notes": "Columns are named as the return names them. Other Columns (as produced) is empty unless the "
                 "sheet carries columns this artifact does not name; such columns are kept there as JSON. Seen "
                 "only in the 2024 return, where the sheet held a header and no records, so this artifact has only"
                 " been exercised on synthetic data. Times carry no zone in the return and are reported as "
                 "produced.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-11",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "gift",
    },
    "binanceLoanOrders": {
        "name": "Binance - Loan Order",
        "description": "Records from the Loan Order sheet.",
        "notes": "Columns are named as the return names them. Other Columns (as produced) is empty unless the "
                 "sheet carries columns this artifact does not name; such columns are kept there as JSON. Seen "
                 "only in the 2024 return, where the sheet held a header and no records, so this artifact has only"
                 " been exercised on synthetic data. The headers label Confirmed Time and Deadline UTC; they are "
                 "reported as produced and not converted, since no value has been seen to confirm their form.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-11",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "moneybag",
    },
    "binanceRepayments": {
        "name": "Binance - Repayment History",
        "description": "Records from the Repayment History sheet.",
        "notes": "Columns are named as the return names them. Other Columns (as produced) is empty unless the "
                 "sheet carries columns this artifact does not name; such columns are kept there as JSON. Seen "
                 "only in the 2024 return, where the sheet held a header and no records, so this artifact has only"
                 " been exercised on synthetic data. The headers label Repaid Time and Borrowed Time 'UTC + 8'; "
                 "they are reported as produced and not converted.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-11",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "moneybag",
    },
    "binanceDevices": {
        "name": "Binance - Approved Devices",
        "description": "One row per device listed on the Approved Devices sheet.",
        "notes": "A device starts on a row with any of the device columns filled; the Key/Value pairs on that row "
                 "and on the rows below it, up to the next device, are listed under Approved Devices - Attributes "
                 "with the same Device Number. In some 2022 returns each header also carried a Chinese label after"
                 " the English one; columns are matched on the English words. Recent Usage Timestamp (UTC) is "
                 "converted from the column the return labels UTC and is blank when the value is not in the form "
                 "YYYY-MM-DD HH:MM:SS.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "device-mobile",
    },
    "binanceDeviceAttributes": {
        "name": "Binance - Approved Devices - Attributes",
        "description": "Key/Value pairs listed for each device on the Approved Devices sheet.",
        "notes": "Keys and values are reported as produced; the module does not interpret any key. The set of keys"
                 " differed between devices and between returns. A pair found above the first device is kept with "
                 "a blank Device Number and listed in Parsing Notes.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "list-details",
    },
    "binanceEmbeddedImages": {
        "name": "Binance - Embedded Images",
        "description": "Images embedded in the workbook, with the sheet and cell each is anchored on.",
        "notes": "Images are read from the workbook's own drawing parts, not from the sheet's cells. In the 2022 "
                 "returns compared cell by cell they were JPEG images anchored on the KYC Documents sheet, which "
                 "held no cells. The module does not say what an image shows. An image stored in the workbook but "
                 "not anchored on any sheet is reported with a blank Sheet.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "photo",
    },
    "binanceOtherSheets": {
        "name": "Binance - Other Sheets",
        "description": "Rows of sheets this module does not recognise, or whose header matches no known layout, reported"
                 " cell for cell.",
        "notes": "Cells (as produced) is every non-empty cell of the row as 'column letter: value' pairs, because "
                 "the module does not know which row of an unknown sheet is its header.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
        "paths": ("*.xlsx",),
        "output_types": "standard",
        "artifact_icon": "table",
    },
    "binanceParsingNotes": {
        "name": "Binance - Parsing Notes",
        "description": "What the module could not read or place, per workbook.",
        "notes": "Lists every .xlsx matched that was not read as a Binance return and why, workbooks that could "
                 "not be opened, the sheets of each recognised workbook, and every sheet, block or row reported "
                 "under one of the Other artifacts. Review the source workbook for each note.",
        "author": "@Maxitelmo, Claude",
        "creation_date": "2026-11-09",
        "last_update_date": "2026-11-11",
        "requirements": "openpyxl",
        "category": "Binance Returns",
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
_BLOCK_SHEETS = ("Account Balance", "Assets Overview")
_OTHER_BLOCKS = "(before the first block)"

# Plain table sheets. For each artifact: the sheets it reads (a name ending in '*' matches by
# prefix), the header names that select it when a sheet has had more than one layout, and the
# columns it reports, in report order: the union of every layout observed, named as produced.
_TABLES = {
    "binanceCurrentAssets": {
        "sheets": ("Current Assets & Wallets",),
        "columns": ("Asset Ticker", "Asset Name", "Total Position", "Estimated BTC Value",
                    "Deposit Wallet Address", "Label/Tag/Memo")},
    "binanceDeposits": {
        "sheets": ("Deposit History",),
        "columns": ("Create Time", "User ID", "Currency", "Amount", "Account Type", "BUSD", "USDT",
                    "Deposit Address", "Source Address", "TXID", "Status", "Network", "CounterParty ID")},
    "binanceWithdrawals": {
        "sheets": ("Withdrawal History",),
        "columns": ("Apply Time", "User ID", "Currency", "Amount", "Account Type", "BUSD", "USDT",
                    "Destination Address", "Label/Tag/Memo", "txId", "Status", "Network", "CounterParty ID")},
    "binanceAttemptedWithdrawals": {
        "sheets": ("ATTEMPTED WITHDRAWAL HISTORY",),
        "columns": ("Date", "User ID", "Asset", "Network", "Amount", "USDT Equivalent", "Address",
                    "Business Type", "Source", "DecisionCode")},
    "binanceOrders": {
        "sheets": ("Order History",),
        "columns": ("Time", "Update Time", "User ID", "Market ID", "Side", "Type", "Status", "Price", "Qty",
                    "Average Price", "Remain Qty", "Trade Qty", "Stop Price", "Price Unit", "Amount Unit",
                    "USDT equivalent", "Operation Source")},
    "binanceMarginOrders": {
        "sheets": ("Margin Order",),
        "columns": ("Time", "Update Time", "User ID", "Market ID", "Side", "Type", "Status", "Price", "Qty",
                    "Average Price", "Remain Qty", "Trade Qty", "Stop Price", "Price Unit", "Amount Unit",
                    "USDT equivalent", "Operation Source")},
    "binanceAssetLogs": {
        "sheets": ("Spot Asset Log", "Funding Asset Log"),
        "columns": ("Time", "User ID", "Order Number", "Commission ID", "Currency", "Type", "Amount",
                    "Available", "Locked", "Freeze", "Processing", "Description")},
    "binanceP2P": {
        "sheets": ("P2P",),
        "columns": ("Create Time", "Payment Time", "Release time", "Update time", "Target UID", "Order ID",
                    "Ad number", "Buy or Sell", "Crypto", "Amount", "Fiat Currency", "Total Amount",
                    "Unit Price", "USDT equivalent", "Take ID", "Ad publisher ID", "Status", "Payment method",
                    "Client")},
    "binanceFiatDeposits": {
        "sheets": ("Fiat Deposit History",),
        "require": ("Internal Serial Number",),
        "columns": ("Create Time", "Completed Time", "Arrived Time", "Update Time", "Status", "UserID",
                    "Email", "Amount", "Currency", "Internal Serial Number", "External Serial Number",
                    "Second External Serial Number", "Source Account Id", "Source Account Name",
                    "Source Account", "Golden Channel", "Remark", "Is Replacement Order?", "Abnormal Reason",
                    "Error Code", "Error Reason", "Channel Fee", "Platform Fee", "Network Provider",
                    "Expect Recharge Amount", "Narrative", "Order Type")},
    "binanceFiatWithdrawals": {
        "sheets": ("Fiat Withdrawal History",),
        "require": ("Internal Serial Number",),
        "columns": ("Create Time", "Completed Time", "Arrived Time", "Update Time", "Status", "UserID",
                    "Email", "Amount", "Currency", "Internal Serial Number", "External Serial Number",
                    "Target Account Id", "Target Name", "Target Account", "Withdraw Channel", "Remark",
                    "Is Replacement Order?", "Abnormal Reason", "Error Reason", "Channel Fee", "Platform Fee",
                    "Network Provider", "Withdrawer", "Narrative", "Bic", "Bank", "Country", "Sortcode",
                    "Bank Address", "Bank City", "Iban", "Flutterwave Proof")},
    "binanceFiatOrders": {
        "sheets": ("Fiat Deposit History", "Fiat Withdrawal History", "Fiat Trades"),
        "require": ("orderId",),
        "columns": ("orderCreateTime", "userId", "userEmail", "userName", "orderId", "channelOrderId",
                    "businessType", "statusName", "currency", "grossAmount", "grossAmountUsd",
                    "cryptoCurrency", "cryptoAmount", "cryptoObtainAmount", "orderExecutePrice",
                    "cryptoNetwork", "cryptoAddress", "cryptoAddressMemo", "cryptoTransactionHash", "userFee",
                    "merchantFee", "networkFee", "channelName", "transactionMethod", "cardBin",
                    "cardLast4Digital", "viban", "iban", "accountNumber", "receivableAccount",
                    "payableAccount")},
    "binanceFiatPaymentMethods": {
        "sheets": ("Fiat payment methods",),
        "columns": ("Create Time", "Update Time", "User ID", "Card ID", "Card Number", "First Name",
                    "Family Name", "Card Country", "Card Scheme", "Bind Type", "Security Type", "expired date",
                    "bank", "cardType")},
    "binanceAccessLogs": {
        "sheets": ("Access Logs",),
        "columns": ("Timestamp (UTC)", "User ID", "Operation", "Client", "Client Version", "Real IP",
                    "Port Number", "Geolocation", "Browser")},
    "binanceOtcPayment": {
        "sheets": ("OTC Payment",),
        "columns": ("User ID", "Receiving Payment ID", "Name", "Payment method", "Bank account number",
                    "Bank name", "Account opening branch")},
    "binanceOtcPaymentIdHistory": {
        "sheets": ("OTC Payment ID History",),
        "columns": ("Update time", "User Id", "Payment ID", "Action", "Client", "Status", "Handler",
                    "Payment Method", "Payment Detail")},
    "binanceFundingWallet": {
        "sheets": ("Funding Wallet",),
        "columns": ("User ID", "TotalAsset", "TotalAsset BUSD", "TotalAsset USDT", "AssetCode", "AssetName",
                    "Freeze", "Withdrawing", "Free", "Locked")},
    "binanceSend": {
        "sheets": ("Binance Send",),
        "columns": ("Send time", "Complete time", "Update time", "Send number", "Payer ID",
                    "Payer account type", "Payer type", "Payer nickname", "Payer phone area code",
                    "Payer phone number", "Payer email", "Payee ID", "Payee account type", "Payee nickname",
                    "Payee phone area code", "Payee phone number", "Payee email", "Amount", "Asset",
                    "Assets BTC rate", "USDT equivalent", "Send note", "Send type", "Send source",
                    "Send status")},
    "binancePay": {
        "sheets": ("Binance Pay",),
        "columns": ("Transaction Time", "User ID", "Transaction wallet ID", "Merchant Name",
                    "Counterparty Wallet ID", "Counterparty Binance ID", "Order ID", "Transaction ID",
                    "Transaction Type", "Currency", "Amount", "USDT equivalent")},
    "binanceOtcTrading": {
        "sheets": ("OTC Trading",),
        "columns": ("CreateTime", "UpdateTime", "UserCompletedTime", "ChannelCompletedTime", "OrderId",
                    "UserId", "ChannelCode", "QuoteId", "PayType", "UserStatus", "UserCurrentPhase",
                    "ChannelStatus", "ChannelCurrentPhase", "symbol", "BaseCoin", "QuoteCoin", "BaseCoinAmount",
                    "QuoteCoinAmount", "USDT Equivalent", "SpreadAmount", "SpreadCoin", "UserQuotePrice",
                    "UserSpreadPrice", "ChannelQuotePrice", "RequestAmount", "RequestAmountCoin", "TransId",
                    "OtcUserId", "SpreadUserId", "ChannelUserId", "UserRemark", "ChannelRemark")},
    "binanceCards": {
        "sheets": ("Binance Card",),
        "columns": ("Create Date", "UID", "Swipe Card ID", "Swipe User ID", "Card Number", "Card Type",
                    "Locked", "Freeze", "Activated", "Card Status")},
    "binanceCardTransactions": {
        "sheets": ("Binance Card transaction*",),
        "columns": ("Created date", "UID", "Swipe Card ID", "Transaction ID", "Merchant Name", "Status",
                    "Type", "Currency", "Channel", "Approved", "Total", "USDT equivalent")},
    "binanceGiftCardCreation": {
        "sheets": ("Gift Card Creation",),
        "columns": ("mint_time", "redeemed_time", "minter_id", "redeemer_id", "card_no", "card_assets",
                    "token", "card_status_text", "amt_usd", "asset_quantity")},
    "binanceGiftCardTransfer": {
        "sheets": ("Gift Card Transfer",),
        "columns": ("card_redeem_time", "user_id", "counterparty_user_id", "card_no", "is_redeemed", "token",
                    "amt_usd", "asset_quantity")},
    "binanceLoanOrders": {
        "sheets": ("Loan Order",),
        "columns": ("Confirmed Time[UTC]", "Deadline[UTC)", "Seq", "Order ID", "User ID", "Collateral Level",
                    "Loan Coin", "Init Loan Amount", "Left Repay Amount", "USDT equivalent",
                    "Left Repay Interest", "Interest Accrual", "Daily Interest Rate", "Collateral Coin",
                    "Initial Collateral Amount", "Remaining Collateral Amount", "Duration",
                    "ActualInterestDays", "OverdueDays", "Type", "Init Collateral Rate",
                    "Margin Call Collateral Rate", "liquidation Collateral Rate", "Order Status",
                    "Status Details", "Late Editor")},
    "binanceRepayments": {
        "sheets": ("Repayment History",),
        "columns": ("Repaid Time[UTC + 8]", "Borrowed Time[UTC + 8]", "Seq", "UID", "Order ID",
                    "Order Group Id", "Event No", "Coin", "Amount", "USDT equivalent", "Interest", "Principal",
                    "CollateralCoin", "Repay Collateral", "Loan / Collateral Price", "Released Collateral",
                    "LTV after repayment", "Repay Type", "Status", "Staking Order")},
}

# Columns the return labels UTC in a form this module converts: reported converted and as produced.
_UTC_COLUMNS = ("Timestamp (UTC)", "Recent Usage Timestamp (UTC)")

# Block layouts of Account Balance and Assets Overview, matched on the header row in this order:
# artifact -> (columns every observed header of the layout holds, columns reported).
_BALANCE_LAYOUTS = {
    "binanceBalanceSpot": (
        ("Currency Name", "Currency Code", "All Positions", "Available Positions", "In Withdrawal",
         "Pending Order", "BTC Equivalent"),
        ("Currency Name", "Currency Code", "All Positions", "Available Positions", "In Withdrawal",
         "Pending Order", "BTC Equivalent", "USDT Equivalent")),
    "binanceBalanceHoldings": (
        ("Currency Name", "Currency Code", "All Positions", "BTC Equivalent"),
        ("Currency Name", "Currency Code", "All Positions", "BTC Equivalent", "USDT Equivalent",
         "Position Status")),
    "binanceBalanceEarnProducts": (
        ("Product Name", "Total Amount"),
        ("Product Name", "Total Amount", "Accruing Interest", "Today Purchased Amount", "Redeeming Amount",
         "Total Interest", "Average Annual Interest Rate", "USDT Equivalent")),
    "binanceBalanceOverview": (
        ("Spot(BTC)", "Futures(BTC)"),
        ("Spot(BTC)", "Futures(BTC)", "Earn(BTC)", "MARGIN(BTC)", "Pool(BTC)", "Funding(BTC)",
         "Option(BTC)")),
    "binanceBalanceFuturesPositions": (
        ("Symbol", "Position Amount", "Entry Price", "Mark Price", "Unrealized Profit"),
        ("Symbol", "Position Amount", "Entry Price", "Mark Price", "Unrealized Profit", "USDT Equivalent")),
    "binanceBalanceFuturesBalances": (
        ("Asset", "Wallet Balance", "Unrealized Profit", "Available For Order"),
        ("Asset", "Wallet Balance", "Unrealized Profit", "Available For Order", "USDT Equivalent")),
    "binanceBalanceFuturesCollateral": (
        ("asset", "locked", "Loan Amount(USDT)", "Total Principal For Interest(USDT)", "Current Rate",
         "Initial Rate", "Liquidation Collateral Rate", "Liquidation Price", "Total Interest(USDT)"),
        ("asset", "locked", "Loan Amount(USDT)", "Total Principal For Interest(USDT)", "Current Rate",
         "Initial Rate", "Liquidation Collateral Rate", "Liquidation Price", "Total Interest(USDT)")),
    "binanceBalanceMarginCross": (
        ("Currency", "Total Balance", "Available Balance", "Borrowed", "Interest"),
        ("Currency", "Total Balance", "Available Balance", "Borrowed", "Interest", "USDT Equivalent")),
    "binanceBalanceMarginIsolated": (
        ("Trading Pair", "Risk Ratio", "Effective Multiple", "Currency", "Total Balance", "Available Balance",
         "Borrowed"),
        ("Trading Pair", "Risk Ratio", "Effective Multiple", "Currency", "Total Balance", "Available Balance",
         "Borrowed", "USDT Equivalent")),
}

# Customer Information blocks: title -> (artifact, columns reported).
_CUSTOMER_BLOCKS = {
    "Basic Information": ("binanceCustomerInfo", (
        "Registration time", "User ID", "Email", "Mobile", "Name", "First Name", "Last Name",
        "User nationality", "User ID number", "User authentication type", "User authentication time",
        "Status", "2FA", "2FA Opening time", "SMS", "SMS Opening time", "2FA Reset Information", "Tax ID",
        "TnC", "TnC Sign Date")),
    "API Information": ("binanceApiInfo", (
        "Create Time", "Update Time", "Rule ID", "API Name", "Trade IP", "Withdraw IP")),
    "KYC Approved Info": ("binanceKycInfo", (
        "Birthday", "ID issue Country", "ID Address", "ID type", "ID Sub-type", "issuing Authority",
        "Issuing Date", "ID expiry Date")),
    "Address Validation": ("binanceAddressValidation", (
        "Residence", "Region/State", "City", "Address", "Postal/Zip Code")),
    "Sub-accounts": ("binanceSubAccounts", ("Has Sub-account", "Sub-account Number")),
}
_DEVICE_COLUMNS = ("Device Name", "Client", "IP Address", "Geolocation", "Recent Usage Timestamp (UTC)",
                   "Status")
_OWN_SHEETS = ("Customer Information", "Approved Devices", "KYC Documents") + _BLOCK_SHEETS

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


def _letters(cells):
    return [_column_letter(i) for i in range(len(cells))]


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


def _name_matches(title, name):
    return title.startswith(name[:-1]) if name.endswith("*") else title == name


def _header_row(sheet_rows):
    """(index, normalised header) of the first non-empty row, or (None, None)."""
    index = next((i for i, r in enumerate(sheet_rows) if not _blank(r)), None)
    if index is None:
        return None, None
    return index, [_header(c) for c in sheet_rows[index]]


def _table_claims(sheets):
    """{sheet title: artifact} for every sheet a table artifact reads, chosen by name and header."""
    claims = {}
    for title, sheet_rows in sheets.items():
        _index, header = _header_row(sheet_rows)
        names = set(header or ())
        for artifact, spec in _TABLES.items():
            if not any(_name_matches(title, name) for name in spec["sheets"]):
                continue
            if header is None or set(spec.get("require", ())) <= names:
                claims[title] = artifact
                break
    return claims


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
    for artifact, (required, _columns) in _BALANCE_LAYOUTS.items():
        if set(required) <= names:
            return artifact
    return None


def _block_sheets(sheets):
    """(sheet title, preamble, blocks) for each Account Balance or Assets Overview sheet present."""
    out = []
    for title in _BLOCK_SHEETS:
        if title in sheets:
            preamble, blocks = _blocks(sheets[title])
            out.append((title, preamble, blocks))
    return out


def _customer_blocks(sheets):
    rows = sheets.get("Customer Information", [])
    preamble, blocks = _blocks(rows)
    heading = next((cells[0] for _n, cells in preamble if cells[0].startswith("User Basic Information")), "")
    return heading, preamble, blocks


def _heading_parts(heading):
    match = _HEADING.match(heading)
    return [match.group("id"), match.group("email"), match.group("time")] if match else ["", "", ""]


# ------------------------------------------------------------------ artifact builders
def _table_artifact(context, artifact):
    spec = _TABLES[artifact]
    known = spec["columns"]
    several = len(spec["sheets"]) > 1
    headers = ["Sheet"] if several else []
    for column in known:
        if column in _UTC_COLUMNS:
            headers += [(column, "datetime"), column.replace("(UTC)", "(as produced)")]
        else:
            headers.append(column)
    headers += ["Other Columns (as produced)", "Sheet Row", "Source File"]
    rows, sources = [], set()
    for source, sheets in _workbooks(context):
        for title, claimed_by in _table_claims(sheets).items():
            if claimed_by != artifact:
                continue
            sources.add(source)
            sheet_rows = sheets[title]
            header_index, header = _header_row(sheet_rows)
            if header_index is None:
                continue
            for index in range(header_index + 1, len(sheet_rows)):
                cells = sheet_rows[index]
                if _blank(cells):
                    continue
                record = _record(header, cells)
                line = [title] if several else []
                for column in known:
                    value = record.get(column, "")
                    if column in _UTC_COLUMNS:
                        line += [_utc(value), value]
                    else:
                        line.append(value)
                line += [_extra(header, cells, known), index + 1, context.get_relative_path(source)]
                rows.append(tuple(line))
    return tuple(headers), rows, "\n".join(sorted(sources))


def _customer_artifact(context, title):
    artifact, known = _CUSTOMER_BLOCKS[title]
    basic = artifact == "binanceCustomerInfo"
    headers = (["Heading (as produced)", "Heading ID", "Heading Email", "Heading Time (as produced)"] if basic
               else ["Heading ID"])
    headers += list(known) + ["Other Columns (as produced)", "Sheet Row", "Source File"]
    rows, sources = [], set()
    for source, sheets in _workbooks(context):
        heading, _preamble, blocks = _customer_blocks(sheets)
        sources.add(source)
        parsed = _heading_parts(heading)
        for block in blocks:
            if block["title"] != title or not block["header"]:
                continue
            for number, cells in block["records"]:
                record = _record(block["header"], cells)
                line = [heading] + parsed if basic else [parsed[0]]
                line += [record.get(c, "") for c in known]
                line += [_extra(block["header"], cells, known), number, context.get_relative_path(source)]
                rows.append(tuple(line))
    return tuple(headers), rows, "\n".join(sorted(sources))


def _balance_artifact(context, artifact):
    _required, known = _BALANCE_LAYOUTS[artifact]
    headers = ["Sheet", "Block (as produced)"] + list(known) + ["Other Columns (as produced)", "Sheet Row",
                                                                 "Source File"]
    rows, sources = [], set()
    for source, sheets in _workbooks(context):
        for title, _preamble, blocks in _block_sheets(sheets):
            sources.add(source)
            for block in blocks:
                if _layout_for(block["header"]) != artifact:
                    continue
                for number, cells in block["records"]:
                    record = _record(block["header"], cells)
                    rows.append(tuple([title, block["title"]] + [record.get(c, "") for c in known]
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
    return _customer_artifact(context, "Basic Information")


@artifact_processor
def binanceApiInfo(context):
    return _customer_artifact(context, "API Information")


@artifact_processor
def binanceKycInfo(context):
    return _customer_artifact(context, "KYC Approved Info")


@artifact_processor
def binanceAddressValidation(context):
    return _customer_artifact(context, "Address Validation")


@artifact_processor
def binanceSubAccounts(context):
    return _customer_artifact(context, "Sub-accounts")


@artifact_processor
def binanceCustomerOther(context):
    headers = ("Block (as produced)", "Record (as produced)", "Sheet Row", "Source File")
    rows, sources = [], set()
    for source, sheets in _workbooks(context):
        if "Customer Information" not in sheets:
            continue
        sources.add(source)
        _heading, preamble, blocks = _customer_blocks(sheets)
        for number, cells in preamble:
            if not cells[0].startswith("User Basic Information"):
                rows.append((_OTHER_BLOCKS, _pairs(_letters(cells), cells), number,
                             context.get_relative_path(source)))
        for block in blocks:
            if block["title"] in _CUSTOMER_BLOCKS:
                continue
            for number, cells in block["records"]:
                rows.append((block["title"], _pairs(block["header"] or [], cells), number,
                             context.get_relative_path(source)))
    return headers, rows, "\n".join(sorted(sources))


@artifact_processor
def binanceBalanceOverview(context):
    return _balance_artifact(context, "binanceBalanceOverview")


@artifact_processor
def binanceBalanceSpot(context):
    return _balance_artifact(context, "binanceBalanceSpot")


@artifact_processor
def binanceBalanceHoldings(context):
    return _balance_artifact(context, "binanceBalanceHoldings")


@artifact_processor
def binanceBalanceEarnProducts(context):
    return _balance_artifact(context, "binanceBalanceEarnProducts")


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
    headers = ("Sheet", "Block (as produced)", "Header (as produced)", "Records", "Note (as produced)",
               "Reported In", "Sheet Row", "Source File")
    rows, sources = [], set()
    for source, sheets in _workbooks(context):
        for title, _preamble, blocks in _block_sheets(sheets):
            sources.add(source)
            for block in blocks:
                layout = _layout_for(block["header"])
                if layout:
                    reported = names[layout]
                elif block["records"]:
                    reported = __artifacts_v2__["binanceBalanceOther"]["name"]
                else:
                    reported = ""
                header = "; ".join(c for c in (block["header_raw"] or ()) if c)
                rows.append((title, block["title"], header, len(block["records"]), block["note"], reported,
                             block["row"], context.get_relative_path(source)))
    return headers, rows, "\n".join(sorted(sources))


@artifact_processor
def binanceBalanceOther(context):
    headers = ("Sheet", "Block (as produced)", "Record (as produced)", "Sheet Row", "Source File")
    rows, sources = [], set()
    for source, sheets in _workbooks(context):
        for title, preamble, blocks in _block_sheets(sheets):
            sources.add(source)
            for number, cells in preamble:
                rows.append((title, _OTHER_BLOCKS, _pairs(_letters(cells), cells), number,
                             context.get_relative_path(source)))
            for block in blocks:
                if _layout_for(block["header"]):
                    continue
                for number, cells in block["records"]:
                    rows.append((title, block["title"], _pairs(block["header"] or [], cells), number,
                                 context.get_relative_path(source)))
    return headers, rows, "\n".join(sorted(sources))


@artifact_processor
def binanceCurrentAssets(context):
    return _table_artifact(context, "binanceCurrentAssets")


@artifact_processor
def binanceDeposits(context):
    return _table_artifact(context, "binanceDeposits")


@artifact_processor
def binanceWithdrawals(context):
    return _table_artifact(context, "binanceWithdrawals")


@artifact_processor
def binanceAttemptedWithdrawals(context):
    return _table_artifact(context, "binanceAttemptedWithdrawals")


@artifact_processor
def binanceOrders(context):
    return _table_artifact(context, "binanceOrders")


@artifact_processor
def binanceMarginOrders(context):
    return _table_artifact(context, "binanceMarginOrders")


@artifact_processor
def binanceAssetLogs(context):
    return _table_artifact(context, "binanceAssetLogs")


@artifact_processor
def binanceP2P(context):
    return _table_artifact(context, "binanceP2P")


@artifact_processor
def binanceFiatDeposits(context):
    return _table_artifact(context, "binanceFiatDeposits")


@artifact_processor
def binanceFiatWithdrawals(context):
    return _table_artifact(context, "binanceFiatWithdrawals")


@artifact_processor
def binanceFiatOrders(context):
    return _table_artifact(context, "binanceFiatOrders")


@artifact_processor
def binanceFiatPaymentMethods(context):
    return _table_artifact(context, "binanceFiatPaymentMethods")


@artifact_processor
def binanceAccessLogs(context):
    return _table_artifact(context, "binanceAccessLogs")


@artifact_processor
def binanceOtcPayment(context):
    return _table_artifact(context, "binanceOtcPayment")


@artifact_processor
def binanceOtcPaymentIdHistory(context):
    return _table_artifact(context, "binanceOtcPaymentIdHistory")


@artifact_processor
def binanceFundingWallet(context):
    return _table_artifact(context, "binanceFundingWallet")


@artifact_processor
def binanceSend(context):
    return _table_artifact(context, "binanceSend")


@artifact_processor
def binancePay(context):
    return _table_artifact(context, "binancePay")


@artifact_processor
def binanceOtcTrading(context):
    return _table_artifact(context, "binanceOtcTrading")


@artifact_processor
def binanceCards(context):
    return _table_artifact(context, "binanceCards")


@artifact_processor
def binanceCardTransactions(context):
    return _table_artifact(context, "binanceCardTransactions")


@artifact_processor
def binanceGiftCardCreation(context):
    return _table_artifact(context, "binanceGiftCardCreation")


@artifact_processor
def binanceGiftCardTransfer(context):
    return _table_artifact(context, "binanceGiftCardTransfer")


@artifact_processor
def binanceLoanOrders(context):
    return _table_artifact(context, "binanceLoanOrders")


@artifact_processor
def binanceRepayments(context):
    return _table_artifact(context, "binanceRepayments")


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
        claims = _table_claims(sheets)
        for title, sheet_rows in sheets.items():
            if title in _OWN_SHEETS or title in claims:
                continue
            for index, cells in enumerate(sheet_rows):
                if not _blank(cells):
                    rows.append((title, index + 1, _pairs(_letters(cells), cells),
                                 context.get_relative_path(source)))
    return headers, rows, "\n".join(sorted(sources))


@artifact_processor
def binanceParsingNotes(context):
    headers = ("Sheet", "Sheet Row", "Note", "Source File")
    notes = []
    workbooks = _workbooks(context, notes)
    other_blocks = {key: __artifacts_v2__[key]["name"] for key in ("binanceCustomerOther", "binanceBalanceOther")}
    for source, sheets in workbooks:
        titles = list(sheets)
        notes.append((source, "", "", f"read as a Binance return; {len(titles)} sheets: " + "; ".join(titles)))
        claims = _table_claims(sheets)
        unknown = [t for t in titles if t not in _OWN_SHEETS and t not in claims]
        if unknown:
            notes.append((source, "", "", "sheets not recognised, or whose header matches no known layout, "
                          "reported under Other Sheets: " + "; ".join(unknown)))
        heading, preamble, blocks = _customer_blocks(sheets)
        if "Customer Information" in sheets and not _HEADING.match(heading):
            notes.append((source, "Customer Information", "",
                          "heading line not found or not in the expected form; Heading ID, Heading Email "
                          "and Heading Time are blank"))
        for number, _cells in preamble:
            if not _cells[0].startswith("User Basic Information"):
                notes.append((source, "Customer Information", number,
                              f"row before the first block, reported under {other_blocks['binanceCustomerOther']}"))
        for block in blocks:
            if block["title"] not in _CUSTOMER_BLOCKS:
                notes.append((source, "Customer Information", block["row"],
                              f"block '{block['title']}' not recognised, reported under "
                              f"{other_blocks['binanceCustomerOther']}"))
        for title, preamble, blocks in _block_sheets(sheets):
            for number, _cells in preamble:
                notes.append((source, title, number,
                              f"row before the first block, reported under {other_blocks['binanceBalanceOther']}"))
            for block in blocks:
                if block["records"] and not _layout_for(block["header"]):
                    notes.append((source, title, block["row"],
                                  f"block '{block['title']}' has a header no known layout matches, reported "
                                  f"under {other_blocks['binanceBalanceOther']}"))
        if "Approved Devices" in sheets:
            _devices, _attributes, orphans = _device_rows(sheets["Approved Devices"])
            for number in orphans:
                notes.append((source, "Approved Devices", number,
                              "Key/Value pair above the first device; reported with a blank Device Number"))
    rows = [(sheet, number, note, context.get_relative_path(source)) for source, sheet, number, note in notes]
    sources = sorted({source for source, _s, _n, _t in notes})
    return headers, rows, "\n".join(sources)

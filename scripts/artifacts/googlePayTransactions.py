__artifacts_v2__ = {
    "googlePayTransactions": {
        "name": "Google Pay Transactions",
        "description": "Purchases on Google like Play and YouTube, and purchases made using Google Pay balance.",
        "author": "@KevinPagano3",
        "creation_date": "2021-09-25",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "Transaction Timestamp is preserved as the raw source value (Takeout CSV format is locale-dependent; not normalized to UTC).",
        "paths": ('*/Google Pay/Google transactions/transactions_*.csv'),
        "output_types": "standard",
        "artifact_icon": "dollar-sign",
    }
}

import csv
import os

from scripts.ilapfuncs import artifact_processor


@artifact_processor
def googlePayTransactions(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).startswith('transactions'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader, None)
            for item in reader:
                if len(item) == 0:
                    continue
                data_list.append((item[0], item[1], item[2], item[3], item[4], item[5], item[6]))

    data_headers = ('Transaction Timestamp', 'Transaction ID', 'Description', 'Product',
                    'Payment Method', 'Payment Status', 'Amount')
    return data_headers, data_list, context.get_relative_path(source_path)

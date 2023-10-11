import os
import openpyxl

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_tikTokipdata(files_found, report_folder, seeker, wrap_text, time_offset):
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('~'):
            continue
        if filename.startswith('.'):
            continue
        
        dth = []
        listtemp = []
        data_headers = []
        data_list =[]
        
        subscriber = filename.split('-')
        
        wb_obj = openpyxl.load_workbook(file_found)
        sheet_obj = wb_obj.active
        
        max_col = sheet_obj.max_column
        m_row = sheet_obj.max_row
        
        # Will print a particular row value
        for j in range(1, m_row + 1):
            for i in range(1, max_col + 1):
                cell_obj = sheet_obj.cell(row = j, column = i)
                value = (cell_obj.value)
                listtemp.append(value)
            data_list.append((listtemp))
            listtemp = []
            
        if data_list:
            data_list.pop(0) #eliminate headers from excel file
            report = ArtifactHtmlReport(f'TikTok - IP Data [{subscriber[0]}] ')
            report.start_artifact_report(report_folder, f'TikTok - IP Data [{subscriber[0]}] ')
            report.add_script()
            data_headers = ('Timestamp', 'Active Start Time', 'IP', 'IP Country' )
            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()
        else:
            logfunc(f'No TikTok - IP Data [{subscriber[0]}]  available')

__artifacts__ = {
        "tikTokipdata": (
            "TikTok Returns",
            ('*/*/*- IP Data.xlsx'),
            get_tikTokipdata)
}
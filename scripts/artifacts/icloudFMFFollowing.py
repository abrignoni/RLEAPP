import os
import xlrd

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_icloudFMFFollowing(files_found, report_folder, seeker, wrap_text, time_offset):
    
    for file_found in files_found:
        file_found = str(file_found)
        filename = os.path.basename(file_found)
        
        if filename.startswith('~'):
            continue
        if filename.startswith('.'):
            continue
        
        loc = file_found
        
        
        dth = []
        list = []
        data_headers = []
        data_list =[]
        
        #First worksheet
        
        wb = xlrd.open_workbook(loc)
        sheetnames = wb.sheet_names() 
        sheet = wb.sheet_by_index(0)
        #dsid = sheet.cell_value(2, 0)
        
        for i in range(sheet.nrows):
            for j in range(sheet.ncols):
                if i == 1:
                    dth.append(sheet.cell_value(i, j))
                if i >= 2:
                    list.append(sheet.cell_value(i, j))
            if i >= 2:
                data_list.append(list) 
            list =[]
        
        
        if data_list:
            #description = f'Sheet name: {sheetnames[0]} - {dsid}'
            description = f'Sheet name: {sheetnames[0]}'
            report = ArtifactHtmlReport('iCloud - FMF Following')
            report.start_artifact_report(report_folder, 'iCloud - FMF Following', description)
            report.add_script()
            data_headers = (dth)
            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()
            
        else:
            logfunc('No iCloud - FMF Following data available')
            
__artifacts__ = {
        "icloudFMFFollowing": (
            "iCloud Returns",
            ('*/fmf/*_Following.xlsx'),
            get_icloudFMFFollowing)
}
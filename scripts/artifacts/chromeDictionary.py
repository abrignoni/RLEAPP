import codecs
import csv
from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, is_platform_windows
def get_chromeDictionary(files_found, report_folder, seeker, wrap_text):
    data_list = []
    file_found = str(files_found[0])
    counter = 1
    with codecs.open(file_found, 'r', 'utf-8-sig') as csvfile:
        for row in csvfile:
            data_list.append((counter, row))
            counter += 1
            
    if len(data_list) > 0:
        report = ArtifactHtmlReport('Google Chrome User Dictionary')
        report.start_artifact_report(report_folder, f'Google Chrome User Dictionary')
        report.add_script()
        data_headers = ('Order', 'Word')
        report.write_artifact_data_table(data_headers, data_list, file_found)
        report.end_artifact_report()
        
        tsvname = f'Google User Chrome Dictionary'
        tsv(report_folder, data_headers, data_list, tsvname)
        
    else:
        logfunc(f'No Google Chrome User Dictionary data available')
    
__artifacts__ = {
        "chromeDictionary": (
                "Google Takeout Archive",
                ('*/Chrome/Dictionary.csv'),
                get_chromeDictionary)
}

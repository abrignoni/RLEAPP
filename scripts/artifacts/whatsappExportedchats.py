import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html, kmlgen, media_to_html


def get_whatsappExportedchats(files_found, report_folder, seeker, wrap_text, time_offset):
    
    data_list = []
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        count = 0
        if file_found.endswith('_chat.txt'):
            with open(file_found, 'r') as f:
                for line in f:
                    count = count + 1
                    line = line.replace(u'\u200e', '')
                    line = line.strip()
                    dividido = (line.strip().split(']'))
                    thumb = ''
                    if len(dividido) > 1:
                        fecha = dividido[0].replace('[','')
                        
                        if ':' in dividido[1]:
                            name = (dividido[1].split(':')[0])
                            mensaje = (dividido[1].split(':',1)[1])
                            
                        else:
                            name = ''
                            mensaje = dividido[1]
                            
                        if '<attached: ' in mensaje:
                            attach = mensaje.split('<attached: ')[1].replace('>','')
                            thumb = media_to_html(attach, files_found, report_folder)
                        else:
                            attach = ''
                    else:
                        mensaje = line
                        
                        
                    if mensaje != '':
                        data_list.append((fecha, count, name, mensaje, thumb))
                    
        
        
        
    
    if data_list:
        report = ArtifactHtmlReport(f'Whatsapp Exported Chat')
        report.start_artifact_report(report_folder, f'Whatsapp Exported Chat')
        report.add_script()
        data_headers = ('Timestamp','Count','Username','Message','Media')
        report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Media'])
        report.end_artifact_report()
        
        tsvname = f'Whatsapp Exported Chat'
        tsv(report_folder, data_headers, data_list, tsvname)
        
        tlactivity = f'Whatsapp Exported Chat'
        timeline(report_folder, tlactivity, data_list, data_headers)
        
        #kmlactivity = f'Snapchat - Geolocations  - {username}'
        #kmlgen(report_folder, kmlactivity, data_list, data_headers)
    else:
        logfunc(f'No Whatsapp Exported Chat')
    
__artifacts__ = {
        "whatsappExportedchats": (
            "Whatsapp Exported Chat",
            ('*/*.*'),
            get_whatsappExportedchats)
}
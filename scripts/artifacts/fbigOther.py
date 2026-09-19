__artifacts_v2__ = {
    "fbigNcmec": {
        "name": "Facebook Instagram Returns - NCMEC Reports",
        "description": "NCMEC CyberTip report records from a Meta (Instagram) law enforcement return.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2023-06-30",
        "last_update_date": "2026-09-19",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "One row per record of the Ncmec Reports section of records.html and every preservation_N.html; Snapshot File names the file. "
                 "The section held no records on the return this was built against ('No responsive records'), so this artifact is unexercised and takes its field names from the provider's embedded definition: Time (when the cybertip was sent), CyberTip ID, and every other field of the record flattened into Details as 'label: value' lines, with any linked_media file the record names rendered in Media. "
                 "The definition lists, among others, Responsible Id, Upload Time, User Generated Filename, Upload IP, NCMEC File ID, Human Reviewed, Recipients, PhotoDNA Hash, Caption, Sharepoint, Messages (up to 3 above and below the reported content), Reported Text, Industry CSAM Classification and NCMEC Defined Product Annotations.",
        "paths": ('*/records.html', '*/preservation*.html', '*/linked_media/*'),
        "output_types": "standard",
        "artifact_icon": "alert-triangle",
    },
    "fbigOtherSections": {
        "name": "Facebook Instagram Returns - Other Sections",
        "description": "Any section of a Meta (Instagram) law enforcement return that holds records and has no dedicated artifact, one row per record, so nothing responsive is silently dropped.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-09-19",
        "last_update_date": "2026-09-19",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "Covers every section of records.html and every preservation_N.html that no dedicated artifact in this module set reads, whenever the section holds something other than the provider's 'No responsive records' placeholder. "
                 "Section is the provider's section name; Time is read from a Time, Timestamp, Date Created, Upload Time, Time Reported or Saved At field of the record when one parses as 'YYYY-MM-DD HH:MM:SS UTC'; Details holds every field of the record as 'label: value' lines, nested blocks flattened with their labels; Media renders any linked_media file the record names. A section whose value is plain text rather than records is reported one row per line of that text. "
                 "On the return this was built against every section that held records had a dedicated artifact, so this artifact produced no rows; it exists for the sections the provider's embedded definitions describe but that return did not exercise (live videos, notes, reported conversations, encrypted groups, the Threads app sections, community notes, quicksnaps, shared access, authenticity submissions, last location, and any section added to the format later). "
                 "The run log lists the sections that reached this artifact, so a section worth its own artifact can be promoted.",
        "paths": ('*/records.html', '*/preservation*.html', '*/linked_media/*'),
        "output_types": "standard",
        "artifact_icon": "list-details",
    },
}

from scripts.ilapfuncs import artifact_processor, logfunc
from scripts import meta_records as mr

TIME_LABELS = ('Time', 'Timestamp', 'Date Created', 'Upload Time', 'Time Reported', 'Saved At')

# Sections read by a dedicated artifact in fbigAccount, fbigSocial, fbigContent and fbigMessages.
COVERED = {
    'request_parameters', 'name', 'emails', 'vanity', 'registration_date', 'registration_ip',
    'account_end_date', 'account_read_receipts', 'phone_numbers', 'privacy_settings', 'popular_block',
    'gender', 'date_of_birth', 'website', 'about_me', 'linked_accounts', 'threads_registration_date',
    'profile_picture', 'name_changes', 'email_changes', 'vanity_changes', 'phone_number_changes',
    'password_changes', 'account_status_history', 'ip_addresses', 'devices', 'devices_info',
    'encrypted_connection_info', 'privacy_blocks', 'followers', 'following', 'incoming_follow_requests',
    'searches', 'photos', 'videos', 'archived_stories', 'comments', 'likes', 'comment_likes', 'saved_media',
    'unified_messages', 'ncmec_reports',
}


def _register(context, names):
    return mr.register_media(context, names)


def _time_of(record):
    for label in TIME_LABELS:
        when = mr.parse_ts(mr.text(record, label))
        if when:
            return when
    return ''


@artifact_processor
def fbigNcmec(context):
    data_list = []
    sources = mr.records_files(context.get_files_found())
    for path in sources:
        rec = mr.load(path)
        for record in rec.records('ncmec_reports'):
            names = mr.linked_media_files(record)
            details = mr.flatten([item for item in record if item.label not in ('Time', 'CyberTip ID')])
            data_list.append((_time_of(record), mr.text(record, 'CyberTip ID'), '\n'.join(details),
                              _register(context, names) or None, rec.name))
    data_headers = (('Time', 'datetime'), 'CyberTip ID', 'Details', ('Media', 'media'), 'Snapshot File')
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def fbigOtherSections(context):
    data_list = []
    sources = mr.records_files(context.get_files_found())
    reached = set()
    for path in sources:
        rec = mr.load(path)
        for section in rec.order:
            if section in COVERED or rec.is_empty(section):
                continue
            reached.add(section)
            records = rec.records(section)
            if records:
                for record in records:
                    names = mr.linked_media_files(record)
                    data_list.append((_time_of(record), section, '\n'.join(mr.flatten(record)),
                                      _register(context, names) or None, rec.name))
            else:
                for line in mr.lines(rec.text(section)):
                    data_list.append(('', section, line, None, rec.name))
    if reached:
        logfunc('Other Sections: sections with records and no dedicated artifact: ' + ', '.join(sorted(reached)))
    data_headers = (('Time', 'datetime'), 'Section', 'Details', ('Media', 'media'), 'Snapshot File')
    return data_headers, data_list, '\n'.join(sources)

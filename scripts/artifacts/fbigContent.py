__artifacts_v2__ = {
    "fbigPhotos": {
        "name": "Facebook Instagram Returns - Photos",
        "description": "Photos uploaded to the account, with the linked media rendered, from a Meta (Instagram) law enforcement return.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2023-07-01",
        "last_update_date": "2026-09-19",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "One row per record of the Photos section of records.html and every preservation_N.html; Snapshot File names the file. "
                 "The Image column renders the file the record's 'Linked Media File:' names inside the return's linked_media folder; Linked Media File keeps that name. "
                 "Column names are the provider's field labels. Per its embedded definition, Taken is when the image was uploaded, Status whether the image can be viewed, Source the device through which the photo was taken, Is Published whether it is currently on the profile, Shared to Platform whether it was shared to a different platform, Carousel Id the identifier a post gets when it contains more than one media, and Upload Ip the address (with source port after a colon, when available) associated with the upload. "
                 "Caption and Comments hold the nested caption and comment records flattened to 'label: value' lines; on the return this was built against both were empty on every photo. "
                 "Location Name, Location Address, Location External Id, Latitude and Longitude come from the record's Location block; all five were blank on every photo of the tested return, and a KML point is written only for a row carrying both coordinates, so the coordinate path is unexercised. Cross Post Id was blank, and Privacy Setting, Filter and Like Count each held one value, on every photo of the tested return; the columns stay because the provider defines them and the Likes and Saved Media sections of the same return carried varying values for the same fields.",
        "paths": ('*/records.html', '*/preservation*.html', '*/linked_media/*'),
        "output_types": "all",
        "artifact_icon": "photo",
    },
    "fbigVideos": {
        "name": "Facebook Instagram Returns - Videos",
        "description": "Videos uploaded by the account holder, with the linked media rendered where present, from a Meta (Instagram) law enforcement return.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2023-07-01",
        "last_update_date": "2026-09-19",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "One row per record of the Videos section of records.html and every preservation_N.html, read with the same field layout as the Photos artifact (the provider's embedded definitions list the same fields for both, plus Cross Post Id for a video shared from Instagram to Facebook). "
                 "The section held no records on the return this was built against ('No responsive records'), so this artifact is unexercised; its row layout was proven only on the Photos section.",
        "paths": ('*/records.html', '*/preservation*.html', '*/linked_media/*'),
        "output_types": "all",
        "artifact_icon": "video",
    },
    "fbigArchiveStories": {
        "name": "Facebook Instagram Returns - Archived Stories",
        "description": "Archived stories with their linked media, from a Meta (Instagram) law enforcement return.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2023-06-30",
        "last_update_date": "2026-09-19",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "One row per record of the Archived Stories section of records.html and every preservation_N.html; Snapshot File names the file. "
                 "Per the provider's embedded definition the section displays stories archived to the account, Time is when the media was uploaded, Owner the owner of the account and AI whether the content was created using generative AI. "
                 "Media renders the file named by the record's 'Linked Media File:' block; on the tested return every story record carried exactly one, a video or an image, and Privacy Setting held one value on every record. AI is reported as stored from the record's AI block. "
                 "The Unarchived Stories and Archived Quicksnap sections, which the definitions describe with the same fields, held no records on the tested return; they are reported by the Other Sections artifact when present.",
        "paths": ('*/records.html', '*/preservation*.html', '*/linked_media/*'),
        "output_types": "standard",
        "artifact_icon": "history",
    },
    "fbigPofilePic": {
        "name": "Facebook Instagram Returns - Profile Picture",
        "description": "The account's profile picture at the time of production, rendered from the linked media of a Meta (Instagram) law enforcement return.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2023-06-30",
        "last_update_date": "2026-09-19",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "One row per snapshot file (records.html and every preservation_N.html) whose Profile Picture section names a linked media file; per the provider's embedded definition it is the profile image at the time of production. "
                 "A snapshot whose section holds 'No responsive records' produces no row here: on the return this was built against one of three snapshots had no profile picture while the other two carried the same file.",
        "paths": ('*/records.html', '*/preservation*.html', '*/linked_media/*'),
        "output_types": "standard",
        "artifact_icon": "user-circle",
    },
    "fbigComments": {
        "name": "Facebook Instagram Returns - Comments",
        "description": "Comments the account holder left on images and videos, from a Meta (Instagram) law enforcement return.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2023-06-30",
        "last_update_date": "2026-09-19",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "One row per record of the Comments section of records.html and every preservation_N.html; Snapshot File names the file. "
                 "Per the provider's embedded definition the section displays comments left by the account holder on their own or other users' images and videos, Media Content Id identifies the media commented on, Media Owner is the account owner of that content, and Date Created is when the comment was published. "
                 "Owner and Media Owner are reported as stored ('username (Instagram: numeric id) [display name]' on the tested return). Status held one value on every comment of the tested return.",
        "paths": ('*/records.html', '*/preservation*.html'),
        "output_types": "standard",
        "artifact_icon": "message-circle",
    },
    "fbigLikes": {
        "name": "Facebook Instagram Returns - Likes",
        "description": "Media the account holder liked, from a Meta (Instagram) law enforcement return.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2023-06-30",
        "last_update_date": "2026-09-19",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "One row per record of the Likes section of records.html and every preservation_N.html; Snapshot File names the file. "
                 "Per the provider's embedded definition, Like Timestamp is when the account holder liked the post, Liked Post Owner Vanity the username of the post owner, Taken when the liked media was uploaded, Url the link to the media, and the remaining columns describe the liked media (Status, Source, Filter, Is Published, Shared to Platform, Upload Ip, Carousel Id, Cross Post Id) as stored. "
                 "Each snapshot file lists its own set of likes and the counts differed widely between the three snapshots of the tested return. Records split across the return's page breaks are rejoined before reporting; on the tested return the row count equalled the number of 'Like Timestamp' labels in the source text of each file.",
        "paths": ('*/records.html', '*/preservation*.html'),
        "output_types": "standard",
        "artifact_icon": "heart",
    },
    "fbigCommentLikes": {
        "name": "Facebook Instagram Returns - Comment Likes",
        "description": "Comments the account holder liked, from a Meta (Instagram) law enforcement return.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-09-19",
        "last_update_date": "2026-09-19",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "One row per Like block of the Comment Likes section of records.html and every preservation_N.html; Snapshot File names the file. "
                 "Per the provider's embedded definition, Time is when the account holder liked the comment, Comment Author Vanity the account holder that made the comment, and Post Url Of Comment Liked the URL of the comment liked. "
                 "The Comment Author Vanity field was empty on one of the five Like blocks of the tested return; the column is then blank.",
        "paths": ('*/records.html', '*/preservation*.html'),
        "output_types": "standard",
        "artifact_icon": "thumb-up",
    },
    "fbigSavedMedia": {
        "name": "Facebook Instagram Returns - Saved Media",
        "description": "Media listed in the Saved Media section of a Meta (Instagram) law enforcement return, one row per saved media item.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-09-19",
        "last_update_date": "2026-09-19",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "One row per Media block inside each Saved Media Item of the Saved Media section of records.html and every preservation_N.html; Snapshot File names the file. "
                 "Per the provider's embedded definition, Saved At is the date and time the media was saved, Taken when the media was uploaded, and the remaining columns describe the saved media as stored. "
                 "A Saved Media Item can hold several Media blocks (one item of the tested return held ten): they share the item's Saved At, and Saved Item Number counts the items in document order so the blocks of one item can be told apart. "
                 "The section carries no media files; Url links to the media on the platform and is reported as stored. Status, Filter and Is Published each held one value on every row of the tested return.",
        "paths": ('*/records.html', '*/preservation*.html'),
        "output_types": "standard",
        "artifact_icon": "bookmark",
    },
}

from scripts.ilapfuncs import artifact_processor
from scripts import meta_records as mr

POST_FIELDS = ('Id', 'Status', 'Privacy Setting', 'Url', 'Source', 'Filter', 'Is Published',
               'Shared to Platform', 'Upload Ip', 'Like Count', 'Owner', 'Carousel Id', 'Cross Post Id')


def _sources(context):
    return mr.records_files(context.get_files_found())


def _register(context, names):
    return mr.register_media(context, names)


def _post_row(context, record, rec):
    """Shared row layout for a photo or video record."""
    names = mr.linked_media_files(record)
    media = _register(context, names)
    location = {}
    for block in mr.sub(record, 'Location'):
        for item in block:
            if isinstance(item.value, str):
                location[item.label] = item.value
    caption = mr.field(record, 'Caption')
    comments = mr.field(record, 'Comments')

    def nested_text(item):
        if item is None:
            return ''
        if isinstance(item.value, list):
            return '\n'.join('\n'.join(mr.flatten(sub)) for sub in item.value)
        return item.value

    return ((mr.parse_ts(mr.text(record, 'Taken')), media or None)
            + tuple(mr.text(record, label) for label in POST_FIELDS)
            + (nested_text(caption), nested_text(comments),
               location.get('Name', ''), location.get('Address', ''), location.get('External Id', ''),
               location.get('Latitude', ''), location.get('Longitude', ''),
               '\n'.join(names), rec.name))


POST_HEADERS = (('Taken', 'datetime'), ('Media', 'media')) + POST_FIELDS + (
    'Caption', 'Comments', 'Location Name', 'Location Address', 'Location External Id',
    'Latitude', 'Longitude', 'Linked Media File', 'Snapshot File')


def _posts(context, section):
    data_list = []
    sources = _sources(context)
    for path in sources:
        rec = mr.load(path)
        for record in rec.records(section):
            data_list.append(_post_row(context, record, rec))
    return data_list, sources


@artifact_processor
def fbigPhotos(context):
    data_list, sources = _posts(context, 'photos')
    return POST_HEADERS, data_list, '\n'.join(sources)


@artifact_processor
def fbigVideos(context):
    data_list, sources = _posts(context, 'videos')
    return POST_HEADERS, data_list, '\n'.join(sources)


@artifact_processor
def fbigArchiveStories(context):
    data_list = []
    sources = _sources(context)
    for path in sources:
        rec = mr.load(path)
        for record in rec.records('archived_stories'):
            names = mr.linked_media_files(record)
            ai = '\n'.join(mr.text(block, 'Ai') for block in mr.sub(record, 'AI')) or mr.text(record, 'AI')
            data_list.append((mr.parse_ts(mr.text(record, 'Time')), _register(context, names) or None,
                              mr.text(record, 'Story Id'), mr.text(record, 'Privacy Setting'),
                              mr.text(record, 'Owner'), ai, '\n'.join(names), rec.name))
    data_headers = (('Time', 'datetime'), ('Media', 'media'), 'Story Id', 'Privacy Setting', 'Owner', 'AI',
                    'Linked Media File', 'Snapshot File')
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def fbigPofilePic(context):
    data_list = []
    sources = _sources(context)
    for path in sources:
        rec = mr.load(path)
        names = []
        for record in rec.records('profile_picture'):
            names.extend(mr.linked_media_files(record))
        for name in names:
            data_list.append((_register(context, [name]) or None, name, rec.name))
    data_headers = (('Media', 'media'), 'Linked Media File', 'Snapshot File')
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def fbigComments(context):
    data_list = []
    sources = _sources(context)
    for path in sources:
        rec = mr.load(path)
        for record in rec.records('comments'):
            data_list.append((mr.parse_ts(mr.text(record, 'Date Created')), mr.text(record, 'Text'),
                              mr.text(record, 'Id'), mr.text(record, 'Media Content Id'),
                              mr.text(record, 'Media Owner'), mr.text(record, 'Owner'),
                              mr.text(record, 'Status'), mr.text(record, 'Privacy Setting'), rec.name))
    data_headers = (('Date Created', 'datetime'), 'Text', 'Id', 'Media Content Id', 'Media Owner', 'Owner',
                    'Status', 'Privacy Setting', 'Snapshot File')
    return data_headers, data_list, '\n'.join(sources)


LIKE_FIELDS = ('Liked Post Owner Vanity', 'Url', 'Id', 'Status', 'Source', 'Filter', 'Is Published',
               'Shared to Platform', 'Upload Ip', 'Owner', 'Carousel Id', 'Cross Post Id')


@artifact_processor
def fbigLikes(context):
    data_list = []
    sources = _sources(context)
    for path in sources:
        rec = mr.load(path)
        for record in rec.records('likes'):
            data_list.append((mr.parse_ts(mr.text(record, 'Like Timestamp')),
                              mr.parse_ts(mr.text(record, 'Taken')))
                             + tuple(mr.text(record, label) for label in LIKE_FIELDS) + (rec.name,))
    data_headers = (('Like Timestamp', 'datetime'), ('Taken', 'datetime')) + LIKE_FIELDS + ('Snapshot File',)
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def fbigCommentLikes(context):
    data_list = []
    sources = _sources(context)
    for path in sources:
        rec = mr.load(path)
        for record in rec.records('comment_likes'):
            for like in mr.subs(record, 'Like'):
                for block in like.value:
                    data_list.append((mr.parse_ts(mr.text(block, 'Time')), mr.text(block, 'Comment Author Vanity'),
                                      mr.text(block, 'Post Url Of Comment Liked'), rec.name))
    data_headers = (('Time', 'datetime'), 'Comment Author Vanity', 'Post Url Of Comment Liked', 'Snapshot File')
    return data_headers, data_list, '\n'.join(sources)


SAVED_FIELDS = ('Id', 'Status', 'Url', 'Source', 'Filter', 'Is Published', 'Shared to Platform', 'Upload Ip',
                'Carousel Id', 'Cross Post Id')


@artifact_processor
def fbigSavedMedia(context):
    data_list = []
    sources = _sources(context)
    for path in sources:
        rec = mr.load(path)
        number = 0
        for record in rec.records('saved_media'):
            for item in mr.subs(record, 'Saved Media Item'):
                number += 1
                saved_at = ''
                blocks = []
                for group in item.value:
                    saved_at = saved_at or mr.text(group, 'Saved At')
                    blocks.extend(mr.subs(group, 'Media'))
                for block in blocks:
                    for media in block.value:
                        data_list.append((mr.parse_ts(saved_at), mr.parse_ts(mr.text(media, 'Taken')), number)
                                         + tuple(mr.text(media, label) for label in SAVED_FIELDS) + (rec.name,))
    data_headers = (('Saved At', 'datetime'), ('Taken', 'datetime'), 'Saved Item Number') + SAVED_FIELDS \
        + ('Snapshot File',)
    return data_headers, data_list, '\n'.join(sources)

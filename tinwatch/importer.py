import acoustid
import logging
import os
import utils

from beets.mediafile import MediaFile, FileTypeError, UnreadableFileError

from library import get_or_create, Song

#LOSSY_MEDIA_FORMATS = ["mp3", "aac", "ogg", "ape", "m4a", "asf", "wma"]
LOSSY_MEDIA_FORMATS = ["mp3", "ogg", "m4a"]
LOSSLESS_MEDIA_FORMATS = ["flac"]
MEDIA_FORMATS = LOSSY_MEDIA_FORMATS + LOSSLESS_MEDIA_FORMATS

CONTENT_TYPES = {
    'ogg': 'audio/ogg',
    'mp3': 'audio/mpeg',
    'm4a': 'audio/m4a',
}

SINGLE_ARTIST_THRESH = 0.25
VARIOUS_ARTISTS = u'Various Artists'

log = logging.getLogger(__name__)


class Importer(object):
    def set_common_album(self, items):
        changes = {}
        albumartist, freq = utils.plurality(
            [i.albumartist or i.artist for i in items]
        )
        if freq == len(items) or freq > 1 and float(freq) / len(items) >= SINGLE_ARTIST_THRESH:
            changes['albumartist'] = albumartist
            changes['comp'] = False
        else:
            changes['albumartist'] = VARIOUS_ARTISTS
            changes['comp'] = True

        for item in items:
            item.update(changes)

        return items

    def find_media(self, session, library):
        if not os.path.isdir(library.path):
            log.warning("Unable to find directory: '%s'", library.path)
            return
        for root, dirs, files in os.walk(library.path):
            if files:
                log.info("This is most likely an album: '%s'", root)
                items = [os.path.join(root, f) for f in files]
                media_files = []

                for item in items:
                    if any(item.lower().endswith('.' + x.lower()) for x in MEDIA_FORMATS):
                        song_path = os.path.join(root, item)
                        try:
                            media_files.append(MediaFile(song_path))
                        except (FileTypeError, UnreadableFileError):
                            log.warning("Unable to read media file '%s'", song_path)
                        except IOError:
                            log.warning("Unable to read media file '%s'", song_path)

                if media_files:
                    media_files = self.set_common_album(media_files)

                # album_metadata = self.album_metadata(media_files)

                for media_file in media_files:
                    media_dict = {
                        'artist': None,
                        'album': None,
                        'title': None,
                        'track': None,
                    }
                    duration, fingerprint = acoustid.fingerprint_file(media_file.path)

                    # m.format = MP3
                    # m.type = mp3

                    missing_metadata = False

                    # TODO: Make this all into a nice dictionary
                    # Set the artist
                    if media_file.albumartist:
                        media_dict['artist'] = media_file.albumartist
                    elif media_file.artist:
                        media_dict['artist'] = media_file.artist
                    else:
                        missing_metadata = True

                    # Set the album
                    if media_file.album:
                        media_dict['album'] = media_file.album
                    else:
                        media_dict['album'] = 'Unknown'
                        missing_metadata = True

                    # Set track information
                    if media_file.title:
                        media_dict['title'] = media_file.title
                    else:
                        missing_metadata = True

                    if media_file.track:
                        media_dict['track'] = media_file.track
                    else:
                        missing_metadata = True

                    if missing_metadata:
                        metadata = utils.metadata_from_filename(media_file.path)
                        if not media_dict['track']:
                            media_dict['track'] = metadata.get('track', 0)
                        if not media_dict['artist']:
                            media_dict['artist'] = metadata.get('artist', 'Unknown')
                        if not media_dict['title']:
                            media_dict['title'] = metadata.get('title', 'Unknown')

                    song = get_or_create(session, Song, path=os.path.dirname(media_file.path), filename=os.path.split(media_file.path)[1])
                    song.album = media_dict['album']
                    song.artist = media_dict['artist']
                    song.title = media_dict['title']
                    song.track = media_dict['track']
                    song.content_type = CONTENT_TYPES.get(media_file.type, 'mp3')
                    song.length = media_file.length
                    song.fingerprint = fingerprint

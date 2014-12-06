import acoustid
import logging
import os

from . import utils
from .models import Artist, Album, Song

from beets.mediafile import MediaFile, FileTypeError, UnreadableFileError


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

logging.basicConfig()
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

    # def album_metadata(self, items):
    #     if not items:
    #         return {}
    #
    #     likelies = {}
    #     consensus = {}
    #     fields = ['album', 'year']
    #     for field in fields:
    #         values = [item[field] for item in items if item]
    #         likelies[field], freq = utils.plurality(values)
    #         consensus[field] = (freq == len(values))
    #
    #     return likelies, consensus

    def find_media(self, library):
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
                    # TODO: This should be a celery job
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

                    artist, artist_created = Artist.objects.get_or_create(
                        name=media_dict['artist']
                    )
                    # TODO: Should only need to do this once per folder/album
                    album, album_created = Album.objects.get_or_create(
                        artist=artist,
                        title=media_dict['album']
                    )
                    song, song_created = Song.objects.get_or_create(
                        path=os.path.dirname(media_file.path),
                        filename=os.path.split(media_file.path)[1],
                        defaults={
                            'album': album,
                            'artist': artist,
                            'title': media_dict['title'],
                            'track': media_dict['track'],
                            'content_type': CONTENT_TYPES.get(media_file.type, 'mp3'),
                            'length': media_file.length,
                            'fingerprint': fingerprint,
                        }
                    )

                    library.songs.add(song)

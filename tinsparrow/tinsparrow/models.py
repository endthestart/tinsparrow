import os

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mutagen.mp3 import MP3


TYPES = {
    'mp3':  'MP3',
    # 'aac':  'AAC',
    # 'alac':  'ALAC',
    # 'ogg':  'OGG',
    # 'opus': 'Opus',
    # 'flac': 'FLAC',
    # 'ape':  'APE',
    # 'wv':   'WavPack',
    # 'mpc':  'Musepack',
    # 'asf':  'Windows Media',
}


class Artist(models.Model):
    name = models.CharField(
        _('name'),
        max_length=255,
        default='',
        blank=True,
        help_text=_("The name of the artist."),
    )

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = _("artist")
        verbose_name_plural = _("artists")


class Album(models.Model):
    artist = models.ForeignKey(
        Artist,
        blank=True,
        null=True,
        related_name='artist',
    )
    title = models.CharField(
        _('title'),
        max_length=255,
        default='',
        blank=True,
        help_text=_("The title of the album."),
    )
    year = models.DateField(
        _('year'),

    )

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = _("album")
        verbose_name_plural = _("albums")


class Library(models.Model):
    name = models.CharField(
        _('name'),
        max_length=255,
        help_text=_("The name of the library."),
    )
    path = models.CharField(
        _('path'),
        help_text=_("The absolute path of the library."),
    )

    def find_media(self):
        for root, dirs, files in os.walk(self.path):
            path = os.path.relpath(root, self.path).split(os.sep)
            print "Adding files from: {}".format(os.path.basename(root))
            for this_file in files:
                if this_file.endswith('.mp3'):
                    print "Adding this file: {}".format(this_file)
                    song_file = MP3(os.path.join(root, this_file))
                    print song_file.info.length, song_file.info.bitrate
                else:
                    print "Not Adding this file: {}".format(os.path.join(root, this_file))


    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("library")
        verbose_name_plural = _("libraries")


class LibraryFile(models.Model):
    library = models.ForeignKey(
        Library,
        related_name='library',
    )
    path = models.CharField(
        _('path'),
        max_length=255,
        default='',
        blank=True,
        help_text=_("The path of that contains the file."),
    )
    name = models.CharField(
        _('name'),
        max_length=255,
        default='',
        blank=True,
        help_text=_("The name of the file."),
    )
    size = models.IntegerField(
        _('size'),
        help_text=_("The size of the file in bytes.")
    )

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = _("file")
        verbose_name_plural = _("files")

# class SongFile(File):
#     length,
#     bitrate,
#     channels,
#     sample_rate,
#     leveling,
#     get_artist_from_file()
#     get_album_from_file()

class Song(models.Model):
    album = models.ForeignKey(
        Album,
        _('album'),
        related_name='album',
    )
    file = models.ForeignKey(
        LibraryFile,
        blank=True,
        null=True,
        related_name='file',
    )
    title = models.CharField(
        _('title'),
        max_length=255,
        default='',
        blank=True,
        help_text=_("The title of the song."),
    )

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('title', )
        verbose_name = _('song')
        verbose_name_plural = _('songs')
import os

from django.db import models
from django.utils.translation import ugettext_lazy as _

from beets.mediafile import MediaFile
from mutagen.mp3 import MP3


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
                    song_file = MediaFile(os.path.join(root, this_file))
                    artist, artist_created = Artist.objects.get_or_create(name=song_file.artist)
                    album, album_created = Album.objects.get_or_create(artist=artist, title=song_file.album, year=song_file.year)
                    song, song_created = Song.objects.get_or_create(path=os.path.join(root, this_file), defaults={'album': album})
                else:
                    print "Not Adding this file: {}".format(os.path.join(root, this_file))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("library")
        verbose_name_plural = _("libraries")


class Song(models.Model):
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
    filename = models.CharField(
        _('name'),
        max_length=255,
        default='',
        blank=True,
        help_text=_("The name of the file."),
    )
    album = models.ForeignKey(
        Album,
        _('album'),
        related_name='album',
    )
    title = models.CharField(
        _('title'),
        max_length=255,
        default='',
        blank=True,
        help_text=_("The title of the song."),
    )
    size = models.IntegerField(
        _('size'),
        default=0,
        help_text=_("The size of the file in bytes.")
    )

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('title', )
        verbose_name = _('song')
        verbose_name_plural = _('songs')
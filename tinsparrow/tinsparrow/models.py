import logging

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

log = logging.getLogger(__name__)

USER_MODULE_PATH = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Artist(models.Model):
    name = models.CharField(
        _('name'),
        max_length=255,
        unique=True,
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
        related_name='albums',
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
        null=True,
        blank=True,
        help_text=_("The year the album was produced."),
    )

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = _("album")
        verbose_name_plural = _("albums")


class Song(models.Model):
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
        blank=True,
        null=True,
        related_name='songs',
    )
    artist = models.ForeignKey(
        Artist,
        blank=True,
        null=True,
        related_name='songs',
    )
    title = models.CharField(
        _('title'),
        max_length=255,
        default='',
        blank=True,
        help_text=_("The title of the song."),
    )
    track = models.PositiveIntegerField(
        _('track'),
        default='0',
        help_text=_("The track of the song within the album."),
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
        unique_together = ('path', 'filename')


class Library(models.Model):
    user = models.ForeignKey(
        USER_MODULE_PATH,
        blank=True,
        null=True,
    )
    name = models.CharField(
        _('name'),
        max_length=255,
        help_text=_("The name of the library."),
    )
    path = models.CharField(
        _('path'),
        max_length=255,
        help_text=_("The absolute path of the library."),
    )
    songs = models.ManyToManyField(
        Song,
        blank=True,
    )

    @property
    def albums(self):
        return Album.objects.filter(songs__in=self.songs).distinct()

    @property
    def artists(self):
        return Artist.objects.filter(songs__in=self.songs).distinct()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("library")
        verbose_name_plural = _("libraries")

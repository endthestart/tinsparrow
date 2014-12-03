import logging

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
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
    fingerprint = models.TextField(
        _('fingerprint'),
        blank=True,
        null=True,
        help_text=_("The AcoustID fingerprint of the audio file."),
    )
    artist = models.ForeignKey(
        Artist,
        blank=True,
        null=True,
        related_name='songs',
    )
    album = models.ForeignKey(
        Album,
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
    content_type = models.CharField(
        _('content type'),
        max_length=255,
        default='',
        blank=True,
        help_text=_("The content type of the media file, such as 'audio/m4a'."),
    )
    length = models.FloatField(
        _('length'),
        default=0,
        help_text=_("The length of the song in seconds (stores as a float)."),
    )

    def get_absolute_url(self):
        return reverse('song_file', kwargs={'song_id': self.id, })

    def url(self):
        from rest_framework.reverse import reverse as drf_reverse
        return drf_reverse('song_file', kwargs={'song_id': self.id, })

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('title', )
        verbose_name = _('song')
        verbose_name_plural = _('songs')
        unique_together = ('path', 'filename')


class Library(models.Model):
    user = models.OneToOneField(
        USER_MODULE_PATH,
        null=True,
        blank=True,
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

    @property
    def name(self):
        return "{}'s Library".format(self.user)

    @property
    def path(self):
        return "{}{}".format(settings.LIBRARY_PATH, self.user)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("library")
        verbose_name_plural = _("libraries")


class Queue(models.Model):
    user = models.ForeignKey(
        USER_MODULE_PATH
    )
    songs = models.ManyToManyField(
        Song,
        through='QueueSong',
    )

    def get_songs(self):
        return [queuesong.song for queuesong in self.queuesong_set.all()]

    def __unicode__(self):
        return "{}'s Queue".format(self.user.username)


class QueueSong(models.Model):
    queue = models.ForeignKey(
        Queue,
    )
    song = models.ForeignKey(
        Song,
    )
    order = models.PositiveIntegerField(
        _('order'),
        default=0,
        help_text=_("The order of the song in the queue"),
    )

    def __unicode__(self):
        return "{} - {}".format(self.queue, self.song)

    class Meta:
        ordering = ('order', )
        verbose_name = _("queue song")
        verbose_name_plural = _("queue songs")


def create_library(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        library, created = Library.objects.get_or_create(user=user)
        library.save()

post_save.connect(create_library, sender=USER_MODULE_PATH)

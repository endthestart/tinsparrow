from django.db import models
from django.utils.translation import ugettext_lazy as _


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


class File(models.Model):
    path = models.CharField(
        _('path'),
        max_length=1000,
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


class SongFile(File):
    length,
    bitrate,
    channels,
    sample_rate,
    leveling,



class Song(models.Model):
    album = models.ForeignKey(
        _('album'),
    )
    file = models.ForeignKey(
        File,
        blank=True,
        null=True,
        related_name='file',
    )

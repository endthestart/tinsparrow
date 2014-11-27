# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tinsparrow', '0002_queue'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='content_type',
            field=models.CharField(default=b'', help_text="The content type of the media file, such as 'audio/m4a'.", max_length=255, verbose_name='content type', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='length',
            field=models.FloatField(default=0, help_text='The length of the song in seconds (stores as a float).', verbose_name='length'),
            preserve_default=True,
        ),
    ]

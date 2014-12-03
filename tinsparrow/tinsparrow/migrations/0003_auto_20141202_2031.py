# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tinsparrow', '0002_song_fingerprint'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='library',
            name='name',
        ),
        migrations.RemoveField(
            model_name='library',
            name='path',
        ),
        migrations.AlterField(
            model_name='library',
            name='user',
            field=models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]

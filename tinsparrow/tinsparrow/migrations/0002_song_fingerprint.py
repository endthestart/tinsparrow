# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tinsparrow', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='fingerprint',
            field=models.TextField(help_text='The AcoustID fingerprint of the audio file.', null=True, verbose_name='fingerprint', blank=True),
            preserve_default=True,
        ),
    ]

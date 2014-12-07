# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tinsparrow', '0004_auto_20141206_1556'),
    ]

    operations = [
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('songs', models.ManyToManyField(to='tinsparrow.Song')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

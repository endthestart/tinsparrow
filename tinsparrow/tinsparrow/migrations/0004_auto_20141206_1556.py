# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tinsparrow', '0003_auto_20141202_2031'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLibrary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('songs', models.ManyToManyField(to='tinsparrow.Song', blank=True)),
                ('user', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user library',
                'verbose_name_plural': 'user libraries',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='library',
            name='songs',
        ),
        migrations.RemoveField(
            model_name='library',
            name='user',
        ),
        migrations.DeleteModel(
            name='Library',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', help_text='The title of the album.', max_length=255, verbose_name='title', blank=True)),
                ('year', models.DateField(help_text='The year the album was produced.', null=True, verbose_name='year', blank=True)),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'album',
                'verbose_name_plural': 'albums',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='The name of the artist.', unique=True, max_length=255, verbose_name='name')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'artist',
                'verbose_name_plural': 'artists',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='The name of the library.', max_length=255, verbose_name='name')),
                ('path', models.CharField(help_text='The absolute path of the library.', max_length=255, verbose_name='path')),
            ],
            options={
                'verbose_name': 'library',
                'verbose_name_plural': 'libraries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QueueSong',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=0, help_text='The order of the song in the queue', verbose_name='order')),
                ('queue', models.ForeignKey(to='tinsparrow.Queue')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'queue song',
                'verbose_name_plural': 'queue songs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(default=b'', help_text='The path of that contains the file.', max_length=255, verbose_name='path', blank=True)),
                ('filename', models.CharField(default=b'', help_text='The name of the file.', max_length=255, verbose_name='name', blank=True)),
                ('title', models.CharField(default=b'', help_text='The title of the song.', max_length=255, verbose_name='title', blank=True)),
                ('track', models.PositiveIntegerField(default=b'0', help_text='The track of the song within the album.', verbose_name='track')),
                ('size', models.IntegerField(default=0, help_text='The size of the file in bytes.', verbose_name='size')),
                ('content_type', models.CharField(default=b'', help_text="The content type of the media file, such as 'audio/m4a'.", max_length=255, verbose_name='content type', blank=True)),
                ('length', models.FloatField(default=0, help_text='The length of the song in seconds (stores as a float).', verbose_name='length')),
                ('album', models.ForeignKey(related_name='songs', blank=True, to='tinsparrow.Album', null=True)),
                ('artist', models.ForeignKey(related_name='songs', blank=True, to='tinsparrow.Artist', null=True)),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'song',
                'verbose_name_plural': 'songs',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='song',
            unique_together=set([('path', 'filename')]),
        ),
        migrations.AddField(
            model_name='queuesong',
            name='song',
            field=models.ForeignKey(to='tinsparrow.Song'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='queue',
            name='songs',
            field=models.ManyToManyField(to='tinsparrow.Song', through='tinsparrow.QueueSong'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='queue',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='library',
            name='songs',
            field=models.ManyToManyField(to='tinsparrow.Song', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='library',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(related_name='albums', blank=True, to='tinsparrow.Artist', null=True),
            preserve_default=True,
        ),
    ]

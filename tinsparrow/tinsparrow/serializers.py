from .models import Artist, Album, Song, Queue
from rest_framework import serializers


class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    albums = serializers.HyperlinkedIdentityField('albums', view_name='artistalbum-list')
    songs = serializers.HyperlinkedIdentityField('songs', view_name='artistsong-list')

    class Meta:
        model = Artist
        fields = ('id', 'name', 'albums', 'songs', )


class AlbumSerializer(serializers.ModelSerializer):
    songs = serializers.HyperlinkedIdentityField('songs', view_name='albumsong-list')

    class Meta:
        model = Album
        fields = ('id', 'artist', 'title', 'songs', )


class SongSerializer(serializers.ModelSerializer):
    #artist = ArtistSerializer(required=False)
    #album = AlbumSerializer(required=False)

    class Meta:
        model = Song
        fields = ('id', 'artist', 'album', 'title', )


class QueueSerializer(serializers.ModelSerializer):
    # songs = serializers.HyperlinkedIdentityField('songs', view_name='queuesong-list')

    class Meta:
        model = Queue
        fields = ('id', 'songs', )







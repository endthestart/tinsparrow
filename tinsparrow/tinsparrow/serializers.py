from .models import Library, Artist, Album, Song
from rest_framework import serializers


class SongSerializer(serializers.HyperlinkedModelSerializer):
    artist = serializers.Field(source='artist.name')
    album = serializers.Field(source='album.title')
    artist_url = serializers.Field(source='artist')
    class Meta:
        model = Song
        fields = ('url', 'artist', 'album', 'artist_url', 'title', )


class AlbumSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Album
        fields = ('url', 'artist', 'title', 'songs', 'tracks', )


class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artist
        fields = ('url', 'name', 'albums', 'songs', )

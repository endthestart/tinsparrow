from rest_framework.reverse import reverse
from rest_framework import serializers

from .models import Artist, Album, Song


class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'name', 'albums', 'songs', )


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('id', 'artist', 'title', 'songs', )


class SongSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer()
    album = AlbumSerializer()
    song_url = serializers.SerializerMethodField()

    def get_song_url(self, obj):
        return reverse('song_file', args=[obj.id], request=self.context.get('request', None))

    class Meta:
        model = Song
        fields = ('id', 'fingerprint', 'artist', 'album', 'title', 'length', 'song_url', 'content_type', )


class LibrarySerializer(serializers.ModelSerializer):
    artist = ArtistSerializer()
    album = AlbumSerializer()
    song_url = serializers.SerializerMethodField('get_song_url')

    def get_song_url(self, obj):
        return reverse('song_file', args=[obj.id], request=self.context.get('request', None))

    class Meta:
        model = Song
        fields = ('id', 'fingerprint', 'artist_id', 'artist', 'album_id', 'album', 'title', 'length', 'song_url',
                  'content_type', )

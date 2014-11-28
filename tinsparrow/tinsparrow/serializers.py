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
    artist_id = serializers.PrimaryKeyRelatedField('artist')
    artist = serializers.RelatedField('artist')
    album_id = serializers.PrimaryKeyRelatedField('album')
    album = serializers.RelatedField('album')
    song_url = serializers.SerializerMethodField('get_song_url')

    def get_song_url(self, obj):
        from rest_framework.reverse import reverse
        return reverse('song_file', args=[obj.id], request=self.context.get('request', None))

    class Meta:
        model = Song
        fields = ('id', 'artist_id', 'artist', 'album_id', 'album', 'title', 'length', 'song_url', 'content_type', )

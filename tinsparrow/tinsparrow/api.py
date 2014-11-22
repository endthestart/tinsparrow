from rest_framework import generics, permissions

from .serializers import ArtistSerializer, AlbumSerializer, SongSerializer
from .models import Artist, Album, Song


class ArtistList(generics.ListCreateAPIView):
    model = Artist
    serializer_class = ArtistSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class ArtistDetail(generics.RetrieveAPIView):
    model = Artist
    serializer_class = ArtistSerializer


class AlbumList(generics.ListCreateAPIView):
    model = Album
    serializer_class = AlbumSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class AlbumDetail(generics.RetrieveAPIView):
    model = Artist
    serializer_class = AlbumSerializer


class SongList(generics.ListCreateAPIView):
    model = Song
    serializer_class = SongSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class SongDetail(generics.RetrieveAPIView):
    model = Song
    serializer_class = SongSerializer


class ArtistAlbumList(generics.ListAPIView):
    model = Album
    serializer_class = AlbumSerializer

    def get_queryset(self):
        queryset = super(ArtistAlbumList, self).get_queryset()
        return queryset.filter(artist=self.kwargs.get('pk'))


class ArtistSongList(generics.ListAPIView):
    model = Song
    serializer_class = SongSerializer

    def get_queryset(self):
        queryset = super(ArtistSongList, self).get_queryset()
        import pdb; pdb.set_trace()
        return queryset.filter(artist=self.kwargs.get('pk'))


class AlbumSongList(generics.ListAPIView):
    model = Song
    serializer_class = SongSerializer

    def get_queryset(self):
        queryset = super(AlbumSongList, self).get_queryset()
        return queryset.filter(album=self.kwargs.get('pk'))
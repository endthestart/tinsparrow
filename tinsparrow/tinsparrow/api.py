from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .serializers import ArtistSerializer, AlbumSerializer, SongSerializer
from .models import Artist, Album, Song, Queue


class DefaultsMixin(object):

    permission_classes = [
        permissions.IsAuthenticated
    ]

    paginate_by = 10000
    paginate_by_param = 'page_size'
    max_paginate_by = 10000


@api_view(('GET', ))
def api_root(request, format=None):
    return Response({
        'artists': reverse('artist-list', request=request, format=format),
        'albums': reverse('album-list', request=request, format=format),
        'songs': reverse('song-list', request=request, format=format),
        'queue': reverse('queue-list', request=request, format=format)
    })


class ArtistList(DefaultsMixin, generics.ListAPIView):
    model = Artist
    serializer_class = ArtistSerializer


class ArtistDetail(DefaultsMixin, generics.RetrieveAPIView):
    model = Artist
    serializer_class = ArtistSerializer


class AlbumList(DefaultsMixin, generics.ListAPIView):
    model = Album
    serializer_class = AlbumSerializer


class AlbumDetail(DefaultsMixin, generics.RetrieveAPIView):
    model = Album
    serializer_class = AlbumSerializer


class SongList(DefaultsMixin, generics.ListAPIView):
    model = Song
    serializer_class = SongSerializer
    #
    # def list(self, request, *args, **kwargs):
    #     queryset = Song.objects.all()
    #     serializer = SongSerializer(queryset, many=True, context={'request': self.request})
    #     return Response(serializer.data)


class SongDetail(DefaultsMixin, generics.RetrieveAPIView):
    model = Song
    serializer_class = SongSerializer


class ArtistAlbumList(DefaultsMixin, generics.ListAPIView):
    model = Album
    serializer_class = AlbumSerializer

    def get_queryset(self):
        queryset = super(ArtistAlbumList, self).get_queryset()
        return queryset.filter(artist=self.kwargs.get('pk'))


class ArtistSongList(DefaultsMixin, generics.ListAPIView):
    model = Song
    serializer_class = SongSerializer

    def get_queryset(self):
        queryset = super(ArtistSongList, self).get_queryset()
        return queryset.filter(artist=self.kwargs.get('pk'))


class AlbumSongList(DefaultsMixin, generics.ListAPIView):
    model = Song
    serializer_class = SongSerializer

    def get_queryset(self):
        queryset = super(AlbumSongList, self).get_queryset()
        return queryset.filter(album=self.kwargs.get('pk'))


class QueueList(DefaultsMixin, generics.ListAPIView):
    model = Queue
    serializer_class = SongSerializer

    def get_queryset(self):
        user = self.request.user
        # Ensure the Queue exists ... middleware?
        queue, created = Queue.objects.get_or_create(user=user)
        return Song.objects.filter(queue=queue)

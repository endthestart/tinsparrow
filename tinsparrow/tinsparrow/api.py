import json
import django_filters

from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .serializers import ArtistSerializer, AlbumSerializer, SongSerializer
from .models import Artist, Album, Library, UserLibrary, Song, Queue, QueueSong


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
        'queue': reverse('queue-list', request=request, format=format),
        'library': reverse('library-list', request=request, format=format)
    })


@api_view(('POST', ))
def song_upload(request, format=None):
    if request.method == "POST":
        return Response({
            'status': "failure"
        })


class ArtistList(DefaultsMixin, generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class ArtistDetail(DefaultsMixin, generics.RetrieveAPIView):
    model = Artist
    serializer_class = ArtistSerializer


class AlbumList(DefaultsMixin, generics.ListAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class AlbumDetail(DefaultsMixin, generics.RetrieveAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class SongFilter(django_filters.FilterSet):
    artist = django_filters.CharFilter(name="artist__name")
    album = django_filters.CharFilter(name="album__name")

    class Meta:
        model = Song
        fields = ['fingerprint', 'artist', 'album', 'title']


class SongList(DefaultsMixin, generics.ListAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filter_class = SongFilter


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


class LibraryList(DefaultsMixin, generics.ListCreateAPIView):
    model = Song
    serializer_class = SongSerializer

    def get_queryset(self):
        user = self.request.user
        library = UserLibrary.objects.get(user=user)
        return library.songs.all()

    def post(self, request, *args, **kwargs):
        user = self.request.user
        song_id = int(request.data.get('id'))
        # TODO: make this less prone to failure if for some reason library does not exist
        # TODO: Add fixture that loads the Library
        library = Library.objects.get()
        user_library = UserLibrary.objects.get(user=user)
        print("Attempting to load song with ID: {}".format(song_id))
        try:
            song = library.songs.get(id=song_id)
            user_library.songs.add(song)
        except Song.DoesNotExist:
            # TODO: Add logging
            print("attempted adding song that doesn't exist")
        return Response({
            'results': [song_id]
        }, status=status.HTTP_201_CREATED, headers={})


class QueueList(DefaultsMixin, generics.ListCreateAPIView):
    model = Song
    serializer_class = SongSerializer

    def get_queryset(self):
        user = self.request.user
        # TODO: Ensure the Queue exists ... middleware?
        queue, created = Queue.objects.get_or_create(user=user)
        return queue.get_songs()

    def post(self, request, *args, **kwargs):
        user = self.request.user
        queue, created = Queue.objects.get_or_create(user=user)
        song_json = json.loads(self.request.POST.get('song_list', None))
        if song_json:
            queue.songs.clear()
            song_order = 0
            for song_data in song_json:
                try:
                    song = Song.objects.get(id=song_data.get('id'))
                    queue_song = QueueSong(queue=queue, song=song, order=song_order)
                    queue_song.save()
                    song_order += 1
                except Song.DoesNotExist:
                    # TODO: Unused, don't know what to do
                    song = None
        return Response(song_json, status=status.HTTP_201_CREATED, headers={})

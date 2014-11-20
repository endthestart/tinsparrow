import os

from django import http
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from rest_framework import viewsets

from .models import Artist, Album, Queue, Song
from .serializers import ArtistSerializer, AlbumSerializer, SongSerializer


def songfile(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    song_data = open(os.path.join(song.path, song.filename)).read()
    return http.HttpResponse(song_data, content_type='audio/m4a')


class HomeView(TemplateView):
    template_name = "tinsparrow/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['queue'] = Queue.objects.get(user=self.request.user)
        return context


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


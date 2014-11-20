import os

from django import http
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView


from .models import Artist, Album, Library, Queue, Song


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


class LibraryView(TemplateView):
    template_name = "tinsparrow/library.html"

    def get_context_data(self, **kwargs):
        context = super(LibraryView, self).get_context_data(**kwargs)
        libraries = Library.objects.all()
        objects = Artist.objects.filter(library__in=libraries)
        context['objects'] = objects
        context['type'] = 'artists'
        return context


class LibraryAlbumsView(LibraryView):
    def get_context_data(self, **kwargs):
        context = super(LibraryView, self).get_context_data(**kwargs)
        libraries = Library.objects.all()
        objects = Album.objects.filter(library__in=libraries)
        context['objects'] = objects
        context['type'] = 'albums'


class ArtistView(TemplateView):
    template_name = "tinsparrow/library.html"

    def get_context_data(self, **kwargs):
        context = super(LibraryView, self).get_context_data(**kwargs)
        libraries = Library.objects.all()
        artists = Artist.objects.filter(library__in=libraries)
        context['artists'] = artists
        return context


class AlbumView(TemplateView):
    template_name = "tinsparrow/library.html"

    def get_context_data(self, **kwargs):
        context = super(LibraryView, self).get_context_data(**kwargs)
        libraries = Library.objects.all()
        artists = Artist.objects.filter(library__in=libraries)
        context['artists'] = artists
        return context

from django.views.generic import TemplateView

from .models import Artist, Album, Song, Library


class HomeView(TemplateView):
    template_name = "tinsparrow/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
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
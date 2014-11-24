import os

from django import http
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from .models import Song


def songfile(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    song_data = open(os.path.join(song.path, song.filename)).read()
    return http.HttpResponse(song_data, content_type='audio/m4a')


class HomeView(TemplateView):
    template_name = "tinsparrow/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        # context['queue'] = Queue.objects.get_or_create(user=self.request.user)
        return context


class LibraryView(TemplateView):
    template_name = "tinsparrow/library.html"

    def get_context_data(self, **kwargs):
        context = super(LibraryView, self).get_context_data(**kwargs)
        return context

class LayoutView(TemplateView):
    template_name = "tinsparrow/layout.html"

    def get_context_data(self, **kwargs):
        context = super(LayoutView, self).get_context_data(**kwargs)
        return context
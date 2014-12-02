import os

from django.contrib import messages
from django.contrib.auth import logout as logout_user
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from django import http
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from .models import Song
from .forms import LoginForm


def songfile(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    song_data = open(os.path.join(song.path, song.filename)).read()
    return http.HttpResponse(song_data, content_type=song.content_type)


def login(request, template_name='login.html'):
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.login(request):
            messages.success(request, "You have successfully logged in.")
            return redirect(request.POST.get('next', '/'))
        else:
            messages.error(request, "Your username and password do not match.")
    else:
        form = LoginForm()
    return render_to_response(template_name, {'form': form, }, RequestContext(request))


def logout(request):
    logout_user(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')


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

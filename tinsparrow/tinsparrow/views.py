from django.views.generic import TemplateView

from rest_framework import viewsets

from .models import Artist, Album, Song, Library
from .serializers import ArtistSerializer


class HomeView(TemplateView):
    template_name = "tinsparrow/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
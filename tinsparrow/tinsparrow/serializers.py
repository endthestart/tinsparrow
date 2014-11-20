from .models import Library, Artist, Album, Song
from rest_framework import serializers


class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artist
        fields = ('name', )

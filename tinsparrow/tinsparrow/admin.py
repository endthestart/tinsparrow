from django.contrib import admin
from .models import UserLibrary, Artist, Album, Song, Queue

admin.site.register(UserLibrary)
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Queue)

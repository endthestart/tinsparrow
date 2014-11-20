from django.conf.urls import patterns, include, url
from django.conf import settings

from .views import HomeView, LibraryView, LibraryAlbumsView, ArtistView, AlbumView, songfile

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^library/', LibraryView.as_view(), name='library'),
    url(r'^library/artists', LibraryView.as_view(), name='library_artists'),
    url(r'^library/albums', LibraryAlbumsView.as_view(), name='library_albums'),
    url(r'^library/songs', LibraryView.as_view(), name='library_songs'),
    url(r'^library/artist/(?P<artist_id>\d+)/', ArtistView.as_view(), name='artist'),
    url(r'^library/album/(?P<album_id>\d+)/', AlbumView.as_view(), name='album'),

    url(r'^song/(?P<song_id>\d+)', songfile, name='tinsparrow_song_file'),

    url(r'^admin/', include(admin.site.urls)),

)

# Uncomment the next line to serve media files in dev.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
    )

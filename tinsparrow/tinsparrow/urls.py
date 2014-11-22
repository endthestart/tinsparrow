from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from .views import  LibraryView, songfile, HomeView
from .api import ArtistList, ArtistDetail
from .api import AlbumList, AlbumDetail, ArtistAlbumList
from .api import SongList, SongDetail, ArtistSongList, AlbumSongList

artist_urls = patterns(
    '',
    url(r'^/(?P<pk>\d+)/albums/$', ArtistAlbumList.as_view(), name='artistalbum-list'),
    url(r'^/(?P<pk>\d+)/songs/$', ArtistSongList.as_view(), name='artistsong-list'),
    url(r'^/(?P<pk>\d+)/$', ArtistDetail.as_view(), name='artist-detail'),
    url(r'^/$', ArtistList.as_view(), name='artist-list'),
)

album_urls = patterns(
    '',
    url(r'^/(?P<pk>\d+)/songs/$', AlbumSongList.as_view(), name='albumsong-list'),
    url(r'^/(?P<pk>\d+)/$', AlbumDetail.as_view(), name='album-detail'),
    url(r'^/$', AlbumList.as_view(), name='album-list'),
)

song_urls = patterns(
    '',
    url(r'^/(?P<pk>\d+)/$', SongDetail.as_view(), name='song-detail'),
    url(r'^/$', SongList.as_view(), name='song-list'),
)

urlpatterns = patterns(
    '',
    url(r'^api/artists', include(artist_urls)),
    url(r'^api/albums', include(album_urls)),
    url(r'^api/songs', include(song_urls)),
    url(r'^$', HomeView.as_view(), name='tinsparrow_home'),
    url(r'^library/', LibraryView.as_view(), name='library'),
    url(r'^api-auth/', include('rest_framework.urls')),
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

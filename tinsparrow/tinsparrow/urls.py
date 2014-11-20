from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from rest_framework import routers
from .views import ArtistViewSet, AlbumViewSet, SongViewSet, songfile, HomeView

router = routers.DefaultRouter()
router.register(r'artists', ArtistViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'songs', SongViewSet)


urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^song/(?P<song_id>\d+)', songfile, name='tinsparrow_song_file'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'', HomeView.as_view(), name='tinsparrow_home'),
)

# Uncomment the next line to serve media files in dev.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
    )

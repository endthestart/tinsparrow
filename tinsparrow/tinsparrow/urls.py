from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'artists', views.ArtistViewSet)


urlpatterns = patterns(
    '',
    #url(r'^$', HomeView.as_view(), name='home'),
    url(r'^api/$', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^admin/', include(admin.site.urls)),

)

# Uncomment the next line to serve media files in dev.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
    )

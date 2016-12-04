from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

from llc.views import HomeView

urlpatterns = patterns(
    'llc.views',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^papers/', include('paper.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^ratings/', include('ratings.urls')),
    url(r'^suggestions/', include('suggestions.urls')),
    url(r'^qrtreader/', include('qrtreader.urls')),
    (r'^accounts/', include('userena.urls')),
)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    url(r'^pages/', include('django.contrib.flatpages.urls')),
]

urlpatterns += staticfiles_urlpatterns()

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required

urlpatterns = patterns(
    'ratings.views',
    url(r'^download_ratings/$', 'getRatings', name='get_ratings'),
)



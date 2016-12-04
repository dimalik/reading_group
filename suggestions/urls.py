from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from suggestions.views import SuggestionsHome, SuggestionCreate

urlpatterns = patterns(
    'suggestions.views',
    url(r'^$', login_required(SuggestionsHome.as_view()), name='suggestions_home'),
    url(r'^create/$', login_required(SuggestionCreate.as_view()), name="suggestions_create"),
    url(r'^download/(?P<pid>\d+)/$', 'download_pdf', name="download_suggestion"),
    url(r'^edit_doi/(?P<pid>\d+)/$', 'edit_doi', name="edit_doi")
)

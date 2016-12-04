from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required




from paper.views import PapersHome, PaperDetail, SessionHome
from blog.views import BlogPostCreate

urlpatterns = patterns(
    'paper.views',
    # url(r'^$', login_required(PapersHome.as_view()), name='papers_home'),
    # url(r'^$', login_required(SessionHome.as_view()), name='papers_home'),
    url(r'^$', SessionHome.as_view(), name='papers_home'),
    url(r'^download/(?P<pid>\d+)/$', 'download_pdf', name='download_pdf'),
    url(r'^(?P<pk>\d+)/$', login_required(PaperDetail.as_view()), name='papers_paperdetail_view'),
    url(r'^(?P<pk>\d+)/post/$', login_required(BlogPostCreate.as_view()), name='blog_post_create'),
    url(r'^(?P<pk>\d+)/message/$', 'paper_send_message', name='send_message'),
    
    url(r'^add_rating/$', 'add_rating', name='add_rating'),
    url(r'^get_data/$', 'get_data', name='get_data'),
)



from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from blog.views import BlogHome, BlogPostDetail, BlogPostCreate

urlpatterns = patterns(
    'blog.views',
    url(r'^$', BlogHome.as_view(), name='blog_home'),
    url(r'^(?P<slug>[\w-]+)/$', BlogPostDetail.as_view(), name='blog_post_detail'),
)




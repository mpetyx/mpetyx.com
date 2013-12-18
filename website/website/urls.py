from django.conf.urls import patterns, include, url

# from .feeds import *

from django.contrib import admin
admin.autodiscover()

# feeds = {
# # 'articles': ArticlesFeed,
# 'blog': BlogFeed,
# # 'podcasts': PodcastFeed,
# }


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'website.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # (r'^feeds/(?P.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    # (r'^feed/$', BlogFeed()),
    # (r'^', include('blogger.urls')),

)

urlpatterns += patterns(
    '',
    url(r'', include('mapentity.urls', namespace='mapentity',
                     app_name='mapentity')),
    url(r'^paperclip/', include('paperclip.urls')),
    url(r'', include('museum.urls', namespace='main',
                     app_name='museum')),
)
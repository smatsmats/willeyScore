from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from willeyScore import topviews

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'willeyScore.views.home', name='home'),
    # url(r'^willeyScore/', include('willeyScore.foo.urls')),
    url(r'^$', topviews.top_home, name='top_home'),
    url(r'^ws/', include('ws.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

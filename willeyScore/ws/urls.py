from django.conf.urls import patterns, url

from ws import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^inout/$', views.inout, name='In Out'),
    url(r'^comp_class/$', views.comp_class, name='comp_class'),
    url(r'^scoring_rules/$', views.scoring_rules, name='scoring_rules'),
    url(r'^(?P<event_short_name>\w+)/$', views.oa, name='oa'),
    url(r'^(?P<event_short_name>\w+)/event/$', views.event, name='event'),
    url(r'^(?P<event_short_name>\w+)/cars/$', views.cars, name='cars'),
    url(r'^(?P<event_short_name>\w+)/detail/$', views.detail, name='detail'),
    url(r'^(?P<event_short_name>\w+)/stats/$', views.stats, name='stats'),
    url(r'^(?P<event_short_name>\w+)/inout/$', views.inout, name='inout'),
    url(r'^(?P<event_short_name>\w+)/(?P<leg_name>\w+)inout/$', views.inout, name='inout'),
)


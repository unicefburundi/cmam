from django.conf.urls import patterns, url
from bdiadmin.views import *

urlpatterns = patterns('',
        url(r'^get_commune/(?P<pk>\d+)/$', get_commune, name='get_commune'),
        url(r'^get_colline/(?P<pk>\d+)/$', get_colline, name='get_colline'),
        #Provinces
        url(r'^province/$', ProvinceListView.as_view(), name='province_list'),
        url(r'^province/add/$', ProvinceCreateView.as_view(), name='province_add'),
        #Communes
        url(r'^commune/$', CommuneListView.as_view(), name='commune_list'),
        url(r'^commune/add/$', CommuneCreateView.as_view(), name='commune_add'),
        #Collines
        url(r'^colline/$', CollineListView.as_view(), name='colline_list'),
        url(r'^colline/add/$', CollineCreateView.as_view(), name='colline_add'),
)
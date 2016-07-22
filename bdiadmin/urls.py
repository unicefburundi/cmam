from django.conf.urls import patterns, url
from bdiadmin.views import get_district

urlpatterns = patterns('',
        url(r'^get_district/(?P<pk>\d+)/$', get_district, name='get_district'),
)
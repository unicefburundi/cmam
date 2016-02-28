from django.conf.urls import patterns, url
from cmam_app.backend import handel_rapidpro_request
from cmam_app.views import *


urlpatterns = patterns('',
    url(r'external_request', handel_rapidpro_request, name="handel_request"),
)

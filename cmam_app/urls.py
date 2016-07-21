from django.conf.urls import patterns, url, include
from cmam_app.backend import handel_rapidpro_request
from cmam_app.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)


urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'external_request', handel_rapidpro_request, name="handel_request"),
    url(r'^sorties/$', SortiesView.as_view(), name="sorties"),
)

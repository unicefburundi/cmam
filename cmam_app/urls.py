from django.conf.urls import patterns, url, include
from cmam_app.backend import handel_rapidpro_request
from cmam_app.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'provinces', ProvinceDistrictViewSet)
router.register(r'districts', DistrictCDSViewSet)
router.register(r'incoming', IncomingViewset)
router.register(r'outgoing', OutgoingViewset)
router.register(r'inoutreport', InOutViewset, base_name="inoutreport")



urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'external_request', handel_rapidpro_request, name="handel_request"),
    url(r'^stocks/$', StockView.as_view(), name="stocks"),
    url(r'^programs/$', programs, name="programs"),
    url(r'^get_year/$', get_year, name="get_year"),
)

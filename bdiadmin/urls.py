from django.conf.urls import patterns, url, include
from bdiadmin.views import get_district, DistrictViewSet, ProvinceViewSet, edit_user, ProfileUserListView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'province', ProvinceViewSet)
router.register(r'district', DistrictViewSet)


urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
    url(r'^get_district/(?P<pk>\d+)/$', get_district, name='get_district'),
    url(r'^profile/(?P<pk>\d+)/$', edit_user, name='edit_profile'),
    url(r'^profile/$', ProfileUserListView.as_view(), name='profile'),
)
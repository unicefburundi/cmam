from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.contrib.auth import views


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cmam/', include('cmam_app.urls')),
    url(r'^bdiadmin/', include('bdiadmin.urls', namespace='bdiadmin', app_name='bdiadmin')),
    url(r'^home/$', 'cmam_app.views.home', name='home'),
    url(r'^dashboard/$', 'cmam_app.views.dashboard', name='dashboard'),
    url(r'^login/$', views.login, {'template_name': 'login.html'}, name="login"),
    url(r'^logout/$', views.logout, {'template_name': 'login.html'}, name="logout"),
    url(r'^$', 'cmam_app.views.landing'),
)


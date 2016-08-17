"""cmam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.contrib.auth import views


#urlpatterns = [
#    url(r'^admin/', include(admin.site.urls)),
#]

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cmam/', include('cmam_app.urls')),
    url(r'^bdiadmin/', include('bdiadmin.urls', namespace='bdiadmin', app_name='bdiadmin')),
    url(r'^home/$', 'cmam_app.views.home', name='home'),
    url(r'^dashboard/$', 'cmam_app.views.dashboard', name='dashboard'),
    url(r'^login/$', views.login, {'template_name': 'login.html'}, name="login"),
    url(r'^logout/$', views.login, {'template_name': 'login.html'}, name="logout"),
    url(r'^$', 'cmam_app.views.landing'),
    )


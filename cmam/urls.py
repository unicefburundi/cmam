from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views
from cmam_app.views import home, dashboard, landing
from django.conf import settings

urlpatterns = [
    url(r"^admin/", include(admin.site.urls)),
    url(r"^cmam/", include("cmam_app.urls")),
    url(r"^explorer/", include("explorer.urls")),
    url(r"^accounts/", include("authtools.urls")),
    url(
        r"^bdiadmin/",
        include("bdiadmin.urls", namespace="bdiadmin", app_name="bdiadmin"),
    ),
    url(r"^home/$", home, name="home"),
    url(r"^dashboard/$", dashboard, name="dashboard"),
    url(r"^login/$", views.login, {"template_name": "login.html"}, name="login"),
    url(r"^logout/$", views.logout, {"template_name": "login.html"}, name="logout"),
    url(r"^$", landing, name="landing"),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns

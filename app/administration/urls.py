from django.contrib import admin
from .healthcheck import run_healthcheck
from django.urls import path, re_path, include

admin.site.site_header = 'Coronavirus Dashboard - Admin'  # default: "Django Administration"
admin.site.index_title = 'Admin'  # default: "Site administration"
admin.site.site_title = 'Coronavirus Dashboard - Admin'   # default: "Django site admin"


urlpatterns = [
    re_path(r'^healthcheck/?', run_healthcheck),
    re_path(r'^administration/healthcheck/?', run_healthcheck),
    re_path(r'^markdownx/', include('markdownx.urls')),
    path('', admin.site.urls),
]

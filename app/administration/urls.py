from django.contrib import admin
from django.urls import path, re_path, include

admin.site.site_header = 'Coronavirus Dashboard - Admin'  # default: "Django Administration"
admin.site.index_title = 'Admin'  # default: "Site administration"
admin.site.site_title = 'Coronavirus Dashboard - Admin'   # default: "Django site admin"


urlpatterns = [
    path('', admin.site.urls),
    re_path(r'^markdownx/', include('markdownx.urls')),
]

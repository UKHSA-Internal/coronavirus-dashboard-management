#!/usr/bin python3

"""
<Description of the programme>

Author:        Pouria Hadjibagheri <pouria.hadjibagheri@phe.gov.uk>
Created:       21 Jan 2020
License:       MIT
Contributors:  Pouria Hadjibagheri
"""

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:

# 3rd party:
from django.urls import include, re_path
from django.contrib.auth.models import User

from rest_framework import routers, serializers, viewsets

from rest_framework_nested import routers as drf_routers

from rest_framework.schemas import get_schema_view

# Internal:
# from . import views

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Header
__author__ = "Pouria Hadjibagheri"
__copyright__ = "Copyright (c) 2020, Public Health England"
__license__ = "MIT"
__version__ = "0.0.1"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# __all__ = [
#     'urlpatterns'
# ]


app_name = "service"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
# router.register(r'content_entries', views.EntryApiViewSet)
# router.register(r'entry_fields', views.FieldApiViewSet)
# router.register(r'', views.ServiceApiView)

# Service router
# service_router = drf_routers.NestedSimpleRouter(
#     router,
#     r'',
#     lookup='service'
# )

# Sections of a service:
# service_router.register(
#     prefix='section',
#     viewset=views.SectionApiViewSet,
#     basename='service-sections'
# )


#
# # Fields associated with a service:
# service_router.register(
#     prefix='field',
#     viewset=views.FieldApiViewSet,
#     basename='service-fields'
# )
#
# # Section of a service router:
# section_router = drf_routers.NestedDefaultRouter(
#     service_router,
#     r'section',
#     lookup='section'
# )
#
# # Contents of a section:
# section_router.register(
#     prefix='content',
#     viewset=views.ContentApiView,
#     basename='section-contents'
# )
#
#
# content_router = drf_routers.NestedDefaultRouter(
#     section_router,
#     r'content',
#     lookup='content'
# )
#
# content_router.register(
#     prefix='entries',
#     viewset=views.EntryApiViewSet,
#     basename='content-entries'
# )


schema = get_schema_view(title="Schema")

# ToDo: Add API Documentations.
urlpatterns = [
    # re_path(r'', views.ContentView.as_view()),
    # re_path(r'^dashboard/?$', views.ServiceListView.as_view()),
    # re_path(r'^dashboard/(?P<service>[^./]+)/?$', views.ServiceSections.as_view(), name="dashboard-services"),
    # re_path(r'^dashboard/(?P<service>[^./]+)/(?P<section>[^./]+)/?$', views.SectionContents.as_view(), name="dashboard-sections"),
    # re_path(r'^dashboard/(?P<service>[^./]+)/(?P<section>[^./]+)/(?P<content>[^./]+)/?$', views.ContentDetails.as_view(), name="dashboard-content"),
    re_path(r'^api/v1/', include(router.urls)),
    # re_path(r'^api/v1/', include(service_router.urls)),
    # re_path(r'^api/v1/', include(section_router.urls)),
    # re_path(r'^api/v1/', include(content_router.urls)),
    # re_path(r'^(?P<service>[^./]+)/(?P<section>[^./]+)/(?P<content>[^./]+)/entries/?'),
    # re_path(r'^(?P<service>[^./]+)/(?P<section>[^./]+)/(?P<content>[^./]+)/entries/(?P<pk>\d{1,12})/?'),
    re_path(r'^api/v1/schema', schema),
]

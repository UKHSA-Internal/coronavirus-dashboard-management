#!/usr/bin python3

# from django.urls import include, re_path
from django.contrib.auth.models import User
from django.urls.conf import path, include, re_path

# from rest_framework import routers, serializers, viewsets

# from rest_framework_nested import routers as drf_routers

# from rest_framework.schemas import get_schema_view

# Internal:
from service_admin import views


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'is_staff']


# ViewSets define the view behavior.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'content_entries', views.EntryApiViewSet)
# router.register(r'entry_fields', views.FieldApiViewSet)
# router.register(r'', views.SectionApiView)

# Service router
# section_router = drf_routers.NestedSimpleRouter(
#     router,
#     r'',
#     lookup='page'
# )

# Sections of a service:
# service_router.register(
#     prefix='section',
#     viewset=views.SectionApiViewSet,
#     basename='service-sections'
# )

# Fields associated with a service:
# section_router.register(
#     prefix='field',
#     viewset=views.FieldApiViewSet,
#     basename='service-fields'
# )

# Section of a service router:
# section_router = drf_routers.NestedDefaultRouter(
#     service_router,
#     r'section',
#     lookup='section'
# )

# Contents of a section:
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


# schema = get_schema_view(title="Schema")

# ToDo: Add API Documentations.
urlpatterns = [
    path('textstats', views.text_stats_api_view, name="textstats"),
    # re_path(r'^dashboard/?$', views.SectionApiView.as_view({"get": "list"})),
    # re_path(r'^dashboard/(?P<service>[^./]+)/?$', views.ServiceSections.as_view(), name="dashboard-services"),
    # re_path(r'^dashboard/(?P<section>[^./]+)/?$', views.SectionContents.as_view(), name="dashboard-sections"),
    # re_path(r'^dashboard/(?P<section>[^./]+)/(?P<content>[^./]+)/?$', views.ContentDetails.as_view(), name="dashboard-content"),
    # re_path(r'^api/v1/', include(router.urls)),
    # re_path(r'^api/v1/', include(section_router.urls)),
    # re_path(r'^api/v1/', include(content_router.urls)),
    # re_path(r'^api/v1/schema', schema),
]


#
# urlpatterns = [
# ]

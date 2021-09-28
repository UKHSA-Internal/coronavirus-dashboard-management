#!/usr/bin python3

"""
<Description of the programme>

Author:        Pouria Hadjibagheri <pouria.hadjibagheri@phe.gov.uk>
Created:       19 Jan 2020
License:       MIT
Contributors:  Pouria Hadjibagheri
"""

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:


# 3rd party:
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.settings import api_settings
from rest_framework.reverse import reverse as rest_reverse
from django.urls import reverse

from django.views.generic import ListView

from django.db.models.query import QuerySet
from django.db.models import Prefetch

# Internal:
from ..models.page import Page
from ..models.cms import Content
from ..serializers import SectionSerializerV1
from .generic import GenericApiViewSet

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Header
__author__ = "Pouria Hadjibagheri"
__copyright__ = "Copyright (c) 2020, Public Health England"
__license__ = "MIT"
__version__ = "0.0.1"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'SectionApiView',
    'SectionApiViewSet',
    'ServiceSections'
]


class ServiceSections(ListView):
    queryset = Page.objects.all()
    template_name = 'dashboard/service_sections.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        service = Page.objects.filter(
            slug=self.kwargs.get("service")
        ).only("name").get()

        context['service_name'] = service.name
        context['service_api_url'] = rest_reverse(
            'service:service-detail',
            kwargs={
                'slug': self.kwargs.get("service")
            },
            request=self.request
        )
        context['api_url'] = reverse(
            "service:service-sections-list",
            kwargs={
                'service_slug': self.kwargs.get("service")
            }
        )

        return context

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(service__slug=self.kwargs.get("service")).prefetch_related(
            'oversight_records'
        )
        return qs.all()


class SectionApiView(ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = SectionSerializerV1
    lookup_field = 'title'


class SectionApiViewSet(GenericApiViewSet):
    queryset = Page.objects.all()
    serializer_class = SectionSerializerV1
    lookup_field = "slug"
    lookup_kws = {
        # param: field
        'slug': 'slug',
        'service_slug': 'service__slug'
    }

    def list(self, request, *args, **kwargs):
        """
        .. NOTE:: Pagination not enabled.
        """
        qs = self.queryset.prefetch_related(
            Prefetch('contents', Content.objects.published())
        ).filter(
            service__slug=kwargs.get('service_slug')
        ).all()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        qs = self.queryset.prefetch_related(
            Prefetch('contents', Content.objects.published())
        ).filter(
            service__slug=kwargs.get('service_slug'),
            slug=kwargs.get('slug')
        ).get()
        serializer = self.get_serializer(qs)
        return Response(serializer.data)

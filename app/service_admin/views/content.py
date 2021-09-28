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
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.core.serializers import serialize
from django.urls import reverse

from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.reverse import reverse as rest_reverse

# Internal:
from service_admin.models import Content
from service_admin.models.page import Page
from service_admin.serializers import ContentSerializerV1
from .generic import GenericApiViewSet
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Header
__author__ = "Pouria Hadjibagheri"
__copyright__ = "Copyright (c) 2020, Public Health England"
__license__ = "MIT"
__version__ = "0.0.1"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'ContentView',
    'ContentApiView',
    'SectionContents',
    'ContentDetails'
]


class ContentDetails(DetailView):
    queryset = Content.objects.all()
    template_name = 'dashboard/content_details.html'
    slug_field = 'slug'
    slug_url_kwarg = 'content'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        context['section_details'] = Page.objects.only(
            "name",
            "uri",
        ).get(
            uri=self.kwargs.get("section")
        )

        context['api_url'] = reverse(
            "service:section-contents-detail",
            kwargs={
                'page_slug': self.kwargs.get("section"),
                'slug': self.kwargs.get("content")
            }
        )
        context['contents_url'] = reverse(
            "service:section-contents-list",
            kwargs={
                'page_slug': self.kwargs.get("section"),
            }
        )
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(
            page__title__iexact=self.kwargs.get("section"),
            slug=self.kwargs.get("content")
        ).prefetch_related(
            'oversight_records'
        )
        return qs.all()


# class SectionListView(ListView):
#     queryset = Page.objects.all()
#     # template_name = 'dashboard/services.html'


class SectionContents(ListView):
    queryset = Content.objects.all()
    template_name = 'dashboard/section_contents.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        context['section_details'] = Page.objects.only(
            "title",
        ).get(
            title__iexact=self.kwargs.get("section")
        )

        context['api_url'] = reverse(
            "service:section-contents-list",
            kwargs={
                'page_slug': self.kwargs.get("section")
            }
        )

        context['section_api_url'] = rest_reverse(
            'service:service-sections-detail',
            kwargs={
                'slug': self.kwargs.get("section")
            },
            request=self.request
        )

        context['content_api_url'] = rest_reverse(
            'service:section-contents-list',
            kwargs={
                'page_slug': self.kwargs.get("section")
            },
            request=self.request
        )
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        # qs = qs.filter(
        #     page__title__iexact=self.kwargs.get("section")
        # )
        return qs.all()


class ContentView(TemplateView):
    model = Content
    template_name = 'content.html'

    def get(self, request, *args, **kwargs):
        qs = self.model.objects.filter(page__title__iexact=kwargs.get('section')).all()
        context = {
            'object': serialize("json", qs)
        }
        return self.render_to_response(context)


class ContentApiView(GenericApiViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializerV1
    lookup_field = 'slug'
    lookup_kws = {
        # param: field
        'slug': 'slug',
        'section_slug': 'page__uri',
    }

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related("section__service", "section")
        return qs

    def list(self, request, *args, **kwargs):
        """
        .. NOTE:: Pagination not enabled.
        """
        qs = self.queryset.filter(
            section__service__slug=kwargs.get('service_slug'),
            section__slug=kwargs.get('section_slug'),
            child_of__isnull=True
        ).all()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        qs = get_object_or_404(
            self.queryset,
            section__service__slug=kwargs.get('service_slug'),
            section__slug=kwargs.get('section_slug'),
            slug=kwargs.get('slug')
        )
        serializer = self.get_serializer(qs)
        return Response(serializer.data)

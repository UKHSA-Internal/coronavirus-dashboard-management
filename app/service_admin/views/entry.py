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
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

# Internal:
from ..models import Entry
from ..serializers import EntrySerializerV1
from .generic import GenericApiViewSet
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Header
__author__ = "Pouria Hadjibagheri"
__copyright__ = "Copyright (c) 2020, Public Health England"
__license__ = "MIT"
__version__ = "0.0.1"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'EntryApiViewSet'
]


class EntryApiViewSet(GenericApiViewSet):
    queryset = Entry.objects.all()
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    serializer_class = EntrySerializerV1
    lookup_kws = {
        'content_slug': 'content__slug',
        'section_slug': 'content__section__slug',
        'service_slug': 'content__section__service__slug',
        'pk': 'pk'
    }

    # def update(self, request, *args, **kwargs):
    #     data = {key: request.data.get(key) for key in request.data}
    #     return self._perform_update(data, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = {key: request.data.get(key) for key in request.data}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        """
        .. NOTE:: Pagination not enabled.
        """
        queries = {value: kwargs.get(key) for key, value in self.lookup_kws.items()}
        qs = self.queryset.filter(**queries).all()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queries = {value: kwargs.get(key) for key, value in self.lookup_kws.items()}
        queries.update({self.lookup_field: kwargs.get(self.lookup_url_kwarg)})
        qs = get_object_or_404(self.queryset, **queries)
        serializer = self.get_serializer(qs)
        return Response(serializer.data)

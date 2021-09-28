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
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from rest_framework.serializers import HyperlinkedRelatedField

# Internal:
from ..models.page import Page
from .generic import ParameterisedHyperlinkedIdentityField

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Header
__author__ = "Pouria Hadjibagheri"
__copyright__ = "Copyright (c) 2020, Public Health England"
__license__ = "MIT"
__version__ = "0.0.1"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'SectionSerializerV1'
]


class SectionSerializerV1(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        # 'service_slug': 'service__slug',
    }

    contents = NestedHyperlinkedRelatedField(
        view_name='section-contents-detail',
        read_only=True,
        many=True,
        lookup_field='slug',
        parent_lookup_kwargs={
            'section_slug': 'page__title__iexact',
        }
    )

    dashboard_url = ParameterisedHyperlinkedIdentityField(
        'dashboard-sections',
        lookup_fields=(
            ("title", "section"),
        ),
        read_only=True
    )

    # service = HyperlinkedRelatedField(
    #     view_name='service-detail',
    #     queryset=Page.objects.all(),
    #     lookup_field='slug'
    # )

    class Meta:
        model = Page
        fields = [
            'pk',
            'title',
            'contents',
            # 'url',
            'dashboard_url',
            'uri',
            # 'service'
        ]
        extra_kwargs = {
            'url': {
                'lookup_field': 'title',
                'view_name': 'service-sections-detail',
            },
        }


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
from functools import reduce


# 3rd party:
from rest_framework_nested.relations import NestedHyperlinkedRelatedField, NestedHyperlinkedIdentityField

from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer


# Internal:
from ..models.cms import Content
from .entry import EntrySerializerV1
from .generic import ParameterisedHyperlinkedIdentityField

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Header
__author__ = "Pouria Hadjibagheri"
__copyright__ = "Copyright (c) 2020, Public Health England"
__license__ = "MIT"
__version__ = "0.0.1"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'ContentSerializerV1'
]


class GenericContentSerializerMeta:
    model = Content
    fields = [
        'url',
    ]
    lookup_field = 'slug'
    extra_kwargs = {
        'url': {
            'lookup_field': 'slug',
            'view_name': 'section-contents-detail',
        }
    }


class GenericContentSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'section_slug': 'section__slug',
        'service_slug': 'section__service__slug',
    }

    class Meta(GenericContentSerializerMeta):
        pass


class RecursiveSerializer(GenericContentSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation['url']


class ContentSerializerV1(GenericContentSerializer):
    entries = EntrySerializerV1(read_only=True, many=True)
    dashboard_url = ParameterisedHyperlinkedIdentityField(
        'service:dashboard-content',
        lookup_fields=(
            ("section__service__slug", "service"),
            ("section__slug", "section"),
            ("slug", "content"),
        ),
        read_only=True
    )

    children = RecursiveSerializer(
        many=True,
        read_only=True
    )

    # child_of = RecursiveSerializer(read_only=True)
    # child_of = NestedHyperlinkedRelatedField(
    #     read_only=True
    # )

    # section = NestedHyperlinkedRelatedField(
    #     view_name='service-sections-detail',
    #     queryset=Section.objects.all(),
    #     parent_lookup_kwargs={
    #         'service_slug': 'service__slug'
    #     },
    #     lookup_field='slug'
    # )

    child_of = NestedHyperlinkedRelatedField(
        view_name='section-contents-detail',
        queryset=Content.objects.all(),
        parent_lookup_kwargs={
            'section_slug': 'section__slug',
            'service_slug': 'section__service__slug'
        },
        lookup_field='slug',
        required=True,
        allow_null=True
    )

    def create(self, validated_data):
        validated_data['section'] = validated_data['section']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'section_id' in validated_data:
            validated_data['section'] = validated_data['section']

        return super().update(instance, validated_data)

    class Meta(GenericContentSerializerMeta):
        fields = [
            'pk',
            'uuid',
            'label',
            'slug',
            'url',
            'dashboard_url',
            'section',
            # 'section_id',
            'child_of',
            'children',
            'entries'
        ]

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
from rest_framework.serializers import HyperlinkedModelSerializer, RelatedField, PrimaryKeyRelatedField

from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

# Internal:
from ..models.cms import Entry, Field, Content
from .field import FieldSerializerV1

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Header
__author__ = "Pouria Hadjibagheri"
__copyright__ = "Copyright (c) 2020, Public Health England"
__license__ = "MIT"
__version__ = "0.0.1"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'EntrySerializerV1'
]


class FieldRelatedField(RelatedField):
    def to_representation(self, value):
        return value.identifier


class EntrySerializerV1(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'content_slug': 'content__slug',
        'section_slug': 'content__page__uri',
    }

    field_details = FieldSerializerV1(read_only=True)
    # field = NestedHyperlinkedRelatedField(
    #     view_name='service-fields-detail',
    #     read_only=True,
    #     parent_lookup_kwargs={
    #         'service_slug': 'service__slug'
    #     },
    #     lookup_field='pk'
    # )
    field = PrimaryKeyRelatedField(queryset=Field.objects.all())
    content_id = PrimaryKeyRelatedField(queryset=Content.objects.all())

    class Meta:
        model = Entry
        fields = [
            'pk',
            'field',
            'field_details',
            'value',
            'order',
            'content_id',
            'url'
        ]
        extra_kwargs = {
            'field': {
                'lookup_field': 'pk',
                'view_name': 'service-fields-detail',
            },
            'url': {
                'lookup_field': 'pk',
                'view_name': 'content-entries-detail',
            }
        }

    def create(self, validated_data):
        validated_data['content_id'] = validated_data['content_id'].id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'content_id' in validated_data:
            validated_data['content_id'] = validated_data['content_id'].id
            
        return super().update(instance, validated_data)

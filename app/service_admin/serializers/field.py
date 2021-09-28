#!/usr/bin python3

"""
<Description of the programme>

Author:        Pouria Hadjibagheri <pouria.hadjibagheri@phe.gov.uk>
Created:       25 Jan 2020
License:       MIT
Contributors:  Pouria Hadjibagheri
"""

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from json import loads

# 3rd party:
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from rest_framework.serializers import JSONField

# Internal:
from ..models.cms import Field
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Header
__author__ = "Pouria Hadjibagheri"
__copyright__ = "Copyright (c) 2020, Public Health England"
__license__ = "MIT"
__version__ = "0.0.1"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'FieldSerializerV1'
]


# class JsonField(DRFField):
#     """ Serializer for JSONField -- required to make field writable"""
#
#     def to_internal_value(self, data):
#         return data
#
#     def to_representation(self, value):
#         return loads(value)


class FieldSerializerV1(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'service_slug': 'service__slug',
    }

    class Meta:
        model = Field
        fields = [
            'pk',
            'name',
            'identifier',
            'type',
            'meta_fields',
            'url'
        ]
        extra_kwargs = {
            'url': {
                'lookup_field': 'pk',
                'view_name': 'service-fields-detail',
            },
        }

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['type_long'] = instance.type_name()
        return res

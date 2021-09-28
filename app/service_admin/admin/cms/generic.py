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
from django.contrib.admin import ModelAdmin, register, TabularInline, StackedInline
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline

# 3rd party:
from reversion.admin import VersionAdmin
from guardian.admin import GuardedModelAdmin

# Internal:
from service_admin.models import cms

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Header
__author__ = "Pouria Hadjibagheri"
__copyright__ = "Copyright (c) 2020, Public Health England"
__license__ = "MIT"
__version__ = "0.0.1"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'CardAdmin',
]


# class GenericAdmin(VersionAdmin, ModelAdmin):
class GenericAdmin(ModelAdmin):
    pass


@register(cms.Card)
class CardAdmin(GenericAdmin):
    pass


class TabFieldTabularInline(StackedInline):
    model = cms.TabField
    fk_name = "tab"
    ct_field = "field_type"
    ct_fk_field = "field_id"
    readonly_fields = ['id']
    extra = 5
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "field_type",
                    "field_id",
                    "published",
                    "id",
                ),
            }
        ),
    )

# @register(cms.TabField)
# class TabFieldAdmin(GenericTabularInline):



@register(cms.Tab)
class TabAdmin(GenericAdmin):
    inlines = (
        TabFieldTabularInline,
    )
    readonly_fields = ['id']

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'id',
                    'id_label',
                    ('type', 'label'),
                    'custom_filters',
                    # 'fields',
                ),
            },
        ),
    )


class VisualisationTabMetricAdmin(GenericStackedInline):
    ct_field = "field_type"
    ct_fk_field = "field_id"
    verbose_name = "Metric"
    verbose_name_plural = "Metrics"
    model = cms.TabMetric
    readonly_fields = ['id']
    extra = 5
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    ("label", "value", "colour"),
                    "tooltip",
                ),
            }
        ),
    )


# class TabulationTabMetricAdmin(StackedInline):
#     verbose_name = "Metric"
#     verbose_name_plural = "Metrics"
#     model = cms.TabulationField.metrics.through
#     readonly_fields = ['id']
#     extra = 5


@register(cms.VisualisationField)
class VisualisationFieldAdmin(GenericAdmin):
    readonly_fields = [
        'id',
    ]
    inlines = (
        VisualisationTabMetricAdmin,
    )

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'id',
                    'id_label',
                    'type',
                    # 'value',
                    # 'label',
                    # 'colour',
                    # 'tooltip',
                    # 'metrics',
                    'rolling_average',
                ),
            },
        ),
        (
            "Line and area chart settings",
            {
                "fields": (
                    'fill',
                )
            }
        ),
        (
            "Bar chart settings",
            {
                "fields": (
                    'bar_type',
                    'highlight',
                )
            }
        ),
        (
            "Heatmap settings",
            {
                "fields": (
                    ('amplitude', 'amplitude_label'),
                    'metric_label',
                    'parameter',
                    'nested_metrics'
                )
            }
        )
    )


@register(cms.TabulationField)
class TabulationFieldAdmin(GenericAdmin):
    readonly_fields = [
        'id',
    ]
    inlines = (
        # TabulationTabMetricAdmin,
    )

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'id',
                    'id_label',
                    'type',
                    # 'value',
                    # 'label',
                    # 'tooltip',
                    # 'metrics',
                ),
            },
        ),
        (
            "Nested metrics",
            {
                "fields": (
                    'nested_metrics',
                )
            }
        )
    )


@register(cms.RollingAverage)
class RollingAverageAdmin(GenericAdmin):
    readonly_fields = [
        'id',
    ]

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'id',
                    ('window', 'clip_end',),
                ),
            },
        ),
    )


@register(cms.Highlight)
class HighlightAdmin(GenericAdmin):
    readonly_fields = [
        'id',
    ]

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'id',
                    'id_label',
                    'label',
                    ('from_index', 'to_index', 'colour',),
                ),
            },
        ),
    )


@register(cms.CustomFilterParameter)
class CustomFieldParameterAdmin(GenericAdmin):
    readonly_fields = [
        'id',
    ]

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'id',
                    ('key', 'sign', 'value'),
                ),
            },
        ),
    )


@register(cms.LocationFilter)
class LocationFilterAdmin(GenericAdmin):
    readonly_fields = [
        'id',
    ]

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'id',
                    'id_label',
                    'excluded',
                    'area_types',
                ),
            },
        ),
    )
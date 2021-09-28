#!/usr/bin python3

"""
<Description of the programme>

Author:        Pouria Hadjibagheri <pouria.hadjibagheri@phe.gov.uk>
Created:       05 Sep 2021
License:       MIT
Contributors:  Pouria Hadjibagheri
"""

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from uuid import uuid4

# 3rd party:
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Internal: 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Header
__author__ = "Pouria Hadjibagheri"
__copyright__ = "Copyright (c) 2021, Public Health England"
__license__ = "MIT"
__version__ = "0.0.1"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


__all__ = [
    'TabMetric'
]


class TabMetric(models.Model):
    id = models.UUIDField(
        verbose_name=_("unique ID"),
        primary_key=True,
        default=uuid4,
        editable=False,
        null=False,
        blank=False
    )
    label = models.CharField(
        max_length=40,
        blank=False,
        null=False,
        db_index=True
    )
    value = models.ForeignKey(
        "MetricReference",
        to_field='metric',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="%(class)s_related_tabs"
    )
    colour = models.ForeignKey(
        'Colour',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="%(class)s_related_colours"
    )
    tooltip = models.CharField(
        max_length=255,
        null=True,
        blank=False
    )

    field_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'model__in': [
                'visualisationfield',
                'tabulationfield',
            ]
        }
    )
    field_id = models.UUIDField()
    field = GenericForeignKey('field_type', 'field_id')

    def __str__(self):
        return f"{self.value.metric} in {self.colour.name} [{self.label}]"

    class Meta:
        db_table = 'cms"."tab_metric'
        verbose_name = _("tab metric")

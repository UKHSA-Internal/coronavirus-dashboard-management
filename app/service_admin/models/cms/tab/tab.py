#!/usr/bin python3

"""
<Description of the programme>

Author:        Pouria Hadjibagheri <pouria.hadjibagheri@phe.gov.uk>
Created:       04 Sep 2021
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

# Internal: 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Header
__author__ = "Pouria Hadjibagheri"
__copyright__ = "Copyright (c) 2021, Public Health England"
__license__ = "MIT"
__version__ = "0.0.1"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


__all__ = [
    'Tab',
]


class Tab(models.Model):
    TAB_TYPES = [
        ("chart", _("Chart")),
        ("table", _("Table")),
        ("nestedTable", _("Nested table")),
        ("metadata", _("Metadata")),
        ("heatmap", _("Heatmap"))
    ]
    id = models.UUIDField(
        verbose_name=_("unique ID"),
        primary_key=True,
        default=uuid4,
        editable=False,
        null=False,
        blank=False
    )
    id_label = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("For internal use.")
    )
    type = models.CharField(max_length=20, choices=TAB_TYPES)
    label = models.CharField(
        max_length=40,
        null=False,
        blank=False
    )
    custom_filters = models.ManyToManyField(
        'CustomFilterParameter',
        db_table='cms"."tab_to_filters'
    )
    # fields = models.ManyToManyField(
    #     'TabField',
    #     related_name='fields_of',
    #     db_table='cms"."tab_to_tab_fields',
    #     verbose_name=_("tab fields")
    # )

    def __str__(self):
        return f'{self.label} [{self.type}]'

    class Meta:
        db_table = 'cms"."tab'
        verbose_name = _("tab")


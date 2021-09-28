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
    'TabulationField'
]


class TabulationField(models.Model):
    TYPES = [
        ("numeric", _("Numeric")),
        ("date", _("Date")),
        ("text", _("Text")),
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
    type = models.CharField(
        max_length=10,
        null=True,
        blank=False,
        choices=TYPES
    )
    nested_metrics = models.JSONField(
        blank=False,
        null=True,
        default=dict
    )

    def __str__(self):
        if self.id_label:
            return self.id_label

        return self.metrics

    class Meta:
        db_table = 'cms"."tabulation_field'
        verbose_name = _("tabulation field")

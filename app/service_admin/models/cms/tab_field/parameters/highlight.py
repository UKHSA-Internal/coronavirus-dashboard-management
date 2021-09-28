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
from django.core.validators import MaxValueValidator, MinValueValidator

# Internal: 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Header
__author__ = "Pouria Hadjibagheri"
__copyright__ = "Copyright (c) 2021, Public Health England"
__license__ = "MIT"
__version__ = "0.0.1"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


__all__ = [
    "Highlight"
]


class Highlight(models.Model):
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
    label = models.CharField(
        max_length=40,
        blank=False,
        null=False
    )
    from_index = models.SmallIntegerField(
        blank=False,
        null=False,
        validators=[
            MinValueValidator(-30),
            MaxValueValidator(-1)
        ]
    )
    to_index = models.SmallIntegerField(
        blank=False,
        null=False,
        validators=[
            MinValueValidator(-29),
            MaxValueValidator(0)
        ]
    )
    colour = models.ForeignKey(
        'Colour',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    def __str__(self):
        if self.id_label:
            return self.id_label

        return self.label

    class Meta:
        db_table = 'cms"."highlight'
        verbose_name = _("highlight")

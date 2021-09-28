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
    'RollingAverage'
]


class RollingAverage(models.Model):
    id = models.UUIDField(
        verbose_name=_("unique ID"),
        primary_key=True,
        default=uuid4,
        editable=False,
        null=False,
        blank=False
    )
    window = models.PositiveSmallIntegerField(
        blank=False,
        null=False,
        default=7,
        validators=[
            MinValueValidator(2),
            MaxValueValidator(28)
        ],
        help_text=_("Number of points included in the rolling average window - range: [2, 28]")
    )
    clip_end = models.PositiveSmallIntegerField(
        blank=False,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ],
        help_text=_("Number of points to exclude from the end (offset) - range: [0, 10]")
    )

    def __str__(self):
        return f'W={self.window}, offset={self.clip_end}'

    class Meta:
        db_table = 'cms"."rolling_average'
        verbose_name = _("rolling average")

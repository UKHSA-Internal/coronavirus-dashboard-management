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
    'Card'
]


class Card(models.Model):
    CARD_TYPES = [
        ("chart", _("Chart")),
        ("multiAreaStatic", _("Multi area static")),
        ("recentData", _("Recent data")),
        ("ageSexBreakdown", _("Age-Sex breakdown")),
        ("ageSexBreakdown", _("Age-Sex breakdown")),
        ("simpleTableStatic", _("Simple table static")),
    ]

    id = models.UUIDField(
        verbose_name=_("unique ID"),
        primary_key=True,
        default=uuid4,
        editable=False,
        null=False,
        blank=False
    )
    type = models.CharField(
        choices=CARD_TYPES,
        max_length=25,
        blank=False,
        null=False
    )
    heading = models.CharField(
        max_length=75,
        blank=False,
        null=False
    )
    full_width = models.BooleanField(
        blank=False,
        null=False,
        default=True
    )
    optional_view = models.BooleanField(
        blank=False,
        null=False,
        default=False
    )
    abstract = models.TextField(null=True)
    introduction = models.TextField(null=True)
    location_aware = models.ForeignKey('LocationFilter', on_delete=models.CASCADE)
    tabs = models.ManyToManyField('Tab', db_table='cms"."card_tabs')
    published = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.heading

    class Meta:
        db_table = 'cms"."card'
        verbose_name = _("card")

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
    'CustomFilterParameter',
]


class CustomFilterParameter(models.Model):
    SIGNS = [
        ("=", "="),
        (">", ">"),
        (">=", ">="),
        ("<", "<"),
        ("<=", "<="),
        ("!=", "!="),
    ]

    id = models.UUIDField(
        verbose_name=_("unique ID"),
        primary_key=True,
        default=uuid4,
        editable=False,
        null=False,
        blank=False
    )
    key = models.CharField(
        max_length=120,
        blank=False,
        null=False
    )
    sign = models.CharField(
        choices=SIGNS,
        max_length=2,
        blank=False,
        null=False
    )
    value = models.CharField(
        max_length=40,
        blank=False,
        null=False
    )

    def __str__(self):
        return f'{self.key} {self.sign} {self.value}'

    class Meta:
        db_table = 'cms"."custom_filter_parameter'
        verbose_name = _("custom filter parameter")


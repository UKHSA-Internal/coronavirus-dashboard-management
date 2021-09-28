#!/usr/bin python3

"""
<Description of the programme>

Author:        Pouria Hadjibagheri <pouria.hadjibagheri@phe.gov.uk>
Created:       09 Sep 2021
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

from reversion import register as versioned

# Internal: 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Header
__author__ = "Pouria Hadjibagheri"
__copyright__ = "Copyright (c) 2021, Public Health England"
__license__ = "MIT"
__version__ = "0.0.1"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


__all__ = [
    'PrivateReport'
]


@versioned()
class PrivateReport(models.Model):
    id = models.UUIDField(
        verbose_name=_("unique ID"),
        primary_key=True,
        default=uuid4,
        editable=False,
        null=False,
        blank=False
    )
    slug_id = models.CharField(
        verbose_name=_("Slug ID"),
        max_length=40,
        editable=False,
        null=False,
        blank=False
    )
    release = models.ForeignKey(
        "ReleaseReference",
        on_delete=models.CASCADE,
        db_column="release_id",
        null=False,
        blank=False
    )
    metric = models.ForeignKey(
        "MetricReference",
        on_delete=models.CASCADE,
        db_column="metric",
        to_field="metric",
        null=False,
        blank=False
    )
    area = models.ForeignKey(
        "AreaReference",
        on_delete=models.CASCADE,
        db_column="area_id",
        null=False,
        blank=False
    )
    date = models.DateField(null=False, blank=False, editable=False)
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False,
        editable=False
    )

    def get_absolute_url(self):
        return (
            "https://coronavirus.data.gov.uk/downloads/ondemand/"
            f"prerelease/{self.slug_id}.html"
        )

    class Meta:
        managed = False
        db_table = 'covid19"."private_report'
        verbose_name = _("Pre-release report")

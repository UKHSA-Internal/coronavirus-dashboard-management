#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:

# 3rd party:
from django.utils.translation import gettext as _
from django.db import models

# Internal: 
from .data import MetricReference
from .fields import VarCharField
from ..utils.default_generators import generate_unique_id

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'MetricETLReference'
]


class MetricETLReference(models.Model):
    id = VarCharField(
        verbose_name=_("unique ID"),
        max_length=36,
        primary_key=True,
        default=generate_unique_id
    )
    metric = models.OneToOneField(
        MetricReference,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    missing_to_zero = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )
    fill_forward = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )
    negative_to_zero = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )
    prevalence_rate = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )
    incidence_rate = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )
    ratio_to_percentage = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )
    rolling_sum_direction = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )

    class Meta:
        db_table = 'covid19"."metric_etl_reference'
        verbose_name = _("ETL Metric")
        verbose_name_plural = _("ETL Metrics")

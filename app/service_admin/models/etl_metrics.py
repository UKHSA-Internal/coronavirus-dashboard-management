#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:

# 3rd party:
from django.utils.translation import gettext as _
from django.db import models

from django_multitenant import mixins as mt_mixins
from django_multitenant import models as mt_models
from django_multitenant import fields as mt_fields

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
        to_field='metric',
        db_column='metric_id',
        null=False,
        blank=False,
        editable=False,
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
        managed = False
        db_table = 'covid19"."metric_etl_reference'
        verbose_name = _("ETL Metric")
        verbose_name_plural = _("ETL Metrics")

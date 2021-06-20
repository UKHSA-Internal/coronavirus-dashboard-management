from django.db import models
from django.utils.translation import gettext as _
from ..fields import VarCharField
from ..data import MetricReference
from ...utils.default_generators import generate_unique_id
from markdownx.models import MarkdownxField

from django_multitenant import models as mt_models


__all__ = [
    'MetricAsset',
    'MetricAssetToMetric'
]


class TenantManager(mt_models.TenantManagerMixin, models.Manager):
    pass


class MetricAsset(models.Model):
    id = VarCharField(
        verbose_name=_("unique ID"),
        max_length=36,
        primary_key=True,
        default=generate_unique_id
    )
    last_modified = models.DateTimeField(verbose_name=_("last modified"), auto_now=True, null=False)
    label = VarCharField(max_length=255, null=False, blank=False)
    released = models.BooleanField(verbose_name=_("released"), default=False, null=False)
    body = MarkdownxField(null=False, blank=False)

    def __str__(self):
        return self.label

    class Meta:
        managed = False
        db_table = 'covid19\".\"metric_asset'
        ordering = ("label",)


class MetricAssetToMetric(models.Model):
    ASSET_TYPES = [
        ('ABSTRACT', _("Abstract")),
        ('DESCRIPTION', _("Description")),
        ('METHODOLOGY', _("Methodology")),
        ('NOTICE', _("Notice")),
        ('SOURCE', _("Source")),
    ]

    id = VarCharField(
        verbose_name=_("unique ID"),
        max_length=36,
        primary_key=True,
        default=generate_unique_id
    )
    metric = models.ForeignKey(MetricReference, to_field='metric', on_delete=models.CASCADE)
    asset = models.ForeignKey(MetricAsset, on_delete=models.CASCADE)
    asset_type = VarCharField(max_length=50, choices=ASSET_TYPES, db_index=True)
    order = models.PositiveIntegerField(verbose_name=_("order"), null=True, db_index=True)

    class Meta:
        managed = False
        db_table = 'covid19\".\"metric_asset_to_metric'
        unique_together = (
            ("metric", "asset", "order"),
            ("metric", "asset")
        )
        verbose_name = _("asset association")
        ordering = ("metric", "asset", "order")

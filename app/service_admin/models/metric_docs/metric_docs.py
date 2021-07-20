from django.db import models
from django.utils.translation import gettext as _
from ..fields import VarCharField
from ..data import MetricReference
from ...utils.default_generators import generate_unique_id
from markdownx.models import MarkdownxField
from uuid import uuid4
from django_multitenant import models as mt_models
from reversion import register as versioned


__all__ = [
    'MetricAsset',
    'MetricAssetToMetric'
]


class TenantManager(mt_models.TenantManagerMixin, models.Manager):
    pass


@versioned()
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


@versioned()
class MetricAssetToMetric(models.Model):
    ASSET_TYPES = [
        ('ABSTRACT', _("Abstract")),
        ('DESCRIPTION', _("Description")),
        ('METHODOLOGY', _("Methodology")),
        ('NOTICE', _("Notice")),
        ('SOURCE', _("Source")),
    ]

    id = models.UUIDField(
        verbose_name=_("unique ID"),
        primary_key=True,
        editable=False,
        default=uuid4
    )
    metric = models.ForeignKey(MetricReference, to_field='metric', on_delete=models.CASCADE)
    asset = models.ForeignKey(MetricAsset, on_delete=models.CASCADE)
    asset_type = VarCharField(max_length=50, choices=ASSET_TYPES)
    order = models.PositiveIntegerField(verbose_name=_("order"), null=True)

    def __str__(self):
        return f"{self.metric.metric}: {self.asset.label}"

    class Meta:
        managed = False
        db_table = 'covid19\".\"metric_asset_to_metric'
        unique_together = (
            ("metric", "asset"),
            ("metric", "asset_type", "order")
        )
        verbose_name = _("asset association")
        ordering = ("metric", "asset", "order")

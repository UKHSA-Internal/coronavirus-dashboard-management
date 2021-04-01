from django.db import models
from django.utils.translation import gettext as _
from ..fields import VarCharField
from ..data import MetricReference
from ...utils.default_generators import generate_unique_id
from markdownx.models import MarkdownxField

from django_multitenant import fields as mt_fields
from django_multitenant import models as mt_models
from django_multitenant import mixins as mt_mixins

__all__ = [
    'MetricAsset',
    'MetricAssetToMetric'
    # 'MetricDescription',
    # 'MetricMethodology',
    # 'MetricDataSource',
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
    label = VarCharField(max_length=255, null=False, blank=False)
    body = MarkdownxField(null=False, blank=False)
    metric = models.ManyToManyField(
        MetricReference,
        through='MetricAssetToMetric'
    )

    class Meta:
        db_table = 'covid19\".\"metric_asset'


class MetricAssetToMetric(mt_mixins.TenantModelMixin, models.Model):
    ASSET_TYPES = [
        ('ABSTRACT', _("Abstract")),
        ('DESCRIPTION', _("Description")),
        ('METHODOLOGY', _("Methodology")),
    ]

    id = VarCharField(
        verbose_name=_("unique ID"),
        max_length=36,
        primary_key=True,
        default=generate_unique_id
    )
    # metric = models.ForeignKey(MetricReference, to_field='metric', on_delete=models.CASCADE)
    # asset = models.ForeignKey(MetricAsset, on_delete=models.CASCADE)
    metric = mt_fields.TenantForeignKey(MetricReference, on_delete=models.CASCADE)
    asset = mt_fields.TenantForeignKey(MetricAsset, on_delete=models.CASCADE)
    asset_type = VarCharField(max_length=50, choices=ASSET_TYPES, db_index=True)

    tenant_id = 'metric_id'

    objects = TenantManager()

    class Meta:
        db_table = 'covid19\".\"metric_asset_to_metric'


# class MetricDescription(models.Model):
#     id = VarCharField(
#         verbose_name=_("unique ID"),
#         max_length=36,
#         primary_key=True,
#         default=generate_unique_id
#     )
#     label = VarCharField(max_length=255, null=False, blank=False)
#     description = models.TextField(null=False, blank=False)
#     # metric = models.ManyToManyField(
#     #     MetricReference,
#     #     related_name='metric_descriptions'
#     # )
#
#     class Meta:
#         db_table = 'covid19\".\"metric_description'


# class MetricMethodology(models.Model):
#     id = VarCharField(
#         verbose_name=_("unique ID"),
#         max_length=36,
#         primary_key=True,
#         default=generate_unique_id
#     )
#     label = VarCharField(max_length=255, null=False, blank=False)
#     methodology = models.TextField(null=False, blank=False)
#     metric = models.ManyToManyField(
#         MetricReference,
#         related_name='metric_methodologies'
#     )
#
#     class Meta:
#         db_table = 'covid19\".\"metric_methodology'
#         verbose_name = _('Metric methodology')
#         verbose_name_plural = _('Metric methodologies')
#
#
# class MetricDataSource(models.Model):
#     id = VarCharField(
#         verbose_name=_("unique ID"),
#         max_length=36,
#         primary_key=True,
#         default=generate_unique_id
#     )
#     label = VarCharField(max_length=255, null=False, blank=False)
#     source = models.TextField(null=False, blank=False)
#     metric = models.ManyToManyField(
#         MetricReference,
#         related_name='metric_sources'
#     )
#     applicable_to = models.ForeignKey(
#         AreaReference,
#         on_delete=models.CASCADE,
#         limit_choices_to={
#             'area_type__in': ['overview', 'nation']
#         },
#         related_name="metric_source_for_area"
#     )
#
#     class Meta:
#         db_table = 'covid19\".\"metric_data_source'


# class MetricDocumentation(models.Model):
#     FREQUENCY_CHOICES = [
#         ('DAILY', 'Daily'),
#         ('WEEKLY', 'Weekly'),
#         ('FORTNIGHTLY', 'Fortnightly'),
#         ('MONTHLY', 'Monthly'),
#     ]
#
#     id = models.AutoField(primary_key=True)
#     metric_id = models.ForeignKey(
#         MetricReference,
#         on_delete=models.CASCADE,
#         related_name="documentation",
#         verbose_name=_("Metric")
#     )
#     update_frequency = VarCharField(
#         max_length=255,
#         choices=FREQUENCY_CHOICES,
#         null=False,
#         blank=False
#     )
#     abstract = models.ForeignKey(
#         MetricAbstract,
#         on_delete=models.CASCADE,
#         null=False,
#         blank=False
#     )
#     description = models.ForeignKey(
#         Description,
#         on_delete=models.CASCADE,
#         null=False,
#         blank=False
#     )
#     methodology = models.ForeignKey(
#         Methodology,
#         on_delete=models.CASCADE,
#         null=False,
#         blank=False
#     )
#     source = models.ManyToManyField(DataSource)
#
#     class Meta:
#         db_table = 'covid19\".\"metric_documentation'

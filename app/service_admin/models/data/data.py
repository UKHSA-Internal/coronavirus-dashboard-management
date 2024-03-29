
from uuid import uuid4
from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone
from ..fields import VarCharField
from django_multitenant import mixins as mt_mixins
from django_multitenant import models as mt_models
from reversion import register as versioned


PROCESS_TYPE_ENUM = [
    ('MAIN', _('Main')),
    ('MSOA', _('MSOA')),
    ('VACCINATION', _("Vaccinations")),
    ('POSITIVITY & PEOPLE TESTED', _("Positivity & People Tested")),
    ('AGE DEMOGRAPHICS: CASE - EVENT DATE', _("Age demographics: Cases")),
    ('AGE-DEMOGRAPHICS: DEATH28DAYS - EVENT DATE', _("Age demographics: Deaths 28 days")),
    ('AGE-DEMOGRAPHICS: VACCINATION - EVENT DATE', _("Age demographics: Vaccinations")),
    ('MSOA: VACCINATION - EVENT DATE', _('MSOA: Vaccinations')),
    ('HEALTHCARE', _('Healthcare')),
    ('TESTING: MAIN', _("Testing")),
    ('CASES: MAIN', _("Cases")),
    ('DEATHS: MAIN', _("Deaths")),
    ('AGE-DEMOGRAPHICS: CASES - FIRST EPISODES', _("Age demographics: Cases - First episodes")),
    ('AGE-DEMOGRAPHICS: CASES - REINFECTIONS', _("Age demographics: Cases - Reinfections")),
    ('EPISODE VARIANTS - EPISODES', _("Variants"))
]


class TenantManager(mt_models.TenantManagerMixin, models.Manager):
    pass


class AreaPriorities(models.Model):
    area_type = VarCharField(primary_key=True, max_length=15, null=False, blank=False)
    priority = models.DecimalField(max_digits=65535, decimal_places=65535)

    def __str__(self):
        return self.area_type

    class Meta:
        managed = False
        db_table = 'covid19"."area_priorities'
        unique_together = (
            ('area_type', 'priority'),
        )
        permissions = [
            ('create_area_priorities_object', _('Can create metrics')),
            ('manage_area_priorities_object', _('Can manage metrics')),
            ('view_area_priorities_object', _('Can view metrics')),
            ('delete_area_priorities_object', _('Can delete metrics')),
        ]


@versioned()
class AreaReference(models.Model):
    area_type_choices = (
        ('overview', _('Overview')),
        ('nation', _('Nation')),
        ('region', _('Region')),
        ('nhsRegion', _('NHS Region')),
        ('nhsTrust', _('NHS Trust')),
        ('utla', _('UTLA')),
        ('ltla', _('LTLA')),
        ('msoa', _('MSOA')),
    )

    id = models.AutoField(primary_key=True, unique=True)
    area_type = VarCharField(max_length=15, null=False, blank=False, choices=area_type_choices)
    area_code = VarCharField(max_length=12, null=False, blank=False)
    area_name = VarCharField(max_length=120, null=False, blank=False)
    unique_ref = VarCharField(max_length=26, null=False, blank=False, unique=True)

    def __str__(self):
        return self.area_code

    class Meta:
        managed = False
        db_table = 'covid19"."area_reference'
        unique_together = (
            ('area_type', 'area_code'),
            ('area_type', 'area_code'),
        )
        verbose_name = _("area")
        ordering = ['area_type', 'area_code']


class GeoReference(models.Model):
    id = models.BigAutoField(primary_key=True)
    area = models.ForeignKey(AreaReference, models.DO_NOTHING)
    type = VarCharField(max_length=50, null=False, blank=False)
    geometry_type = VarCharField(max_length=50, null=False, blank=False)
    coordinates = models.JSONField()

    class Meta:
        managed = False
        db_table = 'covid19"."geo_reference'


@versioned()
class MetricReference(models.Model):
    id = models.AutoField(primary_key=True)
    metric = VarCharField(unique=True, max_length=120, null=False, blank=False)
    metric_name = VarCharField(unique=True, max_length=150, null=True, blank=False)
    category = models.ForeignKey(
        'Page',
        null=True,
        on_delete=models.CASCADE,
        related_name="metrics_of",
        to_field="id",
        db_column="category",
        limit_choices_to={'data_category': True},
        verbose_name=_("category")
    )
    tags = models.ManyToManyField('Tag', through='MetricTag')
    assets = models.ManyToManyField('MetricAsset', through='MetricAssetToMetric')
    source_metric = models.BooleanField(
        verbose_name=_("source"),
        null=False,
        blank=False,
        default=False,
        help_text=_("The metric is present in the source data.")
    )
    released = models.BooleanField()
    deprecated = models.DateField(verbose_name=_("deprecated"), null=True, blank=True)

    def __str__(self):
        return self.metric

    class Meta:
        managed = False
        db_table = 'covid19"."metric_reference'
        verbose_name = _("metric")


# class MsoaRelations(models.Model):
#     msoa = models.OneToOneField(AreaReference, models.DO_NOTHING, primary_key=True)
#     area = models.ForeignKey(AreaReference, models.DO_NOTHING, related_name='')
#
#     class Meta:
#         managed = False
#         db_table = 'msoa_relations'
#         unique_together = (
#             ('msoa', 'area'),
#         )


class PostcodeLookup(models.Model):
    postcode = VarCharField(primary_key=True, max_length=10, null=False, blank=False)
    area = models.ForeignKey(AreaReference, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'covid19"."postcode_lookup'
        unique_together = (
            ('postcode', 'area'),
        )


class ProcessedFile(models.Model):
    id = models.UUIDField(
        verbose_name=_("unique ID"),
        primary_key=True,
        default=uuid4,
        editable=False,
        null=False,
        blank=False
    )

    file_path = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        unique=True
    )

    type = models.CharField(
        max_length=50,
        choices=PROCESS_TYPE_ENUM,
        verbose_name=_("release category"),
        null=False,
        blank=False
    )

    release = models.ForeignKey(
        'ReleaseReference',
        on_delete=models.CASCADE,
        null=True
    )

    timestamp = models.DateTimeField(verbose_name=_("landing time"))

    process_id = models.CharField(
        max_length=255,
        null=True,
        blank=False
    )

    def __str__(self):
        return self.file_path

    class Meta:
        managed = False
        db_table = 'covid19"."processed_file'
        ordering = ("-timestamp",)


class ProcessingStatus(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.ForeignKey(ProcessedFile, models.DO_NOTHING)
    status = models.TextField()  # This field type is a guess.
    timestamp = models.DateTimeField()
    note = models.TextField()

    class Meta:
        managed = False
        db_table = 'covid19"."processing_status'


@versioned()
class ReleaseCategory(models.Model):
    _process_type_dict = dict(PROCESS_TYPE_ENUM)

    release = models.OneToOneField('ReleaseReference', models.DO_NOTHING, primary_key=True, related_name='category')
    process_name = VarCharField(max_length=50, choices=PROCESS_TYPE_ENUM, null=False, blank=False)

    def __str__(self):
        return self._process_type_dict[self.process_name]

    class Meta:
        managed = False
        db_table = 'covid19"."release_category'
        unique_together = (('release', 'process_name'),)


@versioned()
class ReleaseStats(models.Model):
    release = models.OneToOneField(
        'ReleaseReference',
        on_delete=models.CASCADE,
        primary_key=True
    )
    record_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'covid19"."release_stats'
        verbose_name = _("Release statistic")
        verbose_name_plural = _("Release statistics")


class Despatch(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(null=False, unique=True)
    releases = models.ManyToManyField(
        to="ReleaseReference",
        through="DespatchToRelease",
        related_name="despatch_of"
    )

    def __str__(self):
        return f"{self.timestamp:%H:%M:%S}"

    class Meta:
        managed = False
        db_table = 'covid19"."despatch'
        ordering = ("-timestamp",)


class DespatchToRelease(models.Model):
    id = models.AutoField(primary_key=True)

    despatch = models.ForeignKey(
        "Despatch",
        db_column="despatch_id",
        to_field="id",
        on_delete=models.CASCADE,
        null=False
    )

    release = models.ForeignKey(
        "ReleaseReference",
        db_column="release_id",
        to_field="id",
        on_delete=models.CASCADE,
        related_name="despatched_at",
        null=False
    )

    class Meta:
        managed = False
        db_table = 'covid19"."despatch_to_release'
        unique_together = (
            ("despatch", "release"),
        )


@versioned()
class ReleaseReference(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(_("receipt time"), unique=True)
    released = models.BooleanField()

    def count(self):
        count = self.releasestats.record_count

        return f"{count:,d}"

    def previous_count(self):
        timestamp = timezone.make_aware(self.timestamp - timezone.timedelta(days=1))
        release_category = self.category.process_name

        release_ref = (
            ReleaseReference
            .objects
            .filter(
                timestamp__date=timestamp.date(),
                category__process_name=release_category
            )
            .values(count=models.F('releasestats__record_count'))
            .get()
        )

        try:
            return f"{release_ref['count']:,d}"
        except TypeError:
            return "0"

    def delta(self):
        today_count = int(self.count().replace(",", ""))
        previous_count = int(self.previous_count().replace(",", ""))

        return f"{today_count - previous_count:,d}"

    def confirmation(self):
        label = f"{self.category} data received on {self.timestamp:%A, %-d %B %Y} "

        if self.released:
            label += "[ ALREADY RELEASED ]"

        return {"label": label}

    def __str__(self):
        return f"{self.timestamp:%Y-%m-%d}"

    class Meta:
        managed = False
        db_table = 'covid19"."release_reference'
        verbose_name = _("release")
        ordering = ("-timestamp",)


class TimeSeries(mt_mixins.TenantModelMixin, models.Model):
    hash = VarCharField(primary_key=True, max_length=24, null=False, blank=False)
    partition_id = VarCharField(max_length=26)
    release_id = models.ForeignKey(
        ReleaseReference,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        db_column='release_id',
        verbose_name=_('release')
    )
    area_id = models.ForeignKey(
        AreaReference,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        db_column='area_id',
        verbose_name=_('area')
    )
    metric_id = models.ForeignKey(
        MetricReference,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        db_column='metric_id',
        verbose_name=_('metric')
    )
    date = models.DateField()
    payload = models.JSONField(blank=True, null=True)

    tenant_id = 'hash'
    objects = TenantManager()

    def area_type(self):
        return self.area_id.area_type.upper()

    def area_name(self):
        return self.area_id.area_name

    def area_code(self):
        return self.area_id.area_code

    def despatched(self):
        return self.release_id.released

    class Meta:
        managed = False
        db_table = 'covid19"."time_series'
        unique_together = (
            ('hash', 'area_id', 'metric_id', 'release_id', 'partition_id'),
            ('hash', 'partition_id'),
        )
        verbose_name_plural = _('time series')

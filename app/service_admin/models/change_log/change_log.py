#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from uuid import uuid4

# 3rd party:
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.postgres.fields import ArrayField

from markdownx.models import MarkdownxField
from reversion import register as versioned

# Internal: 
from ..fields import VarCharField

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'ChangeLog',
    'ChangeLogToPage',
    'ChangeLogToMetric'
]


@versioned()
class ChangeLog(models.Model):
    area_choices = (
        ("overview::^K.*$", _("UK [Overview]")),
        ("nation::^E92000001$", _("England [Nation]")),
        ("region::^E.*$", _("England [region]")),
        ("utla::^E.*$", _("England [UTLA]")),
        ("ltla::^E.*$", _("England [LTLA]")),
        ("msoa::^E.*$", _("England [MSOA]")),
        ("nation::^S92000003$", _("Scotland [Nation]")),
        ("utla::^S.*$", _("Scotland [UTLA]")),
        ("ltla::^S.*$", _("Scotland [LTLA]")),
        ("nation::^N92000002$", _("Northern Ireland [Nation]")),
        ("utla::^N.*$", _("Northern Ireland [UTLA]")),
        ("ltla::^N.*$", _("Northern Ireland [LTLA]")),
        ("nation::^W.*$", _("Wales [Nation]")),
        ("utla::^W.*$", _("Wales [UTLA]")),
        ("ltla::^W.*$", _("Wales [LTLA]")),
        ("nhsRegion::^.*$", _("All NHS regions")),
        ("nhsTrust::^.*$", _("All NHS trusts")),
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    date = models.DateField(null=False)
    expiry = models.DateField(
        null=True,
        blank=True,
        help_text=_("Only use when the log entry is applicable for a limited period.")
    )
    heading = VarCharField(max_length=150, blank=False, null=False)
    body = MarkdownxField(
        null=False,
        blank=False,
        help_text=_(
            "Markdown enabled. Keep as short as possible when 'High priority' "
            "option is checked."
        )
    )
    details = MarkdownxField(
        null=True,
        blank=True,
        help_text=_("Markdown enabled.")
    )
    high_priority = models.BooleanField(
        null=False,
        default=False,
        help_text=_(
            "Includes the 'Body' in the banner. Only effective when"
            " 'Display banner' option is checked."
        )
    )
    display_banner = models.BooleanField(null=False, default=False)
    type = models.ForeignKey(
        'Tag',
        null=False,
        limit_choices_to={"association": "CHANGE LOGS"},
        on_delete=models.CASCADE,
        related_name='log_pages'
    )
    metrics = models.ManyToManyField(
        'MetricReference',
        through='ChangeLogToMetric',
        related_name='log_metrics',
        blank=True
    )
    area = ArrayField(
        base_field=models.CharField(
            max_length=50,
            choices=area_choices
        ),
        blank=False,
        null=True,
        help_text=_("Hold CTRL / CMD to select or deselect multiple items.")
    )
    timestamp_created = models.DateTimeField(
        verbose_name=_("Created on"),
        auto_created=True,
        editable=False,
        null=False
    )
    pages = models.ManyToManyField(
        'Page',
        through='ChangeLogToPage',
        related_name='log_pages',
        blank=True
    )

    colours = {
        "new feature": {
            "background": "#CCE2D8",
            "text": "#005A30"
        },
        "new metric": {
            "background": "#BFE3E0",
            "text": "#10403C"
        },
        "change to metric": {
            "background": "#FFF7BF",
            "text": "#594D00"
        },
        "update": {
            "background": "#FCD6C3",
            "text": "#6E3619"
        },
        "new content": {
            "background": "#DBD5E9",
            "text": "#3D2375"
        },
        "data issue": {
            "background": "#EEEFEF",
            "text": "#383F43"
        },
        "other": {
            "background": "#D2E2F1",
            "text": "#144E81"
        },
    }

    def get_type_colours(self):
        return self.colours.get(self.type.tag, dict())

    def __str__(self):
        return self.heading

    class Meta:
        managed = False
        db_table = 'covid19"."change_log'
        ordering = ('-date',)


@versioned()
class ChangeLogToMetric(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    log = models.ForeignKey('ChangeLog', on_delete=models.CASCADE)
    metric = models.ForeignKey(
        'MetricReference',
        to_field='metric',
        on_delete=models.CASCADE,
        limit_choices_to={"deprecated__isnull": True}
    )

    def __str__(self):
        return self.metric.metric

    class Meta:
        managed = False
        db_table = 'covid19"."change_log_to_metric'
        unique_together = [
            ('log', 'metric'),
        ]
        ordering = ('log', 'metric')


@versioned()
class ChangeLogToPage(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    log = models.ForeignKey('ChangeLog', on_delete=models.CASCADE)
    page = models.ForeignKey(
        'Page',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.page.title

    class Meta:
        managed = False
        db_table = 'covid19"."change_log_to_page'
        unique_together = [
            ('log', 'page'),
        ]
        ordering = ('log', 'page')

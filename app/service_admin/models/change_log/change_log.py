#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from uuid import uuid4

# 3rd party:
from django.db import models

from markdownx.models import MarkdownxField

# Internal: 
from ..fields import VarCharField

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'ChangeLog',
    'ChangeLogToPage',
    'ChangeLogToMetric'
]


class ChangeLog(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    date = models.DateField(null=False)
    expiry = models.DateField(null=True)
    heading = VarCharField(max_length=150)
    body = MarkdownxField(null=False, blank=False)
    details = MarkdownxField(null=True)
    high_priority = models.BooleanField(null=False, default=False)
    type = models.ForeignKey(
        'Tag', null=False,
        limit_choices_to={"association": "CHANGE LOGS"},
        on_delete=models.CASCADE
    )
    metrics = models.ManyToManyField('Tag', through='ChangeLogToMetric')
    pages = models.ManyToManyField('Page', through='ChangeLogToPage')

    def __str__(self):
        return self.heading

    class Meta:
        managed = False
        db_table = 'covid19"."change_log'
        ordering = ('-date',)


class ChangeLogToMetric(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    log = models.ForeignKey('ChangeLog', on_delete=models.CASCADE)
    metric = models.ForeignKey(
        'MetricReference',
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


class ChangeLogToPage(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    log = models.ForeignKey('ChangeLog', on_delete=models.CASCADE)
    page = models.ForeignKey(
        'Page',
        on_delete=models.CASCADE,
        limit_choices_to={"data_category": True}
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

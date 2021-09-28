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
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.models import ContentType

# Internal: 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Header
__author__ = "Pouria Hadjibagheri"
__copyright__ = "Copyright (c) 2021, Public Health England"
__license__ = "MIT"
__version__ = "0.0.1"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    "VisualisationField"
]


class VisualisationField(models.Model):
    TYPES = [
        ("line", _("Line")),
        ("bar", _("Bar")),
        ("heatmap", _("Heatmap")),
    ]

    BAR_TYPES = [
        ("overlay", _("Overlay")),
        ("group", _("Group")),
        ("stack", _("Stack"))
    ]

    id = models.UUIDField(
        verbose_name=_("unique ID"),
        primary_key=True,
        default=uuid4,
        editable=False,
        null=False,
        blank=False
    )
    id_label = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("For internal use.")
    )
    type = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        choices=TYPES
    )
    rolling_average = models.ForeignKey(
        'RollingAverage',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    fill = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(11)
        ],
        help_text=_("Only applicable to line (area) plots - leave blank for other types.")
    )
    bar_type = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=BAR_TYPES,
        help_text=_("Only applicable to bar plots - leave blank for other types.")
    )
    highlight = models.ForeignKey(
        'Highlight',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text=_("Only applicable to bar plots - leave blanks for other types.")
    )

    # Heatmap only
    amplitude = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )
    amplitude_label = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )
    metric_label = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )
    parameter = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text=_("Attribute name for the 3rd dimension.")
    )
    nested_metrics = models.JSONField(
        default=dict,
        blank=True,
        null=True,
    )

    def __str__(self):
        if self.id_label:
            return self.id_label

        from .metrics import TabMetric

        ctype = ContentType.objects.get_for_model(self.__class__)

        metrics = (
            TabMetric
            .objects
            .filter(field_type__pk=ctype.id, field_id=self.id)
            .values_list("value__metric", flat=True)
        )

        return str.join(", ", metrics)

    class Meta:
        db_table = 'cms"."visualisation_field'
        verbose_name = _("visualisation field")

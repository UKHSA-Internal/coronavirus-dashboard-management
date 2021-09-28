#!/usr/bin python3

"""
<Description of the programme>

Author:        Pouria Hadjibagheri <pouria.hadjibagheri@phe.gov.uk>
Created:       18 Jan 2020
License:       MIT
Contributors:  Pouria Hadjibagheri
"""

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:

# 3rd party:
from django.db import models

from django.utils.translation import gettext as _

from reversion import register as reversion_register

# Internal:
# from .service import Service
# from .activity_log import OversightRecord

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Header
__author__ = "Pouria Hadjibagheri"
__copyright__ = "Copyright (c) 2020, Public Health England"
__license__ = "MIT"
__version__ = "0.0.1"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'Field',
]


@reversion_register()
class Field(models.Model):
    FIELD_TYPES = (
        ('ST', _("Short text (<256 characters)")),
        ('LT', _("Long text (256+ characters)")),
        ('IM', _("Image")),
        ('FL', _("File")),
        ('MA', _("Marker")),
        ('MD', _("Markdown")),
        ('RT', _("Rich Text (HTML)")),
        ('LC', _("Link to another page")),
    )

    field_types = dict(FIELD_TYPES)

    name = models.CharField(
        verbose_name=_("name"),
        max_length=64,
        null=False,
        db_index=True,
        blank=False
    )
    identifier = models.CharField(
        verbose_name=_("identifier"),
        max_length=16,
        null=False,
        db_index=True,
        blank=False
    )
    type = models.CharField(
        verbose_name=_("field type"),
        max_length=2,
        choices=FIELD_TYPES,
        null=False,
        db_index=True,
        blank=False
    )
    meta_fields = models.JSONField(
        verbose_name=_("meta fields"),
        default=dict,
        blank=True
    )
    # oversight_records = models.ManyToManyField(
    #     to=OversightRecord,
    #     verbose_name=_("oversight records"),
    #     related_name="field_records",
    #     db_index=True
    # )

    def type_name(self):
        return self.field_types[self.type]

    def __str__(self):
        return f"{self.name} ({self.identifier}): {self.type_name()}"

    class Meta:
        verbose_name = _("field")
        verbose_name_plural = _("fields")
        db_table = 'covid19"."cms_field'

        unique_together = [
            ("name", "service"),
        ]

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
from .field import Field
from .content import Content
# from .activity_log import OversightRecord

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Header
__author__ = "Pouria Hadjibagheri"
__copyright__ = "Copyright (c) 2020, Public Health England"
__license__ = "MIT"
__version__ = "0.0.1"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'Entry'
]


@reversion_register()
class Entry(models.Model):
    field = models.ForeignKey(
        verbose_name=_("field"),
        to=Field,
        related_name="entry_field",
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    value = models.TextField(
        verbose_name=_("value")
    )
    content = models.ForeignKey(
        to=Content,
        related_name="entries",
        on_delete=models.CASCADE,
        db_index=True
    )
    order = models.PositiveIntegerField(
        verbose_name=_("order"),
        db_index=True,
        null=False,
        blank=False
    )
    # oversight_records = models.ManyToManyField(
    #     to=OversightRecord,
    #     verbose_name=_("oversight records"),
    #     related_name="entry_records",
    #     db_index=True
    # )

    # timestamp = models.DateTimeField(
    #     verbose_name=_("timestamp"),
    #     auto_now_add=True,
    #     db_index=True
    # )
    def service(self):
        return self.content.service()

    def field_details(self):
        return self.field

    def __str__(self):
        value = self.value
        if len(value) > 40:
            value = value[:40] + '...'

        return f'{self.field.name}: <{value}>'

    class Meta:
        verbose_name = _("entry")
        verbose_name_plural = _("entries")
        db_table = 'covid19"."cms_entry'

        # unique_together = [
        #     ("content", "order"),
        # ]

        indexes = [
            models.Index(
                fields=("content", "order"),
                name="ordered_entries"
            )
        ]

        ordering = ("content", "order")

#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
import re
from django.utils.translation import gettext as _

# 3rd party:
from django.db import models

# Internal: 
from ..utils.default_generators import generate_unique_id
from .fields import VarCharField


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


URI_PATTERN = re.compile(r"[A-Za-z0-9,'.\s\-()<>!=/]+")


def url_validator(value):
    if URI_PATTERN.match(value):
        return True

    return False


class Page(models.Model):
    id = models.UUIDField(
        verbose_name=_("unique ID"),
        primary_key=True,
        editable=False,
        default=generate_unique_id
    )
    title = VarCharField(max_length=120, null=False, blank=False, db_index=True, unique=True)
    uri = VarCharField(
        max_length=150,
        validators=[url_validator],
        null=False,
        blank=False
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'covid19"."page'
        verbose_name = _("page")

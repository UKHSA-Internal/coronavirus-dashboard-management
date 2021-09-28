#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
import re

# 3rd party:
from django.db import models
from django.utils.translation import gettext as _

# Internal:
from ..fields import VarCharField
from ...utils.default_generators import generate_unique_id

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    # 'PageURI'
]


URI_PATTERN = re.compile(r"[A-Za-z0-9,'.\s\-()<>!=/]+")


def url_validator(value):
    if URI_PATTERN.match(value):
        return True

    return False


# class PageURI(models.Model):
#     id = VarCharField(
#         verbose_name=_("unique ID"),
#         max_length=36,
#         primary_key=True,
#         default=generate_unique_id
#     )
#     page_name = VarCharField(max_length=100, blank=False, null=False)
#     display_uri = VarCharField(
#         max_length=150,
#         validators=[url_validator],
#         null=False,
#         blank=False
#     )
#
#     class Meta:
#         db_table = 'covid19"."page_uri'
#         verbose_name = _("Page URI")

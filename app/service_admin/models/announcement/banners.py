#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from uuid import uuid4

# 3rd party:
from django.db import models
from django.utils.translation import gettext as _

from markdownx.models import MarkdownxField

# Internal:
from ..data import AreaReference
# from ..shared_models import PageURI
from ..fields import VarCharField
from ...utils.default_generators import generate_unique_id
from ..page import Page

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'Announcement'
]


class Announcement(models.Model):
    id = models.UUIDField(
        verbose_name=_("unique ID"),
        primary_key=True,
        editable=False,
        default=generate_unique_id
    )
    appear_by_update = models.DateField(
        verbose_name=_("appear by update"),
        null=False,
        blank=False,
        db_index=True
    )
    disappear_by_update = models.DateField(
        verbose_name=_("disappear by update"),
        null=False,
        blank=False,
        db_index=True
    )
    date = models.DateField(
        verbose_name=_("date"),
        null=True,
        blank=False
    )
    pages = models.ManyToManyField(
        Page,
        through="BannerPage",
        through_fields=["announcement", "page"]
    )
    # relative_urls = models.ManyToManyField(PageURI)
    # applicable_areas = models.ManyToManyField(
    #     AreaReference,
    #     through='BannerArea',
    #     through_fields=["announcement", "area"]
    # )
    body = MarkdownxField(
        verbose_name=_("body"),
        blank=False,
        max_length=200
    )

    class Meta:
        db_table = 'covid19"."announcement'
        verbose_name = _("Announcement")


class BannerPage(models.Model):
    id = models.UUIDField(
        verbose_name=_("unique ID"),
        primary_key=True,
        editable=False,
        default=generate_unique_id
    )
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)

    class Meta:
        db_table = 'covid19"."banner_page'
        verbose_name = _("banner page")


# class BannerArea(models.Model):
#     id = models.UUIDField(
#         verbose_name=_("unique ID"),
#         primary_key=True,
#         editable=False,
#         default=generate_unique_id
#     )
#     announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
#     area = models.ForeignKey(AreaReference, to_field='area_code', on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = 'covid19"."banner_area'
#         verbose_name = _("banner area")

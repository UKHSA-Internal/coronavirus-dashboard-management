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
from ..tags import Tag
# from ..shared_models import PageURI
from ..fields import VarCharField
from ...utils.default_generators import generate_unique_id
from ..page import Page

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'Announcement',
    'BannerTag'
]


class Announcement(models.Model):
    type_choices = [
        ("BANNER", _("Banner")),
        ("LOG", _("Log")),
    ]

    id = models.UUIDField(
        verbose_name=_("unique ID"),
        primary_key=True,
        editable=False,
        default=generate_unique_id
    )
    type = VarCharField(
        verbose_name=_("announcement type"),
        null=False,
        blank=False,
        max_length=10,
        choices=type_choices
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
    released = models.BooleanField(
        verbose_name=_("released"),
        null=False,
        blank=False,
        default=False
    )
    pages = models.ManyToManyField(
        Page,
        related_name='page_announcements',
        through="BannerPage",
        through_fields=["announcement", "page"]
    )
    areas = models.ManyToManyField(
        AreaReference,
        related_name='area_announcements',
        through="BannerArea",
        through_fields=["announcement", "area"]
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
        max_length=250
    )
    heading = MarkdownxField(
        verbose_name=_("heading"),
        null=True,
        max_length=120,
        help_text=_("Log heading - only used when announcement type is set to \"log\".")
    )
    details = MarkdownxField(
        verbose_name=_("details"),
        null=True,
        help_text=_("Additional information - only used when announcement type is set to \"log\".")
    )
    announcement_tags = models.ManyToManyField(
        'Tag',
        verbose_name=_("tags"),
        related_name="tag_announcements",
        through="BannerTag",
        through_fields=["announcement", "tag"]
    )

    class Meta:
        managed = False
        db_table = 'covid19"."announcement'
        verbose_name = _("Announcement")


class BannerTag(models.Model):
    id = models.UUIDField(
        verbose_name=_("unique ID"),
        primary_key=True,
        editable=False,
        default=generate_unique_id
    )
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        limit_choices_to={"association": "LOGS"}
    )

    class Meta:
        managed = False
        db_table = 'covid19"."banner_tag'
        verbose_name = _("banner tag")


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
        managed = False
        db_table = 'covid19"."banner_page'
        verbose_name = _("banner page")


class BannerArea(models.Model):
    id = models.UUIDField(
        verbose_name=_("unique ID"),
        primary_key=True,
        editable=False,
        default=generate_unique_id
    )
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    area = models.ForeignKey(
        AreaReference,
        db_column='area',
        to_field='unique_ref',
        on_delete=models.CASCADE,
        limit_choices_to=~models.Q(area_type__icontains="msoa")
    )

    class Meta:
        managed = False
        db_table = 'covid19"."banner_area'
        verbose_name = _("banner area")


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

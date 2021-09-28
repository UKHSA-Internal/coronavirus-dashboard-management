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
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.models import User

from reversion import register as reversion_register
# from app.service_admin.models.page import Page
from django.urls import reverse_lazy
from rest_framework.reverse import reverse_lazy as drf_reverse_lazy

# from rest_framework.urls import
from guardian.shortcuts import get_objects_for_user

# Internal:
# from .section import Section
# from .activity_log import OversightRecord, Activity

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Header
__author__ = "Pouria Hadjibagheri"
__copyright__ = "Copyright (c) 2020, Public Health England"
__license__ = "MIT"
__version__ = "0.0.1"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'Content'
]
from uuid import uuid4

# class ContentQuerySet(models.QuerySet):
#     def awaiting_review(self):
#         qs = OversightRecord.objects.get_awaiting_review(Content)
#         return self.filter(pk__in=qs.values('object_id'))
#
#     def published(self):
#         qs = OversightRecord.objects.get_published_for(Content)
#         return self.filter(pk__in=qs.values('object_id'))

    # def all_permitted(self, user, edit=False, delete=False, modify=False, review=False):
    #     qs = self.all()
    #     qs = get_objects_for_user(
    #         user=user,
    #         klass=qs,
    #         perms=[]
    #     )


# class ContentManager(models.Manager):
#     def get_queryset(self):
#         return ContentQuerySet(self.model, using=self._db)
#
#     def published(self):
#         return self.get_queryset().published()
#
#     def awaiting_review(self):
#         return self.get_queryset().awaiting_review()


@reversion_register()
class Content(models.Model):
    uuid = models.UUIDField(
        editable=False,
        null=False,
        blank=False,
        unique=True,
        db_index=True
    )
    label = models.CharField(
        verbose_name=_("label"),
        max_length=64,
        db_index=True,
        blank=False
    )
    page = models.ForeignKey(
        verbose_name=_("section"),
        to="service_admin.Page",
        limit_choices_to={"data_category": True},
        related_name="contents",
        on_delete=models.CASCADE,
        null=False,
        db_index=True
    )
    child_of = models.ForeignKey(
        verbose_name=_("child of"),
        to="self",
        related_name="children",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    slug = models.SlugField(
        blank=False,
        null=False,
        db_index=True,
        help_text=_(
            "URL name for the content: "
            "This is utilised to construct the URL for service admin and the API. "
            "May only contain characters, numbers, - (hyphen) or _ (underscore)."
        ),
    )
    # oversight_records = models.ManyToManyField(
    #     to=OversightRecord,
    #     verbose_name=_("oversight records"),
    #     related_name="content_records",
    #     db_index=True
    # )

    # objects = ContentManager()

    def __str__(self):
        return self.label

    def service(self):
        return self.section.service

    def dashboard_url(self):
        return reverse_lazy(
            "service:dashboard-content",
            kwargs={
                "service": self.section.service.slug,
                "section": self.section.slug,
                "content": self.slug
            }
        )

    class Meta:
        verbose_name = _("content")
        verbose_name_plural = _("contents")
        db_table = 'covid19"."cms_content'


        unique_together = [
            ("label", "section", "child_of"),
            ("slug", "section")
        ]

        indexes = [
            models.Index(
                fields=("section", "slug"),
                name="section_content_slug_idx"
            ),
            models.Index(
                fields=("section", "label"),
                name="section_content_idx"
            )
        ]

        ordering = ("pk",)

    # class Versioning:
    #     publication_date = 'timestamp'
    #     clear_each_revision = [
    #         'change_log',
    #         'published_by',
    #         'reviewed_by'
    #     ]

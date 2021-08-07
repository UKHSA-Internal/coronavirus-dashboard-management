#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from uuid import uuid4

# 3rd party:
from django.db import models
from django.utils.translation import gettext as _
from django.db.models import CheckConstraint
from markdownx.models import MarkdownxField

from reversion import register as versioned

# Internal:

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'Announcement',
]


@versioned()
class Announcement(models.Model):
    id = models.UUIDField(
        verbose_name=_("unique ID"),
        primary_key=True,
        editable=False,
        default=uuid4
    )
    launch = models.DateTimeField(
        verbose_name=_("appear by update"),
        null=False,
        blank=False,
        db_index=True
    )
    expire = models.DateTimeField(
        verbose_name=_("disappear by update"),
        null=False,
        blank=False,
        db_index=True
    )
    date = models.DateField(
        verbose_name=_("date"),
        null=True,
        blank=True,
        help_text=_("Must be between 'launch' and 'expire'.")
    )
    deploy_with_release = models.BooleanField(
        verbose_name=_("deploy with release"),
        null=False,
        blank=False,
        default=True,
        help_text=_(
            "Deploy only when launch date of the announcement is smaller than or equal "
            "to the maximum 'receipt date' of released data."
        )
    )
    remove_with_release = models.BooleanField(
        verbose_name=_("remove with release"),
        null=False,
        blank=False,
        default=True,
        help_text=_(
            "Remove only when expire date of the announcement is smaller than or equal "
            "to the maximum 'receipt date' of released data."
        )
    )
    body = MarkdownxField(
        verbose_name=_("body"),
        blank=False,
        max_length=400,
        help_text=_(
            "Markdown enabled. Announcement banners are available through the public API "
            "as raw text. Minimise the use markdown to avoid confusion."
        )
    )

    class Meta:
        managed = False
        db_table = 'covid19"."announcement'
        verbose_name = _("Announcement")
        constraints = [
            CheckConstraint(
                name="chk__anc_exp_gt_launch",
                check=models.Q(launch__lte=models.F("expire"))
            ),
            CheckConstraint(
                name="chk__anc_date_bw_launch_exp",
                check=models.Q(
                    models.Q(launch__date__lte=models.F("date")) &
                    models.Q(expire__date__gte=models.F("date"))
                )
            ),
        ]
        indexes = [
            models.Index(
                name="idx__anc_launch_expire",
                fields=['launch', 'expire']
            )
        ]
        ordering = [
            "-launch",
            "expire"
        ]

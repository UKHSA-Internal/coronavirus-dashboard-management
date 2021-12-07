#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from uuid import uuid4

# 3rd party:
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

from reversion import register as versioned

# Internal: 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'ReportRecipient'
]


@versioned()
class ReportRecipient(models.Model):
    id = models.UUIDField(
        verbose_name=_("unique ID"),
        primary_key=True,
        editable=False,
        default=uuid4
    )

    recipient = models.EmailField(
        verbose_name=_("Recipient's email"),
        max_length=255,
        null=False,
        unique=True,
        help_text=_("This field is not editable.")
    )

    note = models.TextField(
        verbose_name=_("Note"),
        null=True,
        help_text=_("May include the request, justification, or the position of the recipient.")
    )

    date_added = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        null=False
    )

    created_by = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=False,
        related_name='recipient_added_by',
        db_column="created_by",
        editable=False,
        limit_choices_to={
            models.Q(groups__name="add_email_recipients")
        },
    )

    approved_by = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=True,
        related_name='recipient_approved_by',
        db_column="approved_by",
        limit_choices_to={
            models.Q(groups__name="approve_email_recipients")
        }
    )

    def __str__(self):
        return self.recipient

    def creator(self):
        return self.created_by.get_full_name()

    def approver(self):
        if self.approved_by is not None:
            return self.approved_by.get_full_name()

    class Meta:
        managed = False
        db_table = 'covid19"."report_recipients'
        verbose_name = _("Report recipient")
        verbose_name_plural = _("Report recipients")

        permissions = (
            ('can_approve_report_recipient', _('Can approve report recipient')),
        )

        constraints = (
            models.CheckConstraint(
                check=~models.Q(created_by=models.F("approved_by")),
                name="chk__rep_rec_approver_not_creator"
            ),
        )

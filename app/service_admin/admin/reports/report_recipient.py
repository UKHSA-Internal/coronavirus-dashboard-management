#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from json import dumps

# 3rd party:
from django.contrib import admin
from django.utils.translation import gettext as _
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages

from reversion.admin import VersionAdmin

# Internal:
from service_admin.models import ReportRecipient

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'ReportRecipientAdmin'
]


def approve_recipients(modeladmin, request, queryset):
    if not request.user.has_perm('service_admin.can_approve_report_recipient'):
        return messages.error(request, _("You do not have permission to approve new recipients."))

    if queryset.filter(created_by=request.user).exists():
        return messages.error(request, _("You cannot approve a recipient added by yourself."))

    n_updated = 0
    for item in queryset:
        item.approved_by = request.user
        item.save()

        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(item).pk,
            object_id=item.id,
            object_repr=item.recipient,
            action_flag=CHANGE,
            change_message=dumps([{
                "description": "recipient approved"
            }])
        )

        n_updated += 1

        return messages.success(request, _("Successfully approved %d recipients.") % n_updated)


approve_recipients.short_description = _(f"Approve selected recipients")


@admin.register(ReportRecipient)
class ReportRecipientAdmin(VersionAdmin):
    search_fields = ('recipient',)
    list_per_page = 30
    readonly_fields = [
        "date_added",
        "id",
    ]
    actions = [
        approve_recipients
    ]
    list_filter = [
        ('approved_by', admin.BooleanFieldListFilter,),
        ('deactivated', admin.BooleanFieldListFilter,),
        ('created_by', admin.RelatedOnlyFieldListFilter,),
    ]
    list_display = [
        'recipient',
        'date_added',
        'creator',
        'approver',
        'deactivated',
        'id',
    ]

    list_display_links = [
        'recipient',
    ]

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'id',
                    'recipient',
                    'note',
                    'deactivated',
                ),
            },
        ),
    )

    def get_changeform_initial_data(self, request):
        get_data = super().get_changeform_initial_data(request)
        get_data['created_by'] = request.user.pk

        return get_data

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)

        if request.user.has_perm("service_admin.can_deactivate_report_recipient"):
            return fields

        return [*fields, "deactivated"]

    def save_form(self, request, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change:
            instance.created_by = user
        else:
            data = ReportRecipient.objects.get(pk=instance.id)
            instance.created_by = data.created_by

            if instance.recipient != data.recipient:
                return messages.error(request, "Recipient's email cannot be modified.")

        instance.save()

        return instance

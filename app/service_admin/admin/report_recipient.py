#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:

# 3rd party:
from django.contrib import admin
from django.core.exceptions import ValidationError
from reversion.admin import VersionAdmin

# Internal: 
from .generic_admin import GuardedAdmin
from service_admin.models import ReportRecipient

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'ReportRecipientAdmin'
]


def approve_recipients(modeladmin, request, queryset):
    if request.user.has_perm('reportrecipient.can_approve_report_recipient'):
        for item in queryset:
            if item.created_by == request.user:
                raise ValidationError("You cannot approve a recipient added by yourself.")

        queryset.update(approved_by=request.user)
    else:
        raise ValidationError("You do not have permission to approve new recipients.")


approve_recipients.short_description = f"Approve selected recipients"


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

        if request.user.has_perm("reportrecipient.can_deactivate_report_recipient"):
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
                raise ValidationError("Recipient's email cannot be modified.")

        instance.save()

        return instance

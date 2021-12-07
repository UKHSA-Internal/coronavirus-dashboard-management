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
class ReportRecipientAdmin(VersionAdmin, GuardedAdmin):
    search_fields = ('email',)
    readonly_fields = [
        "date_added",
        "id",
    ]
    actions = [
        approve_recipients
    ]
    list_display = [
        'id',
        'recipient',
        'date_added',
        'creator',
        'approver',
    ]

    list_display_links = [
        'id',
    ]

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'id',
                    'recipient',
                    'note',
                ),
            },
        ),
    )

    def get_changeform_initial_data(self, request):
        get_data = super().get_changeform_initial_data(request)
        get_data['created_by'] = request.user.pk

        return get_data

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


#     @admin.display(
#         boolean=False,
#         ordering='-type',
#         description='Type',
#     )
#     def created_by(self, obj):
#         obj.
#         colours = obj.get_type_colours()
#         bg_colour = colours.get("background", "transparent")
#         text_colour = colours.get("text", "#000000")
#         return mark_safe(f'''\
# <span class="table-tag" \
#  style="margin-right: 2px; margin-bottom: 2px; font-size: x-small; color: {text_colour}; background: {bg_colour}">\
# {obj.type.tag.upper().replace(" ", "&nbsp;")}\
# </span>''')

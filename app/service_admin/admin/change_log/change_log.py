#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from uuid import uuid4
from datetime import datetime

# 3rd party:
from django.contrib import admin
from django.utils.safestring import mark_safe
from reversion.admin import VersionAdmin
from django.utils.translation import gettext as _

# Internal: 
from service_admin.models.change_log import ChangeLog
from .forms import ChangeLogAdminFrom
from .inlines import ChangeLogPagesAdmin, ChangeLogMetricsAdmin

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'ChangeLogAdmin'
]


def clone_objects(modeladmin, request, queryset):
    for item in queryset:
        change_log = ChangeLog(
            date=datetime.utcnow(),
            heading=item.heading,
            body=item.body,
            details=item.details,
            high_priority=item.high_priority,
            display_banner=item.display_banner,
            type=item.type,
            area=item.area
        )

        change_log.save()

        change_log.metrics.add(*item.metrics.all())

        change_log.pages.add(*item.pages.all())


clone_objects.short_description = _("Duplicate entries with today's date")


@admin.register(ChangeLog)
class ChangeLogAdmin(VersionAdmin):
    list_per_page = 20

    search_fields = [
        'heading'
    ]

    actions = [clone_objects]

    readonly_fields = [
        'id',
        'timestamp_created'
    ]

    list_display = [
        "heading",
        "date",
        "expiry",
        "display_banner",
        "high_priority",
        "log_type",
    ]

    list_filter = [
        ('display_banner', admin.BooleanFieldListFilter),
        ('high_priority', admin.BooleanFieldListFilter),
        ('date', admin.DateFieldListFilter),
        ('type', admin.RelatedOnlyFieldListFilter),
    ]

    form = ChangeLogAdminFrom

    inlines = [
        ChangeLogPagesAdmin,
        ChangeLogMetricsAdmin
    ]

    fieldsets = (
        (
            None,
            {
                'fields': (
                    ('id', 'timestamp_created'),
                    'type',
                    ('display_banner', 'high_priority'),
                    ('date', 'expiry'),
                    'heading',
                ),
            },
        ),
        (
            "Log content",
            {
                "fields": (
                    "body",
                    "details"
                )
            }
        ),
        (
            "Area associations",
            {
                "fields": (
                    'area',
                )
            }
        )
    )

    @admin.display(
        boolean=False,
        ordering='-type',
        description='Type',
    )
    def log_type(self, obj):
        colours = obj.get_type_colours()
        bg_colour = colours.get("background", "transparent")
        text_colour = colours.get("text", "#000000")
        return mark_safe(f'''\
<span class="table-tag" \
 style="margin-right: 2px; margin-bottom: 2px; font-size: x-small; color: {text_colour}; background: {bg_colour}">\
{obj.type.tag.upper().replace(" ", "&nbsp;")}\
</span>''')

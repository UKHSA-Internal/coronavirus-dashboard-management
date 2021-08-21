#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:

# 3rd party:
from django.contrib import admin
from django.utils.safestring import mark_safe
from reversion.admin import VersionAdmin

# Internal: 
from service_admin.models.change_log import ChangeLog
from .forms import ChangeLogAdminFrom
from .inlines import ChangeLogPagesAdmin, ChangeLogMetricsAdmin

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'ChangeLogAdmin'
]


@admin.register(ChangeLog)
class ChangeLogAdmin(VersionAdmin):
    list_per_page = 20

    search_fields = [
        'heading'
    ]

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

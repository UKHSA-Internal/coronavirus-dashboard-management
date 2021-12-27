#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from datetime import datetime
from json import dumps

# 3rd party:
from django.contrib import admin
from django.utils.safestring import mark_safe
from reversion.admin import VersionAdmin
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
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
    now = datetime.utcnow()
    for item in queryset:
        change_log = ChangeLog(
            date=now,
            heading=item.heading,
            body=item.body,
            details=item.details,
            high_priority=item.high_priority,
            display_banner=item.display_banner,
            type=item.type,
            area=item.area
        )

        change_log.save()

        metrics = item.metrics.all()
        change_log.metrics.add(*metrics)

        change_log.pages.add(*item.pages.all())

        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(change_log).pk,
            object_id=item.id,
            object_repr=item.heading,
            action_flag=ADDITION,
            change_message=dumps([{
                "category": "duplicated",
                "duplication_of": str(item.pk),
                "metrics_transferred": len(metrics),
                "original_date": item.date.isoformat(),
                "new_date": now.isoformat()
            }])
        )


clone_objects.short_description = _("Duplicate entries with today's date")


@admin.register(ChangeLog)
class ChangeLogAdmin(VersionAdmin):
    list_per_page = 50

    search_fields = [
        'heading'
    ]
    date_hierarchy = 'date'

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

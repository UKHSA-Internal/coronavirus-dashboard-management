#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from json import dumps

# 3rd party:
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib import messages
from django.db import connection

# Internal: 
from .queries import STATS_QUERY, PERMISSIONS_QUERY

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'recalculate_selected_count'
]


def recalculate_selected_count(modeladmin, request, queryset):
    if not any([
        request.user.is_superuser,
        request.user.has_perm('service_admin.change_releasestats')
    ]):
        return messages.error(request, _("You do not have permission to request recalculation."))

    recalculated = list()
    with connection.cursor() as cursor:
        cursor.execute(PERMISSIONS_QUERY)

        for item in queryset:
            receipt_time = item.timestamp
            partition_ids = [
                f"{receipt_time:%-d_%-m_%y}|other",
                f"{receipt_time:%-d_%-m_%y}|utla",
                f"{receipt_time:%-d_%-m_%y}|ltla",
                f"{receipt_time:%-d_%-m_%y}|msoa",
                f"{receipt_time:%-d_%-m_%y}|nhstrust",
            ]
            category = item.category.process_name
            recalculated.append(f"{category} ({item.timestamp:%-d %b %Y})")

            cursor.execute(STATS_QUERY, [partition_ids, category])

            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(item.releasestats).pk,
                object_id=item.releasestats.pk,
                object_repr=str(item.releasestats.record_count),
                action_flag=CHANGE,
                change_message=dumps([{
                    "description": "recalculated count and set permissions",
                    "receipt_time": receipt_time.isoformat(),
                    "category": category,
                }])
            )

    return messages.success(request, _(f"Successfully recalculated: %s") % str.join(', ', recalculated))


recalculate_selected_count.short_description = _(f"Recalculate count and delta for selected items")

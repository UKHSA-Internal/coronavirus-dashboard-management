#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from json import dumps

# 3rd party:
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, CHANGE, ADDITION, DELETION
from django.contrib import messages
from django.db import connection

# Internal: 
from .queries import STATS_QUERY, PERMISSIONS_QUERY

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'recalculate_selected_count',
    'reset_release_stats'
]


def recalculate_selected_count(modeladmin, request, queryset):
    if not request.user.has_perm('service_admin.change_releasestats'):
        return messages.error(
            request,
            _("You do not have permission to request recalculation. Operation aborted.")
        )

    with connection.cursor() as cursor:
        cursor.execute(PERMISSIONS_QUERY)

        for item in queryset:
            receipt_time = item.timestamp
            partition_ids = [
                f"{receipt_time:%Y_%-m_%-d}|other",
                f"{receipt_time:%Y_%-m_%-d}|utla",
                f"{receipt_time:%Y_%-m_%-d}|ltla",
                f"{receipt_time:%Y_%-m_%-d}|msoa",
                f"{receipt_time:%Y_%-m_%-d}|nhstrust",
            ]
            category = item.category.process_name

            cursor.execute(STATS_QUERY, [partition_ids, category])
            print(partition_ids, category)

            obj = item
            obj_repr = str(item)
            obj_id = item.pk
            action_flag = ADDITION

            if hasattr(item, 'releasestats'):
                obj = item.releasestats
                obj_repr = str(item.releasestats.record_count)
                obj_id = item.releasestats.pk
                action_flag = CHANGE

                messages.success(
                    request,
                    _(f"Successfully recalculated: %s") % f"{category} ({item.timestamp:%-d %b %Y})"
                )
            else:
                messages.success(
                    request,
                    _(f"Successfully calculated: %s") % f"{category} ({item.timestamp:%-d %b %Y})"
                )

            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(obj).pk,
                object_id=obj_id,
                object_repr=obj_repr,
                action_flag=action_flag,
                change_message=dumps([{
                    "description": "recalculated count and set permissions",
                    "receipt_time": receipt_time.isoformat(),
                    "category": category,
                }])
            )


recalculate_selected_count.short_description = _(f"Recalculate count and delta for selected items")


def reset_release_stats(modeladmin, request, queryset):
    if not request.user.has_perm('service_admin.change_releasestats'):
        return messages.error(
            request,
            _("You do not have permission to request recalculation. Operation aborted.")
        )

    for item in queryset:
        if not hasattr(item, 'releasestats'):
            messages.warning(
                request,
                _(f"No release statistics exist for '%s' on %s.") % (
                    item.category.process_name,
                    str(item)
                )
            )

            continue

        category = item.category.process_name
        receipt_time = item.timestamp

        count = item.releasestats.record_count
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(item.releasestats).pk,
            object_id=item.releasestats.pk,
            object_repr=str(count),
            action_flag=DELETION,
            change_message=dumps([{
                "description": "reset count and delta",
                "receipt_time": receipt_time.isoformat(),
                "deleted_count": count,
                "category": category,
                "deleted_delta": item.delta()
            }])
        )

        item.releasestats.delete()

        messages.success(
            request,
            _(f"Successfully reset: %s") % f"{category} [{item}]"
        )


reset_release_stats.short_description = _(f"Reset release statistics for selected items")

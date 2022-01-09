#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from json import dumps
from datetime import datetime

# 3rd party:
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, CHANGE, ADDITION, DELETION
from django.contrib import messages
from django.conf import settings

from azure.servicebus import ServiceBusClient, ServiceBusMessage

# Internal:
from service_admin.models import ProcessedFile
from .utils import get_minute_instance_id

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'reporocess_release',
]

TOPIC_NAME = "generic_tasks"
RESUBMIT_PROCESS = "GENERIC_TASKS"
FUNC_NAME = "main_etl_orchestrator"


def reporocess_release(modeladmin, request, queryset):
    if not request.user.has_perm('service_admin.change_releasereference'):
        return messages.error(
            request,
            _("You do not have permission to request a release to be reprocessed. Operation aborted.")
        )

    if (count := queryset.count()) > 1:
        return messages.error(
            request,
            _("You can only submit one release for reprocessing. Found %d selected items.") % count
        )

    now = datetime.utcnow()
    for item in queryset:
        category = item.category.process_name

        file = ProcessedFile.objects.filter(release_id=item.pk)
        old_path = file.file_path

        messages.info(
            request,
            _(f'Data file for "%s" associated with the release: "%s"') % (category, old_path)
        )

        new_path = old_path + f"-RESUBMIT:{now.isoformat()}"
        file.file_path = new_path
        file.update()

        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(ProcessedFile).pk,
            object_id=file.id,
            object_repr=str(file),
            action_flag=CHANGE,
            change_message=dumps([{
                "category": "Renamed file for reprocessing.",
                "old_name": old_path,
                "new_name": new_path
            }])
        )

        messages.info(
            request,
            _(f"File renamed to: %s") % new_path
        )

        # Reset release stats:
        if not hasattr(item, 'releasestats'):
            messages.warning(
                request,
                _(f"No release statistics exist for '%s' on %s.") % (
                    item.category.process_name,
                    str(item)
                )
            )
        else:
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

            messages.info(
                request,
                _(f"Release statistics reset for '%s' on %s.") % (
                    item.category.process_name,
                    str(item)
                )
            )

        # Trigger ETL
        payload = dumps({
            "to": RESUBMIT_PROCESS,
            "fileName": old_path,
            "ENVIRONMENT": settings.API_ENV,
            "timestamp": datetime.utcnow().isoformat(),
        })

        msg = ServiceBusMessage(
            body=payload,
            session_id=request.session.session_key,
            to=RESUBMIT_PROCESS,
            subject=FUNC_NAME,
            message_id=get_minute_instance_id(RESUBMIT_PROCESS)
        )

        with ServiceBusClient.from_connection_string(settings.SERVICE_BUS_CREDENTIALS,
                                                     logging_enable=True) as sb_client:
            with sb_client.get_topic_sender(topic_name=TOPIC_NAME) as sender:
                sender.send_messages(msg)

        messages.success(request, _(f"ETL has been trigger to reprocess the data file."))


reporocess_release.short_description = _(f"Submit selected item to ETL for reprocessing")

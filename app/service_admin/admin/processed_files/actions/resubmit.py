#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from os.path import splitext
from datetime import datetime
from json import dumps

# 3rd party:
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib import messages

# Internal:
from storage import StorageClient

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    "resubmit_file",
    "resubmit_file_for_today",
]

CONTAINER = "rawdbdata"


def resubmit_file(modeladmin, request, queryset):
    if not request.user.has_perm('service_admin.add_processedfile'):
        return messages.error(
            request,
            _("You do not have permission to resubmit source files. Operation aborted.")
        )

    if queryset.count() > 1:
        return messages.error(
            request,
            _("You can only request one resubmission at a time. Operation aborted.")
        )

    for item in queryset:
        file_path: str = item.file_path

        with StorageClient(container=CONTAINER, path=file_path) as cli:
            if not cli.exists():
                return messages.error(request, _("File not found. It has either been removed or archived."))

            now = datetime.utcnow()
            file_timestamp, __ = splitext(file_path.rsplit("_", 1)[1])

            # Only replace the time section of the timestamp.
            file_date = file_timestamp[:-4]
            new_filename = f"{file_date}{now:%H%M}"
            new_path = file_path.replace(file_timestamp, new_filename)

            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(item).pk,
                object_id=item.pk,
                object_repr=file_path,
                action_flag=ADDITION,
                change_message=dumps([{
                    "description": "resubmitted file for ETL processing",
                    "timestamp": now.isoformat(),
                    "category": item.type,
                    "resubmitted_path": new_path
                }])
            )

            cli.copy_blob(target_container=CONTAINER, target_path=new_path)

            return messages.success(
                request,
                _('Resubmitted "%s" as "%s". ETL process will be triggered shortly.') % (file_path, new_path)
            )


resubmit_file.short_description = _(f"Resubmit file for ETL processing")


def resubmit_file_for_today(modeladmin, request, queryset):
    if not request.user.has_perm('service_admin.change_releasereference'):
        return messages.error(
            request,
            _("You do not have permission to resubmit source files as today's data. Operation aborted.")
        )

    if queryset.count() > 1:
        return messages.error(request, _("You can only request one resubmission at a time."))

    for item in queryset:
        file_path: str = item.file_path

        with StorageClient(container=CONTAINER, path=file_path) as cli:
            if not cli.exists():
                return messages.error(request, _("File not found. It has either been removed or archived."))

            now = datetime.utcnow()
            file_timestamp, __ = splitext(file_path.rsplit("_", 1)[1])

            # Only replace the time section of the timestamp.
            new_path = file_path.replace(file_timestamp, f"{file_timestamp[:-4]}{now:%H%M}")
            old_date = datetime.strptime(new_path.split("/")[0], "%Y-%m-%d")
            new_path = (
                new_path
                .replace(f"{old_date:%Y-%m-%d}", f"{now:%Y-%m-%d}")
                .replace(f"{old_date:%Y%m%d}", f"{now:%Y%m%d}")
            )

            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(item).pk,
                object_id=item.pk,
                object_repr=file_path,
                action_flag=ADDITION,
                change_message=dumps([{
                    "description": "resubmitted file for processing as today's data",
                    "timestamp": now.isoformat(),
                    "category": item.type,
                    "resubmitted_path": new_path
                }])
            )

            cli.copy_blob(target_container=CONTAINER, target_path=new_path)

            return messages.success(
                request,
                _('Resubmitted "%s" as "%s". ETL process will be triggered shortly.') % (file_path, new_path)
            )


resubmit_file_for_today.short_description = _(f"Resubmit file for processing as today's data")

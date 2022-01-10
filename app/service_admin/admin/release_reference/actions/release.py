#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from datetime import datetime, timedelta
from json import dumps
from logging import getLogger

# 3rd party:
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, CHANGE, ADDITION, DELETION
from django.forms import Form
from django.forms import CharField, DateField, DateInput, TextInput
from django.contrib import messages
from django.conf import settings
from django.core.exceptions import ValidationError

from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.servicebus.exceptions import ServiceBusError

# Internal: 
from service_admin.models import Despatch, DespatchToRelease
from service_admin.utils.presets import ServiceName
from .utils import confirm_release, get_minute_instance_id

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'release_selected'
]


TOPIC_NAME = "data-despatch"
SERVICE_NAME = getattr(ServiceName, settings.ENVIRONMENT)

logger = getLogger("django")


class ConfirmDespatchForm(Form):
    title = _(f'Despatch selected releases to %s') % SERVICE_NAME.capitalize()
    environment_name = CharField(
        max_length=len(settings.ENVIRONMENT),
        help_text="Case insensitive",
        widget=TextInput(attrs=dict(
            autocomplete='off'
        ))
    )
    release_date = DateField(
        help_text=(
            "Select a date that matches the date for all "
            "of the items you are attempting to despatch."
        ),
        widget=DateInput(attrs={'type': 'date'})
    )

    def __init__(self, *args, data_dates, **kwargs):
        self.data_dates = data_dates
        super(ConfirmDespatchForm, self).__init__(*args, **kwargs)

    def clean_environment_name(self):
        data = self.cleaned_data['environment_name']

        if data.lower() != SERVICE_NAME.lower():
            raise ValidationError("Environment name does not match.")

        return data

    def clean_release_date(self):
        data = self.cleaned_data['release_date']
        data = f"{data:%Y-%m-%d}"

        for item in self.data_dates:
            if item != data:
                raise ValidationError(f"The date you entered does not match the data date of '{item}'.")

        return data


@confirm_release(ConfirmDespatchForm)
def release_selected(modeladmin, request, queryset):
    if settings.DEBUG:
        return messages.error(request, _(f"This feature is unavailable in debug mode."))

    if not request.user.has_perm('service_admin.change_releasereference'):
        return messages.error(
            request,
            _("You do not have permission to despatch. Operation aborted.")
        )

    timestamp = datetime.utcnow()
    time_past_the_hour = timedelta(
        minutes=timestamp.minute,
        seconds=timestamp.second,
        microseconds=timestamp.microsecond
    )
    prev_hour = timestamp - time_past_the_hour
    next_hour = prev_hour + timedelta(hours=1)
    queryset.update(released=True)

    despatch = Despatch.objects.filter(timestamp__gte=prev_hour, timestamp__lte=next_hour).first()
    if despatch is None:
        despatch = Despatch.objects.create(timestamp=timestamp)

    LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(despatch).pk,
        object_id=despatch.id,
        object_repr=timestamp.isoformat(),
        action_flag=ADDITION,
        change_message=dumps([
            {"category": "data despatched", "timestamp": timestamp.isoformat(), "released_object_id": str(release.id)}
            for release in queryset
        ])
    )

    new_objects = list()
    for release in queryset:
        old_releases = DespatchToRelease.objects.filter(release=release).all()
        for item in old_releases:
            category = item.release.category.process_name
            messages.info(
                request,
                _('Deleted release item of category "%s" with id %d') % (category, item.id)
            )

            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(item).pk,
                object_id=item.id,
                object_repr=str(item),
                action_flag=DELETION,
                change_message=dumps([{
                    "timestamp": item.release.timestamp.isoformat(),
                    "category": category,
                }])
            )
            item.delete()

        new_objects.append(DespatchToRelease(despatch=despatch, release=release))

        release_category = release.category.process_name
        messages.info(
            request,
            _(f'Despatched "%s" received on %s') % (release_category, f"{despatch.timestamp:%Y-%m-%d}")
        )

        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(release).pk,
            object_id=release.id,
            object_repr=str(release),
            action_flag=CHANGE,
            change_message=dumps([{
                "description": "despatched",
                "timestamp": timestamp.isoformat(),
                "category": release_category,
                "despatch_object_id": despatch.id
            }])
        )

    DespatchToRelease.objects.bulk_create(new_objects)

    timestamp = timestamp.isoformat()

    message = ServiceBusMessage(dumps({
        "event": "data despatched.",
        "instance_id": get_minute_instance_id(TOPIC_NAME),
        "ENVIRONMENT": settings.API_ENV,
        "timestamp": datetime.utcnow().isoformat(),
        "releaseTimestamp": timestamp
    }))

    try:
        sb_client = ServiceBusClient.from_connection_string(
            settings.SERVICE_BUS_CREDENTIALS,
            logging_enable=True
        )

        with sb_client, sb_client.get_topic_sender(topic_name=TOPIC_NAME) as sender:
            sender.send_messages(message)

    except ServiceBusError as err:
        messages.warning(request, _(f"Failed to trigger post-despatch processes."))
        logger.exception(err)

    return messages.success(
        request,
        _(f"Successfully released %d items - timestamp: %s on %s") % (
            len(new_objects),
            f"{despatch.timestamp:%H:%M:%S}",
            f"{despatch.timestamp:%A, %-d %B %Y}"
        )
    )


release_selected.short_description = _(f"Despatch selected items on {SERVICE_NAME.capitalize()}")

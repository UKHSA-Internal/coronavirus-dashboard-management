# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from json import dumps
from datetime import datetime
from logging import getLogger

# 3rd party:
from django.utils.translation import gettext as _
from django.conf import settings
from django.contrib import messages
from django.forms import Form
from django.forms import DateField, DateInput
from django.core.exceptions import ValidationError

from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.servicebus.exceptions import ServiceBusError

# Internal:
from service_admin.models import ReleaseReference
from .utils import confirm_with_date, get_minute_instance_id

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'purge_storage_cache',
]

TOPIC_NAME = "cache_flusher"

PURGE_STORAGE_CACHE = "PURGE_STORAGE_CACHE"

logger = getLogger("django")


class ConfirmPurgeForm(Form):
    title = _(f'Purge storage cache')
    release_date = DateField(
        help_text=(
            "Select the date for which you want to purge storage cache. The date must "
            "match the receipt date for at least one despatched release."
        ),
        widget=DateInput(attrs={'type': 'date'})
    )

    def clean_release_date(self):
        data = self.cleaned_data['release_date']

        if not ReleaseReference.objects.filter(timestamp__date=data, released=True).exists():
            raise ValidationError("The date you entered does not match the date for a despatched release.")

        return data


@confirm_with_date(ConfirmPurgeForm)
def purge_storage_cache(modeladmin, request, queryset):
    if not (request.user.has_perm('service_admin.change_processedfile') and
            request.user.has_perm('service_admin.change_releasereference')):
        return messages.error(
            request,
            _("You do not have permission to purge storage cache. Operation aborted.")
        )

    payload = dumps({
        "date": request.POST['release_date'],
        "to": PURGE_STORAGE_CACHE,
        "ENVIRONMENT": settings.API_ENV,
        "timestamp": datetime.utcnow().isoformat(),
    })

    msg = ServiceBusMessage(
        body=payload,
        session_id=request.session.session_key,
        to=PURGE_STORAGE_CACHE,
        message_id=get_minute_instance_id(PURGE_STORAGE_CACHE),
    )

    try:
        sb_client = ServiceBusClient.from_connection_string(
            settings.SERVICE_BUS_CREDENTIALS,
            logging_enable=True
        )

        with sb_client, sb_client.get_topic_sender(topic_name=TOPIC_NAME) as sender:
            sender.send_messages(msg)

    except ServiceBusError as err:
        messages.error(request, _(f"Failed to trigger the flusher task."))
        logger.exception(err)
        return

    messages.success(
        request,
        _("Request submitted to flush storage cache for APIv2 and Easy-Read pages on %s.") % (
            f"{request.POST['release_date']:%A, %-d %B %Y}"
        )
    )

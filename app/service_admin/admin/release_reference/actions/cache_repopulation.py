# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from json import dumps
from logging import getLogger

# 3rd party:
from django.utils.translation import gettext as _
from django.conf import settings
from django.contrib import messages
from django.db.models import Max

from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.servicebus.exceptions import ServiceBusError

# Internal:
from service_admin.models import ReleaseReference
from .utils import get_minute_instance_id

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'repopulate_cache'
]


TOPIC_NAME = "etl_operations"

REPOPULATE_CACHE = "REPOPULATE_CACHE"

logger = getLogger("django")


def repopulate_cache(modeladmin, request, queryset):
    if not request.user.has_perm('service_admin.change_releasereference'):
        return messages.error(
            request,
            _("You do not have permission to repopulate cache. Operation aborted.")
        )

    obj = ReleaseReference.objects.filter(released=True).aggregate(Max('timestamp'))

    payload = dumps({
        "ENVIRONMENT": settings.API_ENV,
        "to": REPOPULATE_CACHE,
        "timestamp": obj['timestamp__max'].isoformat(),
    })

    msg = ServiceBusMessage(
        body=payload,
        session_id=request.session.session_key,
        to=REPOPULATE_CACHE,
        message_id=get_minute_instance_id(REPOPULATE_CACHE)
    )

    try:
        sb_client = ServiceBusClient.from_connection_string(
            settings.SERVICE_BUS_CREDENTIALS,
            logging_enable=True
        )

        with sb_client, sb_client.get_topic_sender(topic_name=TOPIC_NAME) as sender:
            sender.send_messages(msg)

    except ServiceBusError as err:
        messages.error(request, _(f"Failed to trigger the ETL processes to repopulate the cache."))
        logger.exception(err)
        return

    messages.success(
        request,
        _("Request submitted to repopulate cache for summary pages as released on %s") % (
            f"{obj['timestamp__max']:%A, %-d %B %Y}"
        )
    )

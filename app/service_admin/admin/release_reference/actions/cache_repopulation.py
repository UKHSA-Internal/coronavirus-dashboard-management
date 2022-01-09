# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from json import dumps

# 3rd party:
from django.utils.translation import gettext as _
from django.conf import settings
from django.contrib import messages
from django.db.models import Max

from azure.servicebus import ServiceBusClient, ServiceBusMessage

# Internal:
from service_admin.models import ReleaseReference
from .utils import get_minute_instance_id

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'repopulate_cache'
]


TOPIC_NAME = "etl_operations"

REPOPULATE_CACHE = "REPOPULATE_CACHE"


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

    with ServiceBusClient.from_connection_string(settings.SERVICE_BUS_CREDENTIALS, logging_enable=True) as sb_client:
        with sb_client.get_topic_sender(topic_name=TOPIC_NAME) as sender:
            sender.send_messages(msg)

    messages.success(
        request,
        _("Request submitted to repopulate cache for summary pages as released on %s") % (
            f"{obj['timestamp__max']:%A, %-d %B %Y}"
        )
    )

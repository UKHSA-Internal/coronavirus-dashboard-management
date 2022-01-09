# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from json import dumps
from datetime import datetime
from hashlib import md5

# 3rd party:
from django.utils.translation import gettext as _
from django.conf import settings
from django.contrib import messages

from azure.servicebus import ServiceBusClient, ServiceBusMessage

# Internal:
from .utils import get_minute_instance_id

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'flush_all_cache',
    'flush_despatch_cache',
]

TOPIC_NAME = "cache_flusher"

FLUSH_ALL = "ALL"
FLUSH_DESPATCH = "DESPATCH"


def flush_all_cache(modeladmin, request, queryset):
    if not (request.user.has_perm('service_admin.change_processedfile') and
            request.user.has_perm('service_admin.change_releasereference')):
        return messages.error(
            request,
            _("You do not have permission to flush all cache. Operation aborted.")
        )

    payload = dumps({
        "ENVIRONMENT": settings.API_ENV,
        "to": FLUSH_ALL,
        "timestamp": datetime.utcnow().isoformat(),
    })

    msg = ServiceBusMessage(
        body=payload,
        session_id=request.session.session_key,
        to=FLUSH_ALL,
        message_id=get_minute_instance_id(FLUSH_ALL)
    )

    with ServiceBusClient.from_connection_string(settings.SERVICE_BUS_CREDENTIALS, logging_enable=True) as sb_client:
        with sb_client.get_topic_sender(topic_name=TOPIC_NAME) as sender:
            sender.send_messages(msg)

    messages.success(request, _("Request submitted to flush all cache."))


def flush_despatch_cache(modeladmin, request, queryset):
    if not request.user.has_perm('service_admin.change_releasereference'):
        return messages.error(
            request,
            _("You do not have permission to flush despatch cache. Operation aborted.")
        )

    payload = dumps({
        "to": FLUSH_DESPATCH,
        "requested_by": request.user.username,
        "ENVIRONMENT": settings.API_ENV,
        "timestamp": datetime.utcnow().isoformat(),
    })

    msg = ServiceBusMessage(
        body=payload,
        session_id=request.session.session_key,
        to=FLUSH_DESPATCH,
        message_id=get_minute_instance_id(FLUSH_DESPATCH)
    )

    with ServiceBusClient.from_connection_string(settings.SERVICE_BUS_CREDENTIALS, logging_enable=True) as sb_client:
        with sb_client.get_topic_sender(topic_name=TOPIC_NAME) as sender:
            sender.send_messages(msg)

    messages.success(request, _("Request submitted to flush despatch cache."))

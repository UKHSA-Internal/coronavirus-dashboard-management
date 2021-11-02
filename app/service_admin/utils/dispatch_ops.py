#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from datetime import datetime
from os import getenv
from json import dumps

# 3rd party:
from azure.servicebus import ServiceBusClient, ServiceBusMessage

# Internal: 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'update_timestamps'
]


SB_CONNSTR = getenv("SERVICEBUS_CONNECTION_STRING")
TOPIC_NAME = "data-despatch"
API_ENV = getenv("API_ENV")


UPLOAD_KWS = dict(
    content_type="text/plain; charset=utf-8",
    cache="no-cache, max-age=0",
    compressed=False,
    connection_string=getenv(f"DeploymentBlobStorage")
)


def update_timestamps(timestamp: datetime):
    timestamp = timestamp.isoformat()

    sb_client = ServiceBusClient.from_connection_string(
        conn_str=SB_CONNSTR,
        logging_enable=True
    )

    message = ServiceBusMessage(dumps({
        "event": "data despatched.",
        "environment": API_ENV,
        "timestamp": datetime.utcnow().isoformat(),
        "releaseTimestamp": timestamp
    }))

    with sb_client:
        with sb_client.get_topic_sender(topic_name=TOPIC_NAME) as sender:
            sender.send_messages(message)

    return True

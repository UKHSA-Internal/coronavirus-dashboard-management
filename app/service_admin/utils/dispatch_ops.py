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
from storage import StorageClient

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


def update_timestamps():
    timestamp = datetime.utcnow().isoformat()  # + "5Z"

    paths = [
        {
            "value": timestamp.split("T")[0],
            "path": "info/seriesDate",
            "container": "pipeline"
        },
        {
            "value": timestamp + "Z",
            "path": "assets/dispatch/website_timestamp",
            "container": "publicdata"
        },
        {
            "value": timestamp + "5Z",
            "path": "info/latest_published",
            "container": "pipeline",
        }
    ]

    for item in paths:
        kws = {**UPLOAD_KWS, **item}
        value = kws.pop("value")

        with StorageClient(**kws) as client:
            client.upload(value)

    sb_client = ServiceBusClient.from_connection_string(
        conn_str=SB_CONNSTR,
        logging_enable=True
    )

    message = ServiceBusMessage(dumps({
        "event": "data despatched.",
        "environment": API_ENV,
        "timestamp": datetime.utcnow().isoformat()
    }))

    with sb_client:
        with sb_client.get_topic_sender(topic_name=TOPIC_NAME) as sender:
            sender.send_messages(message)

    return True

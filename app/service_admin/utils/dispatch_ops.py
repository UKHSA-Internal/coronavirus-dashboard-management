#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from datetime import datetime
from os import getenv

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


UPLOAD_KWS = dict(
    content_type="text/plain; charset=utf-8",
    cache="no-cache, max-age=0",
    compressed=False,
    connection_string=getenv(f"DeploymentBlobStorage")
)


def update_timestamps():
    sb_client = ServiceBusClient.from_connection_string(
        conn_str=SB_CONNSTR,
        logging_enable=True
    )

    with sb_client:
        with sb_client.get_topic_sender(topic_name=TOPIC_NAME) as sender:
            message = ServiceBusMessage("Data deployed")
            sender.send_messages(message)

    timestamp = datetime.utcnow().isoformat() + "5Z"

    paths = [
        {
            "value": timestamp.split("T")[0],
            "path": "info/seriesDate",
            "container": "pipeline"
        },
        {
            "value": datetime.now().isoformat() + "Z",
            "path": "assets/dispatch/website_timestamp",
            "container": "publicdata"
        }
    ]

    for item in paths:
        kws = {**UPLOAD_KWS, **item}
        value = kws.pop("value")

        with StorageClient(**kws) as client:
            client.upload(value)

    return True

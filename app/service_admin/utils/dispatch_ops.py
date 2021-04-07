#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from datetime import datetime
from os import getenv

# 3rd party:

# Internal: 
from storage import StorageClient

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'update_timestamps'
]

UPLOAD_KWS = dict(
    content_type="text/plain; charset=utf-8",
    cache="no-cache, max-age=0",
    compressed=False
)


def update_timestamps():
    conn_str = getenv(f"DeploymentBlobStorage")

    UPLOAD_KWS["connection_string"] = conn_str

    timestamp = datetime.utcnow().isoformat() + "5Z"

    paths = [
        {
            "value": timestamp.split("T")[0],
            "path": "info/seriesDate",
            "container": "pipeline"
        },
        {
            "value": timestamp,
            "path": "info/latest_available",
            "container": "pipeline"
        },
        {
            "value": timestamp,
            "path": "info/latest_published",
            "container": "pipeline"
        },
        {
            "value": datetime.now().isoformat() + "Z",
            "path": "assets/dispatch/website_timestamp",
            "container": "publicdata"
        },

    ]

    for item in paths:
        kws = {**UPLOAD_KWS, **item}
        value = kws.pop("value")

        with StorageClient(**kws) as client:
            client.upload(value)

    return True

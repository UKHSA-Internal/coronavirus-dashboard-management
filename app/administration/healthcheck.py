#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from http import HTTPStatus
from asyncio import get_event_loop, wait, gather
from functools import reduce

# 3rd party:
from django.db import connection
from django.http import JsonResponse

# Internal:
from storage import StorageClient

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'run_healthcheck'
]


def test_db():
    with connection.cursor() as conn:
        conn.execute("SELECT NOW() AS timestamp;")
        response = conn.fetchone()

    return {"db": f"healthy - {response[0]}"}


def test_storage():
    with StorageClient("pipeline", "info/seen") as blob_client:
        blob = blob_client.download()
        blob_data = blob.readall()

    return {"storage": f"healthy - {blob_data.decode()}"}


def run_healthcheck(request):
    response = {
        **test_db(),
        **test_storage()
    }

    if request.method == 'GET':
        return JsonResponse(response, status=HTTPStatus.OK.real)

    return JsonResponse(response, status=HTTPStatus.NO_CONTENT.real)

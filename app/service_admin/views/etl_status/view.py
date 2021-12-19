#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from json import loads
# 3rd party:
from azure.cosmosdb.table.tableservice import TableService

from django.views.generic.base import TemplateView
from django.conf import settings

# Internal: 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'EtlView',
]


def process_table_payload(tasks):
    for task in tasks:
        yield {
            "status": task.RuntimeStatus,
            "name": task.Name,
            "payload": loads(loads(task.Input)),
            "message": task.CustomStatus,
            "key": task.PartitionKey,
            "last_update": task.LastUpdatedTime,
            "created": task.CreatedTime
        }


class EtlView(TemplateView):
    template_name = 'etl_status.html'
    table_obj = TableService(connection_string=settings.ETL_STORAGE)

    def get_context_data(self, **kwargs):
        obj = self.table_obj.query_entities(
            settings.ETL_STORAGE_TABLE_NAME,
            filter="CreatedTime ge datetime'2021-12-17'",
        )

        results = {
            "context": sorted(process_table_payload(obj), key=lambda x: x['last_update'], reverse=True)
        }

        return results

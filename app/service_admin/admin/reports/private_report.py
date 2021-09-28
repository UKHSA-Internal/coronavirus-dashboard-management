#!/usr/bin python3

"""
<Description of the programme>

Author:        Pouria Hadjibagheri <pouria.hadjibagheri@phe.gov.uk>
Created:       10 Sep 2021
License:       MIT
Contributors:  Pouria Hadjibagheri
"""

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from django.contrib import admin

# 3rd party:
from reversion.admin import VersionAdmin

# Internal: 
from service_admin.models.reports import PrivateReport
from service_admin.admin.mixins import ProdOnlyOps

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Header
__author__ = "Pouria Hadjibagheri"
__copyright__ = "Copyright (c) 2021, Public Health England"
__license__ = "MIT"
__version__ = "0.0.1"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


__all__ = [
    'PrivateReportAdmin'
]


@admin.register(PrivateReport)
class PrivateReportAdmin(VersionAdmin, ProdOnlyOps):
    list_per_page = 50
    ordering = [
        '-release',
        '-date'
    ]
    readonly_fields = [
        'id',
        'slug_id',
        'release',
        'metric',
        'area',
        'date',
        'value'
    ]
    view_on_site = True
    list_display = [
        "slug_id",
        "release",
        "metric",
        "area",
        "date",
        "value"
    ]

    list_filter = [
        # ('launch', admin.DateFieldListFilter),
        # ('expire', admin.DateFieldListFilter),
        # ('date', admin.DateFieldListFilter),
        # ('deploy_with_release', admin.BooleanFieldListFilter),
        # ('remove_with_release', admin.BooleanFieldListFilter),
    ]

    fieldsets = (
        (
            None,
            {
                'fields': (
                    ('id', 'slug_id'),
                    ('release', 'metric', 'area'),
                    ('date', 'value')
                ),
            },
        ),
    )

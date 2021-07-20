#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:

# 3rd party:
from django.contrib import admin
from reversion.admin import VersionAdmin

# Internal: 
from ...models.page import Page
from ..generic_admin import GuardedAdmin
from ..mixins import ProdOnlyOps

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


__all__ = [
    'PageAdmin'
]


@admin.register(Page)
class PageAdmin(ProdOnlyOps, VersionAdmin, GuardedAdmin):
    search_fields = [
        'title',
        'uri'
    ]

    readonly_fields = [
        'id'
    ]

    list_filter = [
        'data_category'
    ]

    list_display = [
        "title",
        "uri",
        "data_category"
    ]

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'id',
                    ('title', 'uri'),
                    'data_category',
                ),
            },
        ),
    )

#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:

# 3rd party:
from django.contrib import admin

# Internal: 
from ...models.page import Page
from ..generic_admin import GuardedAdmin
from ..mixins import ProdOnlyOps

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


__all__ = [
    'PageAdmin'
]


@admin.register(Page)
class PageAdmin(ProdOnlyOps, GuardedAdmin):
    search_fields = [
        'title',
        'uri'
    ]

    readonly_fields = [
        'id'
    ]

    list_display = [
        "title",
        "uri",
    ]

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'id',
                    ('title', 'uri'),
                ),
            },
        ),
    )

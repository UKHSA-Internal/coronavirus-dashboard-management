#!/usr/bin python3

from django.contrib import admin

from service_admin.models.announcement import Announcement
from service_admin.admin.generic_admin import GuardedAdmin
from service_admin.admin.mixins import ProdOnlyOps

from .inlines import (
    AnnouncementTagsInlineAdmin, PageTagsInlineAdmin,
    AreaInlineAdmin
)


__all__ = [
    'AnnouncementAdmin'
]


@admin.register(Announcement)
class AnnouncementAdmin(ProdOnlyOps, GuardedAdmin):
    readonly_fields = [
        'id'
    ]

    list_display = [
        "type",
        "appear_by_update",
        "disappear_by_update",
        "date",
        "released"
    ]

    inlines = [
        AnnouncementTagsInlineAdmin,
        PageTagsInlineAdmin,
        AreaInlineAdmin
    ]

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'id',
                    'type',
                    ('appear_by_update', 'disappear_by_update', 'date'),
                    'released',
                    'heading',
                    'body',
                    'details',
                ),
            },
        ),
    )

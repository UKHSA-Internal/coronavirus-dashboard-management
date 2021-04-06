#!/usr/bin python3

from django.contrib import admin

from ...models.announcement import Announcement
from ...models.page import Page
from ..generic_admin import GuardedAdmin
from ..mixins import ProdOnlyOps


__all__ = [
    'AnnouncementAdmin'
]


class PageTagsInlineAdmin(admin.TabularInline):
    model = Announcement.pages.through
    # can_delete = False
    # formset = BaselineMultiTenantFormset
    # readonly_fields = ['id']
    # exclude = ['id']
    extra = 3


@admin.register(Announcement)
class AnnouncementAdmin(ProdOnlyOps, GuardedAdmin):
    readonly_fields = [
        'id'
    ]

    list_display = [
        "appear_by_update",
        "disappear_by_update",
        "date"
    ]

    inlines = [PageTagsInlineAdmin]

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'id',
                    ('appear_by_update', 'disappear_by_update', 'date'),
                    'body'
                ),
            },
        ),
    )

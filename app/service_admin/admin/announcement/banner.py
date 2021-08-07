#!/usr/bin python3

from django.contrib import admin

from service_admin.models.announcement import Announcement
from service_admin.admin.mixins import ProdOnlyOps

from reversion.admin import VersionAdmin


__all__ = [
    'AnnouncementAdmin'
]


@admin.register(Announcement)
class AnnouncementAdmin(VersionAdmin, ProdOnlyOps):
    list_per_page = 20

    readonly_fields = [
        'id'
    ]

    list_display = [
        "launch",
        "expire",
        "date",
        "deploy_with_release",
        "remove_with_release"
    ]

    list_filter = [
        ('launch', admin.DateFieldListFilter),
        ('expire', admin.DateFieldListFilter),
        ('date', admin.DateFieldListFilter),
        ('deploy_with_release', admin.BooleanFieldListFilter),
        ('remove_with_release', admin.BooleanFieldListFilter),
    ]

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'id',
                    'launch',
                    'expire',
                    "date",
                    ('deploy_with_release', 'remove_with_release'),
                    'body',
                ),
            },
        ),
    )

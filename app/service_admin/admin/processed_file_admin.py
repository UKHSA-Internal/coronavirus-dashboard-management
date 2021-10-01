#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:

# 3rd party:
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

# Internal:
from service_admin.models.data import ProcessedFile
from service_admin.admin.release_reference import DateTimeFilter
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


__all__ = [
    'ReleaseReferenceAdmin',
]


@admin.register(ProcessedFile)
class ReleaseReferenceAdmin(admin.ModelAdmin):
    search_fields = ('file_path', 'type')
    list_per_page = 30
    readonly_fields = ["id", "process_id", "type", "timestamp", "release"]
    list_filter = [
        ('type', admin.ChoicesFieldListFilter),
        ('release__released', admin.BooleanFieldListFilter),
        ('timestamp', DateTimeFilter)
    ]

    list_display_links = [
        'timestamp',
    ]

    list_display = [
        'timestamp',
        'file_path',
        'type',
        'released',
        'release_object'
    ]

    def has_add_permission(self, request):
        return False

    def release_object(self, obj):
        if obj.release is None:
            return None

        link = reverse(
            f"admin:{obj._meta.app_label}_releasereference_change",
            args=(obj.release,)
        )

        return mark_safe(f'<a href="{link}">{obj.release}</a>')

    release_object.admin_order_field = 'Release id'
    release_object.short_description = 'Release id'

    def released(self, obj):
        return obj.release.released

    released.admin_order_field = 'Released'
    released.short_description = 'Released'
    released.boolean = True

#!/usr/bin python3

from django.contrib import admin
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe

from ..utils.dispatch_ops import update_timestamps

from ..models.data import ReleaseReference, ReleaseCategory
from .generic_admin import GuardedAdmin

from django_object_actions import DjangoObjectActions


__all__ = [
    'ReleaseReferenceAdmin'
]


def release_selected_for_testing(modeladmin, request, queryset):
    queryset.update(released=True)
    update_timestamps(env="TEST")


release_selected_for_testing.short_description = "Release selected deployments on Tulip"


def release_selected_for_development(modeladmin, request, queryset):
    queryset.update(released=True)
    update_timestamps(env="DEVELOPMENT")


release_selected_for_testing.short_description = "Release selected deployments on Daisy"


def release_selected_for_staging(modeladmin, request, queryset):
    queryset.update(released=True)
    update_timestamps(env="STAGING")


release_selected_for_testing.short_description = "Release selected deployments on Snowdrop"


class FilterByReleaseCategory(admin.SimpleListFilter):
    title = _('release category')
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        return ReleaseCategory.PROCESS_TYPE_ENUM

    def queryset(self, request, queryset):
        value = self.value()

        if value:
            return queryset.filter(category__process_name=value)

        return queryset


class FilterByReleaseStatus(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('release status')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        lookup = [
            ("released", _("Released")),
            ("pending", _("Pending")),
        ]

        return lookup

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        value = self.value()

        if value == 'release':
            queryset = queryset.filter(release_id__released=True)
        elif value == 'pending':
            queryset = queryset.filter(release_id__released=False)

        return queryset


@admin.register(ReleaseReference)
class ReleaseReferenceAdmin(DjangoObjectActions, GuardedAdmin):
    search_fields = ('label',)
    list_per_page = 20
    readonly_fields = ["category"]
    actions = [release_selected_for_testing]
    list_filter = [
        FilterByReleaseStatus,
        FilterByReleaseCategory
    ]
    changelist_actions = ('publish_latest_data',)
    list_display = [
        'formatted_release_time',
        'category',
        'released',
        'count',
        'difference'
    ]

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'timestamp',
                    'released',
                    'category'
                ),
            },
        ),
    )

    def formatted_release_time(self, obj):
        return mark_safe(obj.timestamp.strftime("%a, %d %b %Y &ndash; %H:%M:%S"))

    formatted_release_time.admin_order_field = 'timestamp'
    formatted_release_time.short_description = 'release time'

    def publish_latest_data(self, request, queryset):
        pass
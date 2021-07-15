#!/usr/bin python3

from django.contrib import admin
from django.utils.translation import gettext as _
from django.core.serializers import serialize
from json import dumps

from ...models.tags import Tag
from ..generic_admin import GuardedAdmin

from django_object_actions import DjangoObjectActions

from ..mixins import ProdOnlyOps


__all__ = [
    'TagAdmin'
]


def release_selected(modeladmin, request, queryset):
    queryset.update(released=True)


release_selected.short_description = _("Release selected metrics")


def withhold_selected(modeladmin, request, queryset):
    queryset.update(released=False)


withhold_selected.short_description = _("Withhold selected metrics")


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
            queryset = queryset.filter(released=True)
        elif value == 'pending':
            queryset = queryset.filter(released=False)

        return queryset


@admin.register(Tag)
class TagAdmin(ProdOnlyOps, GuardedAdmin):
    search_fields = ('tag',)
    # actions = [
    #     release_selected,
    #     withhold_selected
    # ]

    list_filter = [
        "association"
    ]

    list_per_page = 300

    readonly_fields = ['id']
    list_display = [
        'tag',
        'association',
    ]
    # changelist_actions = ('migrate_to_snowdrop', 'migrate_to_daisy')

    # def migrate_to_snowdrop(self, request, queryset):
    #     queryset.update(status='p')
    #
    # def migrate_to_daisy(self, request, queryset):
    #     print(dumps(list(queryset.values("metric", "metric_name", "released"))))
    #     print(dumps(queryset.values_list("metric", "metric_name", "released")))

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'id',
                    'association',
                    'tag'
                ),
            },
        ),
    )

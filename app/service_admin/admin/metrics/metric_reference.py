#!/usr/bin python3

from django.contrib import admin
from django.utils.translation import gettext as _
from json import dumps
from django.utils.safestring import mark_safe

from ...models.tags import MetricTag
from ...models.metric_docs import MetricAssetToMetric

from ...models.data import MetricReference
from ..generic_admin import GuardedAdmin

from django_object_actions import DjangoObjectActions
from ..mixins import ProdOnlyOps


__all__ = [
    'MetricReferenceAdmin',
    'TagsInlineAdmin'
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


class FilterBySourceMetricStatus(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('source metric status')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'is_source'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        lookup = [
            ("1", _("Source metrics")),
            ("0", _("Derived metric")),
        ]

        return lookup

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        value = self.value()

        if value == '1':
            queryset = queryset.filter(source_metric=True)
        elif value == '0':
            queryset = queryset.filter(source_metric=False)

        return queryset


# class BaselineMultiTenantFormset(BaseInlineFormSet):
#     def save_new(self, form, commit=True):
#         obj = super().save_new(form, commit=False)
#         print(obj)
#         # set_object_tenant(obj, obj.)


class TagsInlineAdmin(admin.TabularInline):
    model = MetricTag
    # formset = BaselineMultiTenantFormset
    readonly_fields = ['id']
    extra = 1


def as_tag(text):
    return (
        '<span class="table-tag" style="margin-right: 2px">' +
        str(text).strip().title().replace(" ", "&nbsp;") +
        '</span>'
    )


def metric_tags(obj):
    tag_ids = obj.tags.through.objects.filter(metric=obj.metric).all()
    return mark_safe(str.join("", [as_tag(tag) for tag in tag_ids]))


class MetricAssetInlineAdmin(admin.TabularInline):
    model = MetricAssetToMetric
    can_delete = False
    readonly_fields = ['id']
    fields = [
        "asset",
        "asset_type",
        "order",
        "id"
    ]
    extra = 10


@admin.register(MetricReference)
class MetricReferenceAdmin(ProdOnlyOps, DjangoObjectActions, GuardedAdmin):
    search_fields = ('metric',)
    actions = [
        release_selected,
        withhold_selected
    ]
    list_filter = [
        FilterByReleaseStatus,
        FilterBySourceMetricStatus
    ]
    list_per_page = 50

    readonly_fields = ['id', 'metric']
    list_display = [
        'metric',
        'metric_name',
        'source_metric',
        'released',
        metric_tags
    ]
    inlines = (
        TagsInlineAdmin,
        MetricAssetInlineAdmin
    )
    changelist_actions = ('migrate_to_snowdrop', 'migrate_to_daisy')

    def migrate_to_snowdrop(self, request, queryset):
        queryset.update(status='p')

    def migrate_to_daisy(self, request, queryset):
        print(dumps(list(queryset.values("metric", "metric_name", "released"))))
        print(dumps(queryset.values_list("metric", "metric_name", "released")))

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'id',
                    'metric',
                    'metric_name',
                    'source_metric',
                    'released',
                ),
            },
        ),
    )

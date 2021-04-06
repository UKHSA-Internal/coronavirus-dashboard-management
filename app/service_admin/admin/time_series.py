#!/usr/bin python3

from json import load
from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext as _
from datetime import timedelta
from ..models.data import TimeSeries, ReleaseReference, MetricReference, AreaReference
from .generic_admin import GuardedAdmin
from django.conf import settings
from django_admin_json_editor.admin import JSONEditorWidget
from .mixins import ProdOnlyOps


__all__ = [
    'TimeSeriesAdmin'
]


class FilterByAreaType(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('area type')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'area_type'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('overview', _('Overview')),
            ('nation', _('Nation')),
            ('region', _('Region')),
            ('utla', _('UTLA')),
            ('ltla', _('LTLA')),
            ('msoa', _('MSOA')),
            ('nhsRegion', _('NHS Region')),
            ('nhsTrust', _('NHS Trust')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        value = self.value()

        if value:
            queryset = queryset.filter(area_id__area_type=value)

        return queryset


class FilterByReleaseDate(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('release date')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'release'

    # no_filter_value = f"{timezone.now():%Y_%-m_%-d}"
    # no_filter_name = _("Latest")

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        dates = (
            ReleaseReference
            .objects
            .filter(timestamp__gte=timezone.now() - timezone.timedelta(days=7))
            .distinct('timestamp__date')
            .order_by("-timestamp__date")
        )

        return (
            (f"{ts:%Y_%-m_%-d}-{obj_id}", f"{ts:%Y-%m-%d}")
            for obj_id, ts in dates.values_list("id", "timestamp")
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        value = self.value()

        if value:
            release_ts, _ = value.split("-")
            partitions = [
                f"{release_ts}|other",
                f"{release_ts}|utla",
                f"{release_ts}|ltla",
                f"{release_ts}|nhsregion",
                f"{release_ts}|msoa",
            ]
        else:
            release = ReleaseReference.objects.latest('timestamp')
            release_ts = release.timestamp
            partitions = [
                f"{release_ts:%Y_%-m_%-d}|other",
                f"{release_ts:%Y_%-m_%-d}|utla",
                f"{release_ts:%Y_%-m_%-d}|ltla",
                f"{release_ts:%Y_%-m_%-d}|nhsregion",
                f"{release_ts:%Y_%-m_%-d}|msoa",
            ]

        queryset = queryset.filter(partition_id__in=partitions)

        return queryset

    def choices(self, changelist):
        for index, (lookup, title) in enumerate(self.lookup_choices):
            yield {
                'selected': self.value() == str(lookup) if self.value() is not None else index == 0,
                'query_string': changelist.get_query_string({self.parameter_name: lookup}),
                'display': title,
            }


class FilterByReleaseStatus(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('release status')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'status'

    # no_filter_value = f"{timezone.now():%Y_%-m_%-d}"
    # no_filter_name = _("Latest")

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


def dynamic_schema(obj):
    try:
        metric = obj.metric_id.metric
        area_type = obj.area_id.area_type
    except AttributeError:
        metric, area_type = None, None

    def func(widget):
        with open(settings.STATIC_ROOT.joinpath("data_schema", "schema.json")) as fp:
            schema = load(fp)

        generic = schema["generic"]

        if area_type != "msoa":
            return schema.get(metric, generic)

        return schema["msoa"].get(metric, generic)

    return func


@admin.register(TimeSeries)
class TimeSeriesAdmin(ProdOnlyOps, GuardedAdmin):
    search_fields = (
        'area_id__area_name',
        'area_id__area_type',
        'area_id__area_code',
        'metric_id__metric'
    )

    list_filter = [
        FilterByReleaseStatus,
        FilterByAreaType,
        FilterByReleaseDate,
    ]

    list_per_page = 100

    ordering = ('-release_id', '-date', 'area_id__area_type', 'area_id__area_code')

    readonly_fields = [
        'hash',
        'partition_id',
        'date',
        'release_id',
        'metric_id',
        'area_id',
        'area_name',
        'area_type',
        'area_code'
    ]

    list_display = [
        'area_name',
        'area_type',
        'area_code',
        'metric_id',
        'date',
        'release_id',
        'despatched'
    ]

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'release_id',
                    'date',
                    ('area_name', 'area_type', 'area_code'),
                    'metric_id',
                    'payload'
                ),
            },
        ),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if "release" in request.GET or "change" in request.path:
            return qs

        release = ReleaseReference.objects.latest('timestamp')
        release_ts = release.timestamp
        partitions = [
            f"{release_ts:%Y_%-m_%-d}|other",
            f"{release_ts:%Y_%-m_%-d}|utla",
            f"{release_ts:%Y_%-m_%-d}|ltla",
            f"{release_ts:%Y_%-m_%-d}|nhsregion",
            f"{release_ts:%Y_%-m_%-d}|msoa",
        ]

        return qs.filter(partition_id__in=partitions)

    def get_form(self, request, obj=None, change=False, **kwargs):
        widget = JSONEditorWidget(dynamic_schema(obj), False)
        form = super().get_form(request, obj, widgets={'payload': widget}, **kwargs)
        return form

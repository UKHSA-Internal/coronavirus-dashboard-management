#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:

# 3rd party:
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext as _

# Internal: 
from service_admin.models import PROCESS_TYPE_ENUM

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    "FilterByReleaseCategory"
]


class FilterByReleaseCategory(SimpleListFilter):
    title = _('release category')
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        return PROCESS_TYPE_ENUM

    def queryset(self, request, queryset):
        value = self.value()

        if value:
            return queryset.filter(category__process_name=value)

        return queryset

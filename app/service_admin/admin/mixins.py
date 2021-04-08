#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:

# 3rd party:
from django.conf import settings

# Internal: 
from service_admin.utils.presets import Environment

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'ProdOnlyAdd',
    'ProdOnlyDelete',
    'ProdOnlyChange',
    'ProdOnlyOps'
]


class ProdOnlyAdd:
    def has_add_permission(self, request):
        if settings.ENVIRONMENT != Environment.PRODUCTION and not request.user.is_superuser():
            return False

        return super().has_add_permission(request)


class ProdOnlyDelete:
    def has_delete_permission(self, request, obj=None):
        if settings.ENVIRONMENT != Environment.PRODUCTION and not request.user.is_superuser():
            return False

        return super().has_delete_permission(request, obj)


class ProdOnlyChange:
    def has_change_permission(self, request, obj=None):
        if settings.ENVIRONMENT != Environment.PRODUCTION and not request.user.is_superuser():
            return False

        return super().has_change_permission(request, obj)


class ProdOnlyOps(ProdOnlyAdd, ProdOnlyChange, ProdOnlyDelete):
    pass

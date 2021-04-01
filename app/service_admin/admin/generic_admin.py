#!/usr/bin python3

from functools import partial

from django.contrib import admin
from django.utils.translation import gettext as _

from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user

from ..models.generic import OversightRecord, Activity, Service

from django.core.exceptions import PermissionDenied


__all__ = [
    'GuardedAdmin',
    'PermittedActions'
]


class PermittedActions(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('permitted actions')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'view_basis'

    permissions = dict()

    @classmethod
    def with_permissions(cls, permissions):
        cls.permissions = permissions
        return cls

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('modify', _('can modify')),
            ('review', _('can review')),
            ('delete', _('can delete')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        query = self.value()

        user = request.user

        get_obj = partial(get_objects_for_user, user=user, klass=queryset)

        if query == 'modify':
            queryset = get_obj(perms=self.permissions.get("modify", list()))
        elif query == 'review':
            queryset = get_obj(perms=self.permissions.get("review", list()))
        elif query == 'delete':
            queryset = get_obj(perms=self.permissions.get("delete", list()))

        return queryset


class GuardedAdmin(GuardedModelAdmin):
    list_filter = [
        PermittedActions
    ]

    user_can_access_owned_by_group_objects_only = False

    permissions = dict(
        view=[
            'manage_service_object',
            'view_service_object',
            'view_service_contents'
        ],
        modify=[
            'manage_service_object',
            'modify_service_contents'
        ],
        create=[
            'manage_service_object',
            'create_service_contents'
        ],
        delete=[
            'manage_service_object',
            'delete_service_contents'
        ],
        review=[
            'manage_service_object',
            'review_service_contents'
        ]
    )

    def __init__(self, *args, **kwargs):
        for index, item in enumerate(self.list_filter):
            if isinstance(item, PermittedActions):
                self.list_filter[index] = PermittedActions.with_permissions(
                    permissions=self.permissions
                )

        super().__init__(*args, **kwargs)

    # def get_queryset(self, request):
    #     user = request.user
    #     perms = [
    #         *self.view_perms,
    #         *self.modify_perms,
    #         *self.create_perms,
    #         *self.delete_perms,
    #         *self.review_perms
    #     ]
    #     obj = get_objects_for_user(user=user, perms=perms, klass=self.model)
    #     return obj

    # def get_object
    # def changelist_view(self, request, extra_context=None):
    #     get_objects_for_user()
    # def changelist_view(self, request, extra_context=None):

    # def get_queryset(self, request):
    #     return get_objects_for_user(
    #         user=request.user,
    #         klass=super().get_queryset(request),
    #         perms=self.permissions.get("view", list())
    #     )

    def _do_save(self, request, obj, form, change):
        edit = getattr(obj, 'pk') is not None

        obj.save()
        oversight = OversightRecord(
            content_object=obj,
            user=request.user,
            activity=Activity.Modified if edit else Activity.Created
        )
        oversight.save()

        obj.oversight_records.add(oversight)

    def get_service(self, obj):
        if not isinstance(obj, Service):
            service = getattr(obj, 'service')

            if callable(service):
                service = service()
        else:
            service = obj

        return service

    # def save_model(self, request, obj, form, change):
    #     if (pk := getattr(obj, 'pk')) is not None:
    #         edit = False
    #     else:
    #         edit = obj.filter(pk=pk).exists()
    #
    #     user = request.user
    #     service = self.get_service(obj)
    #     user_perm = partial(user.has_perm, obj=service)
    #
    #     if edit and any(map(user_perm, self.permissions['modify'])):
    #         self._do_save(request, obj, form, change)
    #     elif not edit and any(map(user_perm, self.permissions['create'])):
    #         self._do_save(request, obj, form, change)
    #     else:
    #         raise PermissionDenied()

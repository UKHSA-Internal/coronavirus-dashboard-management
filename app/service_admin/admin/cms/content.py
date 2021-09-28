#!/usr/bin python3

"""
<Description of the programme>

Author:        Pouria Hadjibagheri <pouria.hadjibagheri@phe.gov.uk>
Created:       19 Jan 2020
License:       MIT
Contributors:  Pouria Hadjibagheri
"""

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:

# 3rd party:
from django.contrib import admin
from django.utils.translation import gettext as _

# Internal:
# from .generic import GenericAdmin
# from service_admin.models import Content, Entry

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Header
__author__ = "Pouria Hadjibagheri"
__copyright__ = "Copyright (c) 2020, Public Health England"
__license__ = "MIT"
__version__ = "0.0.1"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    # 'ContentAdmin'
]

#
# class EntryInline(admin.TabularInline):
#     model = Entry
#     fields = [
#         'field',
#         'value',
#         'order'
#     ]
#
#
# class ReviewStatus(admin.SimpleListFilter):
#     # Human-readable title which will be displayed in the
#     # right admin sidebar just above the filter options.
#     title = _('review status')
#
#     # Parameter for the filter that will be used in the URL query.
#     parameter_name = 'review_status'
#
#     permissions = dict(
#         view_perms=[
#             'view_content'
#         ],
#         modify_perms=[
#             'change_content'
#         ],
#         create_perms=[
#             'create_contents'
#         ],
#         delete_perms=[
#             'delete_content'
#         ],
#         review_perms=[
#             'review_content'
#         ]
#     )
#
#     def lookups(self, request, model_admin):
#         """
#         Returns a list of tuples. The first element in each
#         tuple is the coded value for the option that will
#         appear in the URL query. The second element is the
#         human-readable name for the option that will appear
#         in the right sidebar.
#         """
#         return (
#             ('P', _('Published')),
#             ('AR', _('Awaiting review')),
#         )
#
#     def queryset(self, request, queryset):
#         """
#         Returns the filtered queryset based on the value
#         provided in the query string and retrievable via
#         `self.value()`.
#         """
#         query = self.value()
#
#         if query == 'AR':
#             return queryset.awaiting_review()
#         elif query == 'P':
#             return queryset.published()
#
#
# @admin.register(Content)
# class ContentAdmin(GenericAdmin):
#     list_filter = (ReviewStatus,)
#     search_fields = ('label',)
#     list_display = ('label', 'child_of', 'get_children', 'page',)
#
#     inlines = [
#         EntryInline
#     ]
#
#     fieldsets = [
#         (
#             None,
#             {
#                 'fields': (
#                     ('label', 'slug'),
#                     'child_of',
#                     'page',
#                 )
#             }
#         )
#     ]
#
#     # def get_queryset(self, request):
#     #     qs = super().get_queryset(request)
#         # service = self.get_service(qs)
#         # if not request.user.has_perm(service, self.permissions['view']):
#         #     return None
#         # return qs
#
#
#
#         # return get_objects_for_user(
#         #     user=request.user,
#         #     klass=super().get_queryset(request),
#         #     perms=self.permissions.get("view", list())
#         # )
#
#     def get_children(self, obj):
#         return str.join("\n", [child.label for child in obj.children.all()]) or '-'
#
#     get_children.short_description = 'children'
#
#     # def save_model(self, request, obj, form, change):
#     #     edit = getattr(obj, 'pk') is not None
#     #     user = request.user
#     #     user_perm = partial(user.has_perm, obj=obj.section.service)
#     #
#     #     if edit and any(map(user_perm, self.modify_perms)):
#     #         super().save_model(request, obj, form, change)
#     #
#     #     elif not edit and any(map(user_perm, self.create_perms)):
#     #         super().save_model(request, obj, form, change)
#     #
#     #     return PermissionDenied()

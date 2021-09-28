# #!/usr/bin python3
#
# """
# <Description of the programme>
#
# Author:        Pouria Hadjibagheri <pouria.hadjibagheri@phe.gov.uk>
# Created:       18 Jan 2020
# License:       MIT
# Contributors:  Pouria Hadjibagheri
# """
#
# # Imports
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # Python:
#
# # 3rd party:
# from django.contrib import admin
#
# from guardian.shortcuts import get_objects_for_user
#
# # Internal:
# from ..models import Service
# from .generic import GenericAdmin
#
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # Header
# __author__ = "Pouria Hadjibagheri"
# __copyright__ = "Copyright (c) 2020, Public Health England"
# __license__ = "MIT"
# __version__ = "0.0.1"
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# __all__ = [
#     'ServiceAdmin'
# ]
#
#
# @admin.register(Service)
# class ServiceAdmin(GenericAdmin):
#     search_fields = ('name',)
#     fieldsets = (
#         (
#             None,
#             {
#                 'fields': (
#                     ('name', 'slug'),
#                     'description'
#                 ),
#             },
#         ),
#     )
#
#     def get_queryset(self, request):
#         qs = get_objects_for_user(
#             user=request.user,
#             perms=(
#                 'view_service_object',
#                 'manage_service_object'
#             ),
#             klass=super().get_queryset(request),
#             with_superuser=True,
#             use_groups=True,
#             accept_global_perms=True
#         )
#
#         return qs

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
# # Internal:
# from ..models import Section
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
#     'SectionAdmin'
# ]
#
#
# @admin.register(Section)
# class SectionAdmin(GenericAdmin):
#     search_fields = ('name',)
#
#     fieldsets = (
#         (
#             None,
#             {
#                 'fields': (
#                     ('name', 'slug'),
#                     'service'
#                 ),
#             },
#         ),
#     )
#

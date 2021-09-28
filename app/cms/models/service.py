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
# from django.db import models
# from django.urls import reverse_lazy
# from django.utils.translation import gettext as _
#
# from reversion import register as reversion_register
#
# # Internal:
# # from .activity_log import OversightRecord
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # Header
# __author__ = "Pouria Hadjibagheri"
# __copyright__ = "Copyright (c) 2020, Public Health England"
# __license__ = "MIT"
# __version__ = "0.0.1"
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# __all__ = [
#     'Service'
# ]
#
#
# @reversion_register()
# class Service(models.Model):
#     name = models.CharField(
#         verbose_name=_("name"),
#         max_length=32,
#         null=False,
#         db_index=True,
#         unique=True
#     )
#     slug = models.SlugField(
#         verbose_name=_("slug"),
#         help_text=_(
#             "URL name for the service: "
#             "This is utilised to construct the URL for service admin and the API. "
#             "May only contain characters, numbers, - (hyphen) or _ (underscore)."
#         ),
#         unique=True,
#         blank=False,
#         null=False,
#         db_index=True
#     )
#     description = models.TextField(
#         verbose_name=_("description")
#     )
#     # oversight_records = models.ManyToManyField(
#     #     to=OversightRecord,
#     #     verbose_name=_("oversight records"),
#     #     related_name="service_records",
#     #     db_index=True
#     # )
#     # created = models.DateTimeField(
#     #     verbose_name=_("created"),
#     #     auto_now_add=True,
#     #     db_index=True
#     # )
#
#     # def urls(self):
#     #     return reverse_lazy('service:service', kwargs=dict(service=self.slug))
#
#     def __str__(self):
#         return self.name
#
#     def get_dashboard_url(self):
#         return reverse_lazy(
#             "service:dashboard-services",
#             kwargs={
#                 "service": self.slug
#             }
#         )
#
#     class Meta:
#         verbose_name = _("service")
#         verbose_name_plural = _("services")
#         db_table = 'covid19"."cms_service'
#
#         ordering = ('pk',)
#
#         permissions = (
#             ('manage_service_object', _('Can manage service')),
#             ('view_service_object', _('Can view service')),
#             ('view_service_contents', _('Can view service contents')),
#             ('create_service_contents', _('Can create service contents')),
#             ('modify_service_contents', _('Can modify service contents')),
#             ('review_service_contents', _('Can review service contents')),
#             ('delete_service_contents', _('Can delete service contents')),
#         )

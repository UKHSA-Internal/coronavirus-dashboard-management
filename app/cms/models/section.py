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
#
# from django.utils.translation import gettext as _
#
# from reversion import register as reversion_register
#
# from django.urls import reverse_lazy
#
# # Internal:
# from .service import Service
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
#     'Section'
# ]
#
#
# class SectionManager(models.Manager):
#     def get_queryset(self):
#         from .content import Content
#         qs = super().get_queryset().filter(
#             contents__in=Content.objects.filter(section=models.F('pk'))
#         )
#         return qs.all()
#
#
# @reversion_register()
# class Section(models.Model):
#     name = models.CharField(
#         verbose_name=_("name"),
#         max_length=128,
#         null=False,
#         db_index=True
#     )
#     slug = models.SlugField(
#         verbose_name=_("slug"),
#         help_text=_(
#             "URL name for the section: "
#             "This is utilised to construct the URL for service admin and the API. "
#             "May only contain characters, numbers, - (hyphen) or _ (underscore)."
#         ),
#         blank=False,
#         null=False
#     )
#     service = models.ForeignKey(
#         to=Service,
#         related_name="sections",
#         on_delete=models.CASCADE,
#         db_index=True
#     )
#     # oversight_records = models.ManyToManyField(
#     #     to=OversightRecord,
#     #     verbose_name=_("oversight records"),
#     #     related_name="section_records",
#     #     db_index=True
#     # )
#
#     def get_dashboard_url(self):
#         return reverse_lazy(
#             "service:dashboard-sections",
#             kwargs={
#                 "service": self.service.slug,
#                 "section": self.slug
#             }
#         )
#
#     # timestamp = models.DateTimeField(
#     #     verbose_name=_("timestamp"),
#     #     auto_now_add=True,
#     #     db_index=True
#     # )
#     # change_log = models.CharField(
#     #     verbose_name=_("change log"),
#     #     max_length=255,
#     #     null=False,
#     #     blank=False,
#     #     help_text=_("Brief description of changes made to the document.")
#     # )
#
#     # def urls(self):
#     #     return reverse_lazy(
#     #         'service:service-sections-detail',
#     #         kwargs={
#     #             'service': self.service.slug,
#     #             'slug': self.slug
#     #         }
#     #     )
#
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = _("section")
#         verbose_name_plural = _("sections")
#         db_table = 'covid19"."cms_section'
#
#         unique_together = (
#             ('name', 'service'),
#             ('slug', 'service')
#         )
#
#         permissions = (
#             ('create_section', 'Create section'),
#             ('release_section', 'Release section'),
#             ('verify_section', 'Verify section'),
#         )
#
#     # class Versioning:
#     #     publication_date = 'timestamp'
#     #     clear_each_revision = ['change_log']

#!/usr/bin python3

"""
<Description of the programme>

Author:        Pouria Hadjibagheri <pouria.hadjibagheri@phe.gov.uk>
Created:       19 Jan 2020
License:       MIT
Contributors:  Pouria Hadjibagheri

ToDo:
    Oversight constrains to be implemented with respect to `service.Content`:
        - Last reviewer must not be the creator: OK - DB constraint (not the latest).
        - The review must be dated after the last modification for publication.
        - Object must not be published, or the last reviewed item must be published.
"""

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:

# 3rd party:
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from django.db import models

from django.urls import reverse_lazy
from django.utils.translation import gettext as _

# Internal:

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Header
__author__ = "Pouria Hadjibagheri"
__copyright__ = "Copyright (c) 2020, Public Health England"
__license__ = "MIT"
__version__ = "0.0.1"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'OversightRecord',
    'Activity',
    'Service'
]


ACTIVITIES = [
    ("C", _("Created")),
    ("M", _("Modified")),
    # ("P", _("Published")),
    ("R", _("Reviewed"))
]

activities_dict = dict(ACTIVITIES)

Activity = type(
    'Activities',
    tuple(),
    dict(zip(activities_dict.values(), activities_dict.keys()))
)


class OversightRecordQuerySet(models.QuerySet):
    def reviews(self):
        return self.filter(activity=Activity.Reviewed)

    def created(self):
        return self.filter(activity=Activity.Created)

    def _get_content_type(self, model):
        return ContentType.objects.get_for_model(model)

    def get_published_for(self, model):
        ctype = self._get_content_type(model)

        qs_reviewed = OversightRecord.objects.filter(
            activity=Activity.Reviewed,
            content_type=ctype,
            object_id=models.OuterRef('object_id')
        )

        qs = self.filter(
            content_type=ctype,
            activity__in=[Activity.Created, Activity.Modified],
        ).annotate(
            last_reviewed_on=models.Subquery(
                queryset=qs_reviewed.values('object_id').values('timestamp'),
                output_field=models.DateTimeField()
            )
        ).filter(
            last_reviewed_on__gt=models.F('timestamp')
        ).order_by(
            "object_id"
        ).distinct(
            "object_id"
        )

        return qs

    def get_awaiting_review(self, model):
        published = self.get_published_for(model)

        qs = self.filter(
            ~models.Q(object_id__in=published.values('object_id'))
        ).all()

        return qs

    def modified(self):
        return self.filter(activity=Activity.Modified)


class OversightRecordManager(models.Manager):
    def get_queryset(self):
        return OversightRecordQuerySet(self.model, using=self._db)

    def get_published_for(self, model):
        return self.get_queryset().get_published_for(model)

    def get_awaiting_review(self, model):
        return self.get_queryset().get_awaiting_review(model)


class OversightRecord(models.Model):
    content_type = models.ForeignKey(
        verbose_name=_("content type"),
        to=ContentType,
        on_delete=models.CASCADE,
        db_index=True,
        null=False
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_("object id"),
        db_index=True,
        null=False
    )
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(
        verbose_name=_("user"),
        to=User,
        on_delete=models.DO_NOTHING,
        null=False,
        db_index=True
    )
    timestamp = models.DateTimeField(
        verbose_name=_("timestamp"),
        auto_now_add=True,
        null=False,
        db_index=True
    )
    activity = models.CharField(
        max_length=1,
        choices=ACTIVITIES,
        verbose_name=_("activity"),
        null=False,
        blank=False,
        db_index=True,
        editable=False
    )

    objects = OversightRecordManager()

    def activity_long(self):
        return activities_dict.get(self.activity)

    class Meta:
        verbose_name = _("activity log")
        verbose_name_plural = _("activity logs")

        constraints = [
            models.UniqueConstraint(
                fields=('content_type', 'object_id', 'activity', 'user'),
                name='content_user_activity_unique_non_modifier',
                condition=~models.Q(activity=Activity.Modified)
            )
        ]

        get_latest_by = 'timestamp'

        indexes = [
            models.Index(
                fields=("content_type", "object_id"),
                name="oversight_cnt_idx"
            ),
            models.Index(
                fields=("content_type", "object_id", "user"),
                name="oversight_usercnt_idx"
            ),
            models.Index(
                fields=("content_type", "object_id", "-timestamp"),
                name="oversight_recent_objcnt_idx"
            ),
            models.Index(
                fields=("content_type", "object_id", "activity", 'user'),
                name="oversight_recent_useract_idx"
            ),
            models.Index(
                fields=("content_type", "object_id", "-timestamp", "user"),
                name="oversight_recent_timecnt_idx"
            ),
            models.Index(
                fields=("content_type", "object_id", "-timestamp", "activity"),
                name="oversight_recent_objact_idx"
            ),
        ]

        ordering = ["-timestamp"]


class Service(models.Model):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=32,
        null=False,
        db_index=True,
        unique=True
    )
    slug = models.SlugField(
        verbose_name=_("slug"),
        help_text=_(
            "URL name for the service: "
            "This is utilised to construct the URL for service admin and the API. "
            "May only contain characters, numbers, - (hyphen) or _ (underscore)."
        ),
        unique=True,
        blank=False,
        null=False,
        db_index=True
    )
    description = models.TextField(
        verbose_name=_("description")
    )
    oversight_records = models.ManyToManyField(
        to=OversightRecord,
        verbose_name=_("oversight records"),
        related_name="service_records",
        db_index=True
    )
    # created = models.DateTimeField(
    #     verbose_name=_("created"),
    #     auto_now_add=True,
    #     db_index=True
    # )

    # def urls(self):
    #     return reverse_lazy('service:service', kwargs=dict(service=self.slug))

    def __str__(self):
        return self.name

    def get_dashboard_url(self):
        return reverse_lazy(
            "service:dashboard-services",
            kwargs={
                "service": self.slug
            }
        )

    class Meta:
        verbose_name = _("service")
        verbose_name_plural = _("services")

        ordering = ('pk',)

        permissions = (
            ('manage_service_object', _('Can manage service')),
            ('view_service_object', _('Can view service')),

            ('create_metric_object', _('Can create metrics')),
            ('manage_metric_object', _('Can manage metrics')),
            ('view_metric_object', _('Can view metrics')),
            ('view_delete_object', _('Can delete metrics')),

            ('manage_release_object', _('Can despatch data')),
            ('view_release_object', _('Can view despatch')),

            ('create_banner_object', _('Can manage banners')),
            ('manage_banner_object', _('Can manage banners')),
            ('view_banner_object', _('Can view banners')),

            ('create_changelog_object', _('Can create change logs')),
            ('manage_changelog_object', _('Can manage change logs')),
            ('view_changelog_object', _('Can view change logs')),

            ('create_metricdoc_object', _('Can create metric documentations')),
            ('manage_metricdoc_object', _('Can manage metric documentations')),
            ('view_metricdoc_object', _('Can view metric documentations')),
        )

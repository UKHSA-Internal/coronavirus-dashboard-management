#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:

# 3rd party:
from django.contrib.admin import TabularInline

# Internal:
from service_admin.models.announcement import Announcement, BannerTag

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'PageTagsInlineAdmin',
    'AreaInlineAdmin',
    'AnnouncementTagsInlineAdmin',
]


class PageTagsInlineAdmin(TabularInline):
    model = Announcement.pages.through
    extra = 3


class AreaInlineAdmin(TabularInline):
    model = Announcement.areas.through
    extra = 5


class AnnouncementTagsInlineAdmin(TabularInline):
    model = BannerTag
    extra = 1

#!/usr/bin python3

from django.urls.conf import path
from .views.api import text_stats_api_view


urlpatterns = [
    path('', text_stats_api_view, name="textstats"),
]

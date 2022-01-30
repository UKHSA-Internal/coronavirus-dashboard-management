#!/usr/bin python3

from django.urls.conf import path
from django.contrib.admin.views.decorators import staff_member_required

from service_admin import views


# ToDo: Add API Documentations.
urlpatterns = [
    path('login', views.ProtectedLoginView.as_view()),
    path('textstats', views.text_stats_api_view, name="textstats"),
    path('etl_status', staff_member_required(views.EtlView.as_view(), login_url="/login"), name='etlview')
]


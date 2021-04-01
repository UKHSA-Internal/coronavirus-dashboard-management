#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:

# 3rd party:
from django import forms
from django_admin_json_editor.admin import JSONEditorWidget

# Internal: 
from service_admin.models.data import TimeSeries

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# class TimeSeriesAdminForm(forms.ModelForm):
#     class Meta:
#         model = TimeSeries
#         fields = '__all__'
#         widgets = {
#             'data': JSONEditorWidget(DATA_SCHEMA, collapsed=False),
#         }

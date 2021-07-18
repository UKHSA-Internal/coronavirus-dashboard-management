#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:

# 3rd party:
from django import forms

# Internal: 
from service_admin.models.change_log import ChangeLog

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'ChangeLogAdminFrom'
]


class ChangeLogAdminFrom(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        choice_dict = dict(ChangeLog.area_choices)
        self.fields['area'] = forms.MultipleChoiceField(
            initial=[(choice_dict[item], item) for item in kwargs['instance'].area],
            choices=ChangeLog.area_choices,
            required=False
        )

    class Meta:
        model = ChangeLog
        fields = '__all__'

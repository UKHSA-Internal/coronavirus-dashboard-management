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
        initial = list()
        if 'instance' in kwargs:
            initial = [(choice_dict[item], item) for item in kwargs['instance'].area]

        self.fields['area'] = forms.MultipleChoiceField(
            initial=initial,
            choices=ChangeLog.area_choices,
            required=False
        )

    class Meta:
        model = ChangeLog
        fields = '__all__'

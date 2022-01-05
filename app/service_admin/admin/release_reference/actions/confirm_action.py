#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from functools import wraps

# 3rd party:
from django.utils.translation import gettext as _
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.template.response import TemplateResponse
from django.contrib import messages

# Internal: 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'confirm_action'
]


def confirm_action(form_class=None):
    def decorator(func):
        @wraps(func)
        def wrapper(modeladmin, request, queryset):
            data_dates = {f"{item.timestamp:%Y-%m-%d}" for item in queryset}

            if len(data_dates) > 1:
                return messages.error(
                    request,
                    _(
                        "You cannot despatch multiple releases with different receipt "
                        "dates in one action. Found %d different dates: %s"
                    ) % (len(data_dates), str.join(", ", data_dates))
                )

            form = form_class(data_dates=data_dates)

            if request.POST and 'confirm' in request.POST:
                form = form_class(request.POST, data_dates=data_dates)
                if form.is_valid():
                    return func(modeladmin, request, queryset)

            context = dict(
                modeladmin.admin_site.each_context(request),
                title=form_class.title,
                action=func.__name__,
                opts=modeladmin.model._meta,
                queryset=queryset,
                form=form,
                action_checkbox_name=ACTION_CHECKBOX_NAME
            )

            return TemplateResponse(request, 'admin/action_confirmation.html', context)

        wrapper.short_description = form_class.title

        return wrapper

    return decorator

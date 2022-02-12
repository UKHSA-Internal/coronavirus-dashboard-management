#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:

# 3rd party:

from django.contrib.auth.views import LoginView
from django.contrib.admin.forms import AdminAuthenticationForm
from django.conf import settings

from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

# Internal: 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'ProtectedLoginView',
]


class ProtectedAuthenticationForm(AdminAuthenticationForm):
    if not settings.DEBUG:
        captcha = ReCaptchaField(
            widget=ReCaptchaWidget(),
            label='recaptcha',
            error_messages={'required': "Please use our fancy tool to prove you're not a robot!"}
        )


class ProtectedLoginView(LoginView):
    template_name = 'admin/login.html'
    form_class = ProtectedAuthenticationForm


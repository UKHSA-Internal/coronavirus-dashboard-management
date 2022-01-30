#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:

# 3rd party:
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView

from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

# Internal: 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'ProtectedLoginView',
]


class ProtectedAuthenticationForm(AuthenticationForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaWidget(),
        error_messages={'required': "Please use our fancy tool to prove you're not a robot!"}
    )


class ProtectedLoginView(LoginView):
    form_class = ProtectedAuthenticationForm



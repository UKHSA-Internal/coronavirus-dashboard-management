#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from uuid import uuid4

# 3rd party:
from django.db import models
from django.utils.translation import gettext as _

from markdownx.models import MarkdownxField

# Internal:
from .data import AreaReference
# from ..shared_models import PageURI
from .fields import VarCharField
from ..utils.default_generators import generate_unique_id

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


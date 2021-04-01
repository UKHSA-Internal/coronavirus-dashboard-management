#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:

# 3rd party:
from django.utils.translation import gettext as _
from django.db import models
from .data import MetricReference

# Internal: 
from .fields import VarCharField
from ..utils.default_generators import generate_unique_id

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# class Card(models.Model):
#     id = VarCharField(
#         verbose_name=_("unique ID"),
#         max_length=36,
#         primary_key=True,
#         default=generate_unique_id
#     )
#     heading = VarCharField(max_length=100)
#     card_type = VarCharField(max_length=50)
#     full_width = models.BooleanField()
#
#     download = models.ForeignKey(MetricReference, on_delete=models.CASCADE, related_name="")
#
#     options =

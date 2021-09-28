#!/usr/bin python3

from django.db import models


class VarCharField(models.CharField):
    def db_type(self, connection) -> str:
        return f"varchar({self.max_length})"

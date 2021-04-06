#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from dataclasses import dataclass

# 3rd party:

# Internal: 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'Environment'
]


@dataclass()
class Environment:
    DEVELOPMENT = "DEVELOPMENT"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"

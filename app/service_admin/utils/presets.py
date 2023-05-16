#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from dataclasses import dataclass

# 3rd party:

# Internal:

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'Environment',
    'ServiceName'
]


@dataclass()
class Environment:
    DEVELOPMENT = "DEVELOPMENT"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"
    SANDBOX = "SANDBOX"


@dataclass()
class ServiceName:
    DEVELOPMENT = "daisy"
    STAGING = "snowdrop"
    PRODUCTION = "tulip"
    SANDBOX = "tulip"

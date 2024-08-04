"""Models for Firefly."""

from __future__ import annotations


from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum

from mashumaro import DataClassDictMixin, field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin
from mashumaro.types import SerializationStrategy
from mashumaro.config import BaseConfig


@dataclass
class AboutResponse(DataClassORJSONMixin):
    """AboutResponse model."""

    data: About

@dataclass
class About(DataClassORJSONMixin):
    """About model."""

    version: str
    api_version: str
    php_version: str
    os: str
    driver: str

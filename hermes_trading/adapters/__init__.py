"""Data adapters. Each module exposes:

    SCHEMA_VERSION: int
    async def fetch(...) -> dict      # dict always includes "schema_version"

A shape that does not match the expected schema raises SchemaError, which the
loop treats as fatal (it halts rather than trading on data it can't trust).
Transient network errors are not SchemaErrors — the loop retries those.
"""

from .base import SchemaError, with_retries  # noqa: F401
from . import price, onchain, news, macro  # noqa: F401

ALL = {
    "price": price,
    "onchain": onchain,
    "news": news,
    "macro": macro,
}

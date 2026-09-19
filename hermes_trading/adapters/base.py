"""Shared adapter plumbing: schema errors and a retry helper."""

from __future__ import annotations

import asyncio
from typing import Awaitable, Callable, TypeVar

T = TypeVar("T")


class SchemaError(Exception):
    """Raised when fetched data does not match the adapter's expected schema.

    This is fatal by design: the loop halts rather than trading on data whose
    shape it no longer understands (e.g. an upstream API changed its payload).
    """


async def with_retries(
    fn: Callable[[], Awaitable[T]],
    *,
    attempts: int = 3,
    base_delay: float = 1.0,
) -> T:
    """Run an async fn with exponential backoff.

    Retries transient failures only. SchemaError is re-raised immediately and
    never retried — a schema mismatch will not fix itself.
    """
    last: Exception | None = None
    for i in range(attempts):
        try:
            return await fn()
        except SchemaError:
            raise
        except Exception as exc:  # noqa: BLE001 - transient, retry
            last = exc
            if i < attempts - 1:
                await asyncio.sleep(base_delay * (2 ** i))
    assert last is not None
    raise last

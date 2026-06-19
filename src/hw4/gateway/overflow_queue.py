"""Bounded FIFO overflow queue for the API gatekeeper (§5.3).

When the rate limiter is saturated, pending calls wait here in arrival order
instead of being rejected. The queue has a configured maximum depth; once full
it emits a backpressure alert and refuses further admissions so an overloaded
upstream fails loudly rather than growing memory without bound.
"""

from __future__ import annotations

import logging
import threading
from collections import deque
from typing import Any

from hw4.constants import GATEWAY_LOGGER_NAME


class OverflowQueue:
    """Thread-safe FIFO queue with a hard depth cap and backpressure logging."""

    def __init__(self, max_size: int, logger: logging.Logger | None = None) -> None:
        self._max_size = max_size
        self._items: deque[Any] = deque()
        self._lock = threading.Lock()
        self._logger = logger or logging.getLogger(GATEWAY_LOGGER_NAME)

    def enqueue(self, item: Any) -> bool:
        """Append ``item`` in FIFO order; return ``False`` (alert) when full."""
        with self._lock:
            if len(self._items) >= self._max_size:
                self._logger.warning(
                    "Backpressure: gateway queue full (max=%d); rejecting admission",
                    self._max_size,
                )
                return False
            self._items.append(item)
            return True

    def peek(self) -> Any:
        """Return the head item without removing it (``None`` if empty)."""
        with self._lock:
            return self._items[0] if self._items else None

    def remove(self, item: Any) -> None:
        """Remove the first occurrence of ``item`` if present."""
        with self._lock:
            try:
                self._items.remove(item)
            except ValueError:
                pass

    @property
    def is_full(self) -> bool:
        with self._lock:
            return len(self._items) >= self._max_size

    def __len__(self) -> int:
        with self._lock:
            return len(self._items)

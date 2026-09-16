"""Key helpers shared by the byte-oriented ciphers."""

from __future__ import annotations

import secrets
from collections.abc import Sized


def generate_key(length: int) -> bytes:
    """Return cryptographically secure random bytes of exactly ``length``."""
    if not isinstance(length, int) or isinstance(length, bool) or length < 0:
        raise ValueError("key length must be a non-negative integer")
    return secrets.token_bytes(length)


def validate_key(key: Sized, length: int) -> bool:
    """Return whether a key has the required length without modifying it."""
    if not isinstance(length, int) or isinstance(length, bool) or length < 0:
        return False
    try:
        return len(key) == length
    except TypeError:
        return False

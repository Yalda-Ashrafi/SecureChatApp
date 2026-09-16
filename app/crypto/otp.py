"""One-time-pad demonstration using UTF-8 message bytes."""

from __future__ import annotations

import secrets


def generate_key(length: int) -> bytes:
    if not isinstance(length, int) or isinstance(length, bool) or length < 0:
        raise ValueError("key length must be a non-negative integer")
    return secrets.token_bytes(length)


def _bytes(value: str | bytes, label: str) -> bytes:
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode("utf-8")
    raise TypeError(f"{label} must be text or bytes")


def _xor(data: str | bytes, key: str | bytes) -> bytes:
    data_bytes = _bytes(data, "message")
    key_bytes = _bytes(key, "key")
    if len(data_bytes) != len(key_bytes):
        raise ValueError("OTP key must be exactly the message length in bytes")
    return bytes(left ^ right for left, right in zip(data_bytes, key_bytes))


def encrypt(plaintext: str | bytes, key: str | bytes) -> bytes:
    return _xor(plaintext, key)


def decrypt(ciphertext: str | bytes, key: str | bytes) -> str | bytes:
    result = _xor(ciphertext, key)
    try:
        return result.decode("utf-8")
    except UnicodeDecodeError:
        return result

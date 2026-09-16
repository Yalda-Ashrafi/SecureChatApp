"""Byte-oriented Vernam (XOR) cipher.

Unlike Vigenere, Vernam never silently truncates data: a one-time key must
have exactly the same byte length as the message.
"""

from __future__ import annotations


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
        raise ValueError("Vernam key must be exactly the message length in bytes")
    return bytes(left ^ right for left, right in zip(data_bytes, key_bytes))


def encrypt(plaintext: str | bytes, key: str | bytes) -> bytes:
    return _xor(plaintext, key)


def decrypt(ciphertext: str | bytes, key: str | bytes) -> str | bytes:
    result = _xor(ciphertext, key)
    try:
        return result.decode("utf-8")
    except UnicodeDecodeError:
        return result

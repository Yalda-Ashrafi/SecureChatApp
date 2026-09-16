"""Classical Vigenere cipher.

Only ASCII alphabetic characters are transformed. Punctuation, whitespace,
digits, and letter case are preserved; non-letters do not consume key bytes.
"""

from __future__ import annotations


def _normalise_key(key: str) -> str:
    if not isinstance(key, str) or not key or not key.isascii() or not key.isalpha():
        raise ValueError("Vigenere key must contain ASCII alphabetic characters")
    return key.upper()


def _crypt(text: str, key: str, direction: int) -> str:
    if not isinstance(text, str):
        raise TypeError("Vigenere input must be text")
    key = _normalise_key(key)
    result: list[str] = []
    key_index = 0
    for char in text:
        if "A" <= char <= "Z" or "a" <= char <= "z":
            base = ord("A") if char.isupper() else ord("a")
            shift = ord(key[key_index % len(key)]) - ord("A")
            result.append(chr((ord(char) - base + direction * shift) % 26 + base))
            key_index += 1
        else:
            result.append(char)
    return "".join(result)


def encrypt(plaintext: str, key: str) -> str:
    return _crypt(plaintext, key, 1)


def decrypt(ciphertext: str, key: str) -> str:
    return _crypt(ciphertext, key, -1)

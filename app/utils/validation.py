"""Small validation helpers used by the HTTP layer."""

import re

USERNAME_RE = re.compile(r"^[A-Za-z0-9_.-]{3,30}$")


def validate_input(text: str | None, key: str | None) -> tuple[bool, str]:
    if not text or not key:
        return False, "Text and key must not be empty."
    return True, "Valid input."


def validate_username(username: str | None) -> tuple[bool, str]:
    if not username or not USERNAME_RE.fullmatch(username):
        return False, "Username must be 3-30 characters: letters, numbers, _, ., or -."
    return True, ""


def validate_password(password: str | None) -> tuple[bool, str]:
    if not password or len(password) < 8:
        return False, "Password must contain at least 8 characters."
    return True, ""

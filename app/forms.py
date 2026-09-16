"""Form-related constants.

The application intentionally uses ordinary HTML forms and validates them in
the route layer, so Flask-WTF (and its CSRF extension) is not required.
"""

USERNAME_MAX_LENGTH = 30
PASSWORD_MIN_LENGTH = 8


class _Field:
    """Tiny compatibility field used without pulling in Flask-WTF."""

    def __init__(self, data: str = ""):
        self.data = data


class LoginForm:
    """Validate login data for callers that prefer a form-style API."""

    def __init__(self, formdata=None):
        formdata = formdata or {}
        self.username = _Field(formdata.get("username", ""))
        self.password = _Field(formdata.get("password", ""))
        self.errors: dict[str, str] = {}

    def validate(self) -> bool:
        self.errors.clear()
        if not self.username.data or not 3 <= len(self.username.data) <= USERNAME_MAX_LENGTH:
            self.errors["username"] = "Enter a valid username."
        if not self.password.data:
            self.errors["password"] = "Enter your password."
        return not self.errors

    def validate_on_submit(self) -> bool:
        from flask import request

        return request.method == "POST" and self.validate()

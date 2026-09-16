"""Application factory for SecureChatApp."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Mapping

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config: Mapping[str, Any] | None = None) -> Flask:
    """Create and configure a Flask application.

    The factory keeps tests isolated by allowing a complete configuration
    override, while the normal application stores its SQLite database in the
    Flask instance directory.
    """
    root = Path(__file__).resolve().parent.parent
    instance_path = root / "instance"
    instance_path.mkdir(exist_ok=True)

    app = Flask(__name__, instance_path=str(instance_path), instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECURECHAT_SECRET_KEY", "dev-only-change-this-key"),
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{instance_path / 'chat.db'}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=False,
        MAX_CONTENT_LENGTH=256 * 1024,
    )
    if config:
        app.config.update(config)

    db.init_app(app)

    # Importing routes also imports models, registering their tables.
    from .routes import bp

    app.register_blueprint(bp)
    with app.app_context():
        db.create_all()
    return app

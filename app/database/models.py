from datetime import datetime, timezone

from sqlalchemy.orm import synonym

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    # Backwards-compatible alias for older code that reads the password field.
    password = synonym("password_hash")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(50), nullable=False, index=True)
    receiver = db.Column(db.String(50), nullable=False, index=True)
    algorithm = db.Column(db.String(20), nullable=False, default="unknown")
    ciphertext = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

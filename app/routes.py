from __future__ import annotations

import base64
import binascii
from functools import wraps

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .crypto import otp, vernam, vigenere
from .database.models import Message, User
from .utils.validation import validate_input, validate_password, validate_username

bp = Blueprint('routes', __name__)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("routes.login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def _current_user() -> User | None:
    user_id = session.get("user_id")
    return db.session.get(User, user_id) if user_id else None


def _display_ciphertext(value: bytes | str) -> str:
    if isinstance(value, bytes):
        return base64.b64encode(value).decode("ascii")
    return value


def _safe_next(value: str | None) -> str | None:
    """Allow only local paths when redirecting after authentication."""
    return value if value and value.startswith("/") and not value.startswith("//") else None


@bp.route("/")
def index():
    if session.get("user_id"):
        return redirect(url_for("routes.chat"))
    return redirect(url_for("routes.login"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        valid, error = validate_username(username)
        if not valid:
            flash(error, "error")
        else:
            valid, error = validate_password(password)
        if valid and error:
            flash(error, "error")
        elif valid and password != confirm:
            flash("Passwords do not match.", "error")
        elif valid and User.query.filter_by(username=username).first():
            flash("That username is already registered.", "error")
        elif valid:
            user = User(username=username, password_hash=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            flash("Account created. You can now log in.", "success")
            return redirect(url_for("routes.login"))
    return render_template("register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session.clear()
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(_safe_next(request.args.get("next")) or url_for("routes.chat"))
        flash("Invalid username or password.", "error")
    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("routes.login"))


def _encrypt(algorithm: str, text: str, key: str):
    if algorithm == "vigenere":
        return vigenere.encrypt(text, key)
    if algorithm == "vernam":
        return vernam.encrypt(text, key)
    if algorithm == "otp":
        return otp.encrypt(text, key)
    raise ValueError("Unknown encryption algorithm")


def _decrypt(algorithm: str, ciphertext: str, key: str):
    if algorithm == "vigenere":
        return vigenere.decrypt(ciphertext, key)
    if algorithm in {"vernam", "otp"}:
        try:
            encrypted_bytes = base64.b64decode(ciphertext.strip(), validate=True)
        except (ValueError, binascii.Error) as exc:
            raise ValueError("Ciphertext must be valid Base64 for this algorithm") from exc
        decrypt_key = key
        if algorithm == "otp":
            try:
                decrypt_key = base64.b64decode(key.strip(), validate=True)
            except (ValueError, binascii.Error) as exc:
                raise ValueError("OTP key must be valid Base64") from exc
        decrypted = (vernam if algorithm == "vernam" else otp).decrypt(encrypted_bytes, decrypt_key)
        if not isinstance(decrypted, str):
            raise ValueError("Decrypted bytes are not valid UTF-8 text")
        return decrypted
    raise ValueError("Unknown encryption algorithm")


@bp.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    user = _current_user()
    messages = Message.query.filter(
        or_(Message.sender == user.username, Message.receiver == user.username)
    ).order_by(Message.timestamp.desc()).limit(25).all()
    ciphertext = None
    ciphertext_type = None
    decrypted_text = None
    decrypt_algorithm = "vigenere"
    decrypt_ciphertext = ""
    if request.method == "POST":
        action = request.form.get("action", "encrypt")
        if action == "decrypt":
            decrypt_algorithm = request.form.get("decrypt_algorithm", "vigenere")
            decrypt_ciphertext = request.form.get("decrypt_ciphertext", "").strip()
            decrypt_key = request.form.get("decrypt_key", "")
            if not decrypt_ciphertext or not decrypt_key:
                flash("Enter ciphertext and its key to decrypt.", "error")
            else:
                try:
                    decrypted_text = _decrypt(decrypt_algorithm, decrypt_ciphertext, decrypt_key)
                except (TypeError, ValueError) as exc:
                    flash(str(exc), "error")
        else:
            text = request.form.get("plaintext", "")
            key = request.form.get("key", "")
            algorithm = request.form.get("algorithm", "vigenere")
            receiver = request.form.get("receiver", "").strip() or user.username
            valid, error = validate_input(text, key)
            if not valid:
                flash(error, "error")
            else:
                try:
                    encrypted = _encrypt(algorithm, text, key)
                    ciphertext = _display_ciphertext(encrypted)
                    ciphertext_type = "Base64 bytes" if isinstance(encrypted, bytes) else "Text"
                    message = Message(
                        sender=user.username,
                        receiver=receiver,
                        algorithm=algorithm,
                        ciphertext=ciphertext,
                    )
                    db.session.add(message)
                    db.session.commit()
                except (TypeError, ValueError) as exc:
                    flash(str(exc), "error")
    return render_template(
        "chat.html",
        ciphertext=ciphertext,
        ciphertext_type=ciphertext_type,
        decrypted_text=decrypted_text,
        decrypt_algorithm=decrypt_algorithm,
        decrypt_ciphertext=decrypt_ciphertext,
        messages=messages,
    )


@bp.route("/otp-demo", methods=["GET", "POST"])
@bp.route("/otp", methods=["GET", "POST"])
def otp_demo():
    result = None
    decrypted_text = None
    if request.method == "POST":
        action = request.form.get("action", "encrypt")
        if action == "decrypt":
            encoded_key = request.form.get("decrypt_key", "").strip()
            encoded_ciphertext = request.form.get("decrypt_ciphertext", "").strip()
            result = {
                "key": encoded_key,
                "ciphertext": encoded_ciphertext,
                "plaintext": request.form.get("original_plaintext", ""),
                "length": 0,
            }
            if not encoded_key or not encoded_ciphertext:
                flash("Enter both the Base64 key and ciphertext.", "error")
            else:
                try:
                    key = base64.b64decode(encoded_key, validate=True)
                    ciphertext = base64.b64decode(encoded_ciphertext, validate=True)
                    result["length"] = len(key)
                    decrypted = otp.decrypt(ciphertext, key)
                    if not isinstance(decrypted, str):
                        raise ValueError("The decrypted bytes are not valid UTF-8 text.")
                    decrypted_text = decrypted
                except (ValueError, binascii.Error) as exc:
                    flash(f"Unable to decrypt: {exc}", "error")
        else:
            plaintext = request.form.get("plaintext", "")
            if not plaintext:
                flash("Enter a message to generate a one-time pad.", "error")
            else:
                key = otp.generate_key(len(plaintext.encode("utf-8")))
                ciphertext = otp.encrypt(plaintext, key)
                result = {
                    "key": base64.b64encode(key).decode("ascii"),
                    "ciphertext": base64.b64encode(ciphertext).decode("ascii"),
                    "plaintext": plaintext,
                    "length": len(key),
                }
    return render_template(
        "otp_demo.html",
        result=result,
        decrypted_text=decrypted_text,
    )

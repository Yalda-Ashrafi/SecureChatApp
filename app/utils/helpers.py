from datetime import datetime


def format_message(sender: str, receiver: str, ciphertext: str, timestamp: datetime | None = None) -> str:
    when = f" ({timestamp:%Y-%m-%d %H:%M UTC})" if timestamp else ""
    return f"From: {sender} To: {receiver}{when} | {ciphertext}"

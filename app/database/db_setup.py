from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created successfully.")

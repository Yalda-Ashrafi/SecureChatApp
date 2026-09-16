"""Development entry point.

This file is intentionally runnable both as ``python -m app.main`` and as
``python app/main.py`` from the repository root.
"""

from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

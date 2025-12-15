from flask import Flask, jsonify
import os
from pathlib import Path
from app.db import Base, engine
from app import create_app
from app.models.contact import Contact  # noqa: F401  ensure model is imported
from app.models.deal import Deal  # noqa: F401  ensure model is imported


# Ensure data dir exists for SQLite
Path("data").mkdir(parents=True, exist_ok=True)

# Create tables (dev convenience; use migrations later)
Base.metadata.create_all(bind=engine)

app: Flask = create_app()


@app.get("/")
def health():
    return jsonify({"app": "OpenERP-MVP", "status": "ok"})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="127.0.0.1", port=port, debug=True)

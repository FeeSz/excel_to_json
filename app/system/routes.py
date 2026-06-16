from pathlib import Path

from flask import Blueprint
from flask import jsonify

from app.core.database import db


system_bp = Blueprint(
    "system",
    __name__
)


@system_bp.route(
    "/health",
    methods=["GET"]
)
def health():

    database_ok = True
    storage_ok = True

    try:

        db.session.execute(
            db.text("SELECT 1")
        )

    except Exception:

        database_ok = False

    try:

        Path(
            "storage/uploads"
        ).mkdir(
            parents=True,
            exist_ok=True
        )

        Path(
            "storage/outputs"
        ).mkdir(
            parents=True,
            exist_ok=True
        )

    except Exception:

        storage_ok = False

    return jsonify({
        "status": (
            "ok"
            if database_ok and storage_ok
            else "error"
        ),
        "database": database_ok,
        "storage": storage_ok
    })
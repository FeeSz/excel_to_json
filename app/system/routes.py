from pathlib import Path

from flask import Blueprint
from flask import jsonify

from app.core.database import db
from app.core.logger import logger

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

    except Exception as erro:

        database_ok = False

        logger.exception(
            f"HEALTH_DATABASE_ERROR | {erro}"
        )

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

    except Exception as erro:

        storage_ok = False

        logger.exception(
            f"HEALTH_STORAGE_ERROR | {erro}"
        )

    status = (
        "ok"
        if database_ok and storage_ok
        else "error"
    )

    logger.info(
        f"HEALTH_CHECK | "
        f"status={status} | "
        f"database={database_ok} | "
        f"storage={storage_ok}"
    )

    return jsonify({
        "status": status,
        "database": database_ok,
        "storage": storage_ok
    })
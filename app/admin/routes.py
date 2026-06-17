from flask import Blueprint
from flask import jsonify

from flask_login import (
    login_required,
    current_user
)

from app.admin.service import (
    AdminService
)

from app.core.logger import logger

admin_bp = Blueprint(
    "admin",
    __name__
)


@admin_bp.route(
    "/admin/stats",
    methods=["GET"]
)
@login_required
def stats():

    dados = (
        AdminService
        .obter_estatisticas()
    )

    logger.info(
        f"ADMIN_STATS | "
        f"user_id={current_user.id}"
    )

    return jsonify(
        dados
    )
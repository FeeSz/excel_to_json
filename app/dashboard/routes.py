from flask import Blueprint
from flask import jsonify
from flask_login import current_user
from flask_login import login_required
from app.core.decorators import admin_required

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    return jsonify({
        "success": True,
        "usuario": current_user.nome,
        "email": current_user.email,
        "role": current_user.role
    })


@dashboard_bp.route(
    "/admin"
)
@admin_required
def admin_panel():

    return jsonify({
        "success": True,
        "message": "Painel administrativo"
    })
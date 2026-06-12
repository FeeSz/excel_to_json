from functools import wraps

from flask import jsonify

from flask_login import current_user
from flask_login import login_required


def admin_required(func):

    @wraps(func)
    @login_required
    def wrapper(*args, **kwargs):

        if current_user.role != "admin":

            return jsonify({
                "success": False,
                "message": "Acesso negado."
            }), 403

        return func(*args, **kwargs)

    return wrapper
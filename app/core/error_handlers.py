from flask import jsonify

from app.core.exceptions import (
    AppError
)


def register_error_handlers(app):

    @app.errorhandler(AppError)
    def handle_app_error(error):

        return jsonify({
            "success": False,
            "message": error.message
        }), 400

    @app.errorhandler(404)
    def handle_not_found(error):

        return jsonify({
            "success": False,
            "message": "Recurso não encontrado."
        }), 404

    @app.errorhandler(500)
    def handle_internal_error(error):

        return jsonify({
            "success": False,
            "message": "Erro interno do servidor."
        }), 500
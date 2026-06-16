from flask import Blueprint
from flask import jsonify
from flask import request
from flask_login import (
    login_required,
    current_user
)


from app.core.logger import logger
from app.uploads.service import (
    UploadService
)

upload_bp = Blueprint(
    "upload",
    __name__
)


@upload_bp.route(
    "/upload",
    methods=["POST"]
)
@login_required
def upload():

    if "file" not in request.files:

        return jsonify({
            "success": False,
            "message": "Arquivo não enviado."
        }), 400

    try:

        arquivo = request.files["file"]

        layout = request.form.get(
            "layout"
        )

        logger.info(
            f"UPLOAD_INICIADO | "
            f"user_id={current_user.id} | "
            f"arquivo={arquivo.filename} | "
            f"layout={layout}"
        )

        job = UploadService.salvar_upload(
            arquivo,
            layout
        )

        logger.info(
            f"JOB_CRIADO | "
            f"user_id={current_user.id} | "
            f"job_id={job.id} | "
            f"status={job.status}"
        )

        return jsonify({
            "success": True,
            "job_id": job.id,
            "filename": job.filename,
            "status": job.status
        })

    except ValueError as erro:

        logger.warning(
            f"UPLOAD_INVALIDO | "
            f"user_id={current_user.id} | "
            f"erro={str(erro)}"
        )

        return jsonify({
            "success": False,
            "message": str(erro)
        }), 400

    except Exception as erro:

        logger.exception(
            f"UPLOAD_ERRO | "
            f"user_id={current_user.id}"
        )

        return jsonify({
            "success": False,
            "message": "Erro interno."
        }), 500
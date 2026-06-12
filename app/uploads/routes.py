from flask import Blueprint
from flask import jsonify
from flask import request

from flask_login import login_required

from app.uploads.service import UploadService

upload_bp = Blueprint(
    "uploads",
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

        job = UploadService.salvar_upload(
            arquivo
        )

        return jsonify({
            "success": True,
            "job_id": job.id,
            "filename": job.filename,
            "status": job.status
        })

    except ValueError as erro:

        return jsonify({
            "success": False,
            "message": str(erro)
        }), 400
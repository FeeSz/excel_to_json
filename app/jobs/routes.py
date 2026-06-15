from flask import Blueprint
from flask import jsonify
from flask import send_file

from flask_login import (
    login_required,
    current_user
)

from app.jobs.service import (
    JobService
)

jobs_bp = Blueprint(
    "jobs",
    __name__
)

@jobs_bp.route(
    "/jobs",
    methods=["GET"]
)
@login_required
def listar_jobs():

    jobs = (
        JobService
        .listar_jobs_usuario(
            current_user.id
        )
    )

    resultado = []

    for job in jobs:

        resultado.append({
            "id": job.id,
            "filename": job.filename,
            "status": job.status,
            "records_processed":
                job.records_processed,
            "created_at":
                job.created_at.isoformat()
        })

    return jsonify(resultado)


@jobs_bp.route(
    "/jobs/<int:job_id>",
    methods=["GET"]
)
@login_required
def consultar_job(job_id):

    job = JobService.obter_job(
        job_id
    )

    if not job:

        return jsonify({
            "success": False,
            "message":
                "Job não encontrado."
        }), 404

    if job.user_id != current_user.id:

        return jsonify({
            "success": False,
            "message":
                "Acesso negado."
        }), 403

    return jsonify({
        "id": job.id,
        "filename": job.filename,
        "status": job.status,
        "records_processed":
            job.records_processed,
        "output_filename":
            job.output_filename,
        "error_message":
            job.error_message,
        "created_at":
            job.created_at.isoformat()
    })

@jobs_bp.route(
    "/jobs/<int:job_id>/download",
    methods=["GET"]
)
@login_required
def download_job(job_id):

    job, arquivo = (
        JobService
        .obter_arquivo_resultado(job_id)
    )

    if not job:

        return jsonify({
            "success": False,
            "message": "Job não encontrado."
        }), 404

    if job.user_id != current_user.id:

        return jsonify({
            "success": False,
            "message": "Acesso negado."
        }), 403

    if not arquivo or not arquivo.exists():

        return jsonify({
            "success": False,
            "message": "Arquivo não disponível."
        }), 404
    
    print("JOB",job_id)
    print("AQRUIVO",arquivo)
    print("EXISTS",arquivo.exists())
    print("TIPO",type(arquivo))

    return send_file(
        str(arquivo),
        as_attachment=True
    )
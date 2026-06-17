from flask import Blueprint
from flask import jsonify
from flask import send_file

from flask_login import (
    login_required,
    current_user
)

from app.core.logger import logger

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

    logger.info(
        f"JOB_LISTADO | "
        f"user_id={current_user.id} | "
        f"quantidade={len(resultado)}"
    )

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

        logger.warning(
            f"JOB_NAO_ENCONTRADO | "
            f"user_id={current_user.id} | "
            f"job_id={job_id}"
        )

        return jsonify({
            "success": False,
            "message":
                "Job não encontrado."
        }), 404

    if job.user_id != current_user.id:

        logger.warning(
            f"JOB_ACESSO_NEGADO | "
            f"user_id={current_user.id} | "
            f"job_id={job.id}"
        )

        return jsonify({
            "success": False,
            "message":
                "Acesso negado."
        }), 403

    logger.info(
        f"JOB_CONSULTADO | "
        f"user_id={current_user.id} | "
        f"job_id={job.id} | "
        f"status={job.status}"
    )

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

        logger.warning(
            f"DOWNLOAD_JOB_NAO_ENCONTRADO | "
            f"user_id={current_user.id} | "
            f"job_id={job_id}"
        )

        return jsonify({
            "success": False,
            "message":
                "Job não encontrado."
        }), 404

    if job.user_id != current_user.id:

        logger.warning(
            f"DOWNLOAD_NEGADO | "
            f"user_id={current_user.id} | "
            f"job_id={job.id}"
        )

        return jsonify({
            "success": False,
            "message":
                "Acesso negado."
        }), 403

    if not arquivo or not arquivo.exists():

        logger.warning(
            f"DOWNLOAD_ARQUIVO_AUSENTE | "
            f"user_id={current_user.id} | "
            f"job_id={job.id}"
        )

        return jsonify({
            "success": False,
            "message":
                "Arquivo não disponível."
        }), 404

    logger.info(
        f"DOWNLOAD_REALIZADO | "
        f"user_id={current_user.id} | "
        f"job_id={job.id} | "
        f"arquivo={job.output_filename}"
    )

    return send_file(
        str(arquivo),
        as_attachment=True
    )
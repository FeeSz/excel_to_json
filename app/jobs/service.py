from pathlib import Path

from app.models.conversion_job import ConversionJob
from app.core.database import db


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

OUTPUT_PATH = (
    BASE_DIR
    / "storage"
    / "outputs"
)


class JobService:

    @staticmethod
    def listar_jobs_usuario(user_id):

        return (
            ConversionJob.query
            .filter_by(user_id=user_id)
            .order_by(
                ConversionJob.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def obter_job(job_id):

        return db.session.get(
            ConversionJob,
            job_id
        )

    @staticmethod
    def obter_arquivo_resultado(job_id):

        job = db.session.get(
            ConversionJob,
            job_id
        )

        if not job:
            return None, None

        if not job.output_filename:
            return job, None

        arquivo = (
            OUTPUT_PATH
            / job.output_filename
        ).resolve()

        return job, arquivo
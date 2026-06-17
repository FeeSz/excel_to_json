from sqlalchemy import func

from app.core.database import db

from app.models.user import User
from app.models.conversion_job import ConversionJob

from app.core.constants import (
    JOB_COMPLETED,
    JOB_PENDING,
    JOB_ERROR
)


class AdminService:

    @staticmethod
    def obter_estatisticas():

        usuarios = (
            User.query.count()
        )

        jobs_total = (
            ConversionJob.query.count()
        )

        jobs_concluidos = (
            ConversionJob.query
            .filter_by(
                status=JOB_COMPLETED
            )
            .count()
        )

        jobs_pendentes = (
            ConversionJob.query
            .filter_by(
                status=JOB_PENDING
            )
            .count()
        )

        jobs_erro = (
            ConversionJob.query
            .filter_by(
                status=JOB_ERROR
            )
            .count()
        )

        registros_processados = (
            db.session.query(
                func.coalesce(
                    func.sum(
                        ConversionJob.records_processed
                    ),
                    0
                )
            )
            .scalar()
        )

        return {
            "usuarios": usuarios,
            "jobs_total": jobs_total,
            "jobs_concluidos": jobs_concluidos,
            "jobs_pendentes": jobs_pendentes,
            "jobs_erro": jobs_erro,
            "registros_processados":
                registros_processados
        }
    
	
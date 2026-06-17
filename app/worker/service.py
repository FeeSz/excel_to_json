from app.models.conversion_job import ConversionJob

from app.core.constants import (
    JOB_PENDING
)


class WorkerService:

    @staticmethod
    def buscar_job_pendente():

        return (
            ConversionJob.query
            .filter_by(
                status=JOB_PENDING
            )
            .order_by(
                ConversionJob.created_at.asc()
            )
            .first()
        )

    @staticmethod
    def total_pendentes():

        return (
            ConversionJob.query
            .filter_by(
                status=JOB_PENDING
            )
            .count()
        )
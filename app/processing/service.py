from app.core.logger import logger
from pathlib import Path
from datetime import datetime

from app.core.database import db

from app.core.constants import (
    JOB_PROCESSING,
    JOB_COMPLETED,
    JOB_ERROR,
    LAYOUT_CLIENTES
)

from app.core.logger import logger

from app.models.conversion_job import (
    ConversionJob
)

from app.processing.excel_processor import (
    ExcelProcessor
)

from app.processing.exporters import (
    JsonExporter
)


class ProcessingService:

    @staticmethod
    def processar_job(job_id):

        job = db.session.get(
            ConversionJob,
            job_id
        )

        if not job:

            raise ValueError(
                f"Job {job_id} não encontrado."
            )

        logger.info(
            f"PROCESSAMENTO_INICIADO | "
            f"job_id={job.id} | "
            f"arquivo={job.filename}"
        )

        job.status = JOB_PROCESSING

        db.session.commit()

        filepath = (
            Path("storage/uploads")
            / job.stored_filename
        )

        try:

            if job.layout_type == LAYOUT_CLIENTES:

                df = (
                    ExcelProcessor
                    .processar_clientes(
                        filepath
                    )
                )

            else:

                raise ValueError(
                    f"Layout não suportado: "
                    f"{job.layout_type}"
                )

            logger.info(
                f"EXCEL_PROCESSADO | "
                f"job_id={job.id} | "
                f"registros={len(df)}"
            )

            output_filename = (
                JsonExporter.exportar(df)
            )

            logger.info(
                f"JSON_GERADO | "
                f"job_id={job.id} | "
                f"arquivo={output_filename}"
            )

            job.output_filename = (
                output_filename
            )

            job.records_processed = (
                len(df)
            )

            job.status = (
                JOB_COMPLETED
            )

            job.completed_at = (
                datetime.utcnow()
            )

            db.session.commit()

            logger.info(
                f"PROCESSAMENTO_CONCLUIDO | "
                f"job_id={job.id} | "
                f"registros={job.records_processed}"
            )

            return job

        except Exception as erro:

            logger.exception(
                f"PROCESSAMENTO_ERRO | "
                f"job_id={job.id}"
            )

            db.session.rollback()

            job.status = JOB_ERROR

            job.error_message = (
                str(erro)[:500]
            )

            job.completed_at = (
                datetime.utcnow()
            )

            db.session.commit()

            raise
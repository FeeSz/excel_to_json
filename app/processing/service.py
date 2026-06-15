from pathlib import Path
from datetime import datetime

from app.core.database import db
from app.core.constants import (
    JOB_PROCESSING,
    JOB_COMPLETED,
    JOB_ERROR,
    LAYOUT_CLIENTES
)

from app.models.conversion_job import ConversionJob

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
        job.status = JOB_PROCESSING

        db.session.commit()
        filepath = Path("storage/uploads") / job.stored_filename
        try:
            if job.layout_type == LAYOUT_CLIENTES:

                df = (
                    ExcelProcessor
                    .processar_clientes(filepath)
                )

            else:

                raise ValueError(
                    f"Layout não suportado: "
                    f"{job.layout_type}"
                )
            output_filename = JsonExporter.exportar(df)
            job.output_filename = output_filename

            job.records_processed = len(df)

            job.status = JOB_COMPLETED

            job.completed_at = datetime.utcnow()
            db.session.commit()
            return job
        
        
        except Exception as erro:
            db.session.rollback()
            job.status = JOB_ERROR
            job.error_message = str(erro)[:500]
            job.completed_at = datetime.utcnow()
            db.session.commit()
            raise
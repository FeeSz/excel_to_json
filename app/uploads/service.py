import uuid

from pathlib import Path

from werkzeug.utils import secure_filename

from flask_login import current_user

from app.core.database import db

from app.core.constants import (
    JOB_PENDING,
    JOB_PROCESSING,
    MAX_PENDING_UPLOADS,
    LAYOUT_CLIENTES
)

from app.models.conversion_job import (
    ConversionJob
)

from app.core.logger import logger

from app.processing.excel_processor import (
    ExcelProcessor
)


class UploadService:

    ALLOWED_EXTENSIONS = {
        "xlsx",
        "xls"
    }

    STORAGE_PATH = Path(
        "storage/uploads"
    )

    @staticmethod
    def salvar_upload(
        file,
        layout_type
    ):

        if layout_type != LAYOUT_CLIENTES:
            raise ValueError(
                "Layout não suportado."
            )

        UploadService.validar_limite_uploads(
            current_user.id
        )

        if not file.filename:

            raise ValueError(
                "Arquivo inválido."
            )

        if "." not in file.filename:

            raise ValueError(
                "Arquivo sem extensão."
            )

        extensao = (
            file.filename
            .rsplit(".", 1)[1]
            .lower()
        )

        if extensao not in (
            UploadService
            .ALLOWED_EXTENSIONS
        ):

            raise ValueError(
                "Formato não suportado."
            )

        UploadService.STORAGE_PATH.mkdir(
            parents=True,
            exist_ok=True
        )

        filename = secure_filename(
            file.filename
        )

        stored_filename = (
            f"{uuid.uuid4()}.{extensao}"
        )

        filepath = (
            UploadService.STORAGE_PATH
            / stored_filename
        )

        file.save(filepath)

        try:

            logger.info(
                f"UPLOAD_VALIDADO | "
                f"user_id={current_user.id} | "
                f"arquivo={file.filename} | "
                f"layout={layout_type}"
            )

            ExcelProcessor.carregar_excel(
                filepath
            )

            job = ConversionJob(
                user_id=current_user.id,
                filename=filename,
                stored_filename=stored_filename,
                layout_type=layout_type,
                status=JOB_PENDING
            )

            db.session.add(job)
            db.session.commit()

            from app.processing.service import (
                ProcessingService
            )

            db.session.add(job)
            db.session.commit()

            logger.info(
                f"JOB_ENFILEIRADO | "
                f"job_id={job.id}"
            )

            logger.info(
                f"JOB_CONCLUIDO | "
                f"job_id={job.id}"
            )

            return job

        except Exception:

            logger.exception(
                f"UPLOAD_ERRO | "
                f"user_id={current_user.id} | "
                f"arquivo={file.filename}"
            )

            filepath.unlink(
                missing_ok=True
            )

            raise ValueError(
                "Arquivo Excel inválido."
            )

    @staticmethod
    def validar_limite_uploads(
        user_id
    ):

        uploads_pendentes = (
            ConversionJob.query
            .filter(
                ConversionJob.user_id == user_id,
                ConversionJob.status.in_([
                    JOB_PENDING,
                    JOB_PROCESSING
                ])
            )
            .count()
        )

        if (
            uploads_pendentes
            >= MAX_PENDING_UPLOADS
        ):

            raise ValueError(
                "Limite de uploads simultâneos atingido."
            )
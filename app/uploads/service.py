import uuid

from pathlib import Path

from werkzeug.utils import secure_filename

from flask_login import current_user

from app.core.database import db
from app.core.constants import JOB_PENDING, JOB_PROCESSING, MAX_PENDING_UPLOADS

from app.models.conversion_job import ConversionJob

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
    def salvar_upload(file):
        
        UploadService.validar_limite_uploads(
            current_user.id
        )

        if not file.filename:

            raise ValueError(
                "Arquivo inválido."
        )
        
        if "." not in file.filename:
            raise ValueError("Arquivo sem extensão.")

        extensao = (
            file.filename
            .rsplit(".", 1)[1]
            .lower()
        )

        if extensao not in UploadService.ALLOWED_EXTENSIONS:

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
            job = ConversionJob(
                user_id=current_user.id,
                filename=filename,
                stored_filename=stored_filename,
                status=JOB_PENDING
            )

            ExcelProcessor.carregar_excel(
                filepath
            )

            db.session.add(job)

            db.session.commit()

            return job
        except Exception:
            filepath.unlink(missing_ok=True)
            raise ValueError(
                "Arquivo Excel inválido."
            )
        
    @staticmethod
    def validar_limite_uploads(user_id):
        uploads_pendentes = (
            ConversionJob.query
            .filter(
                ConversionJob.user_id == user_id,
                ConversionJob.status.in_([
                    JOB_PENDING,
                    JOB_PROCESSING,
                    MAX_PENDING_UPLOADS
                ])
            ).count()
        )
        if uploads_pendentes >= MAX_PENDING_UPLOADS:
            raise ValueError(
                "Limite de uplodas simultâneos atingido."
            )
    upload_limit = db.Column(
    db.Integer,
    default=5
    
)
    
            
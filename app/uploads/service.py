import uuid

from pathlib import Path

from werkzeug.utils import secure_filename

from flask_login import current_user

from app.core.database import db
from app.core.constants import JOB_PENDING

from app.models.conversion_job import ConversionJob


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

        job = ConversionJob(
            user_id=current_user.id,
            filename=filename,
            stored_filename=stored_filename,
            status=JOB_PENDING
        )

        db.session.add(job)

        db.session.commit()

        return job
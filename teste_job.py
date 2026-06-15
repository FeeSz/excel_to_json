from app import create_app
from app.core.database import db

from app.models.conversion_job import ConversionJob

from app.core.constants import JOB_PENDING

app = create_app()

with app.app_context():

    job = ConversionJob(
        user_id=1,
        filename="excel_teste_empresa_1000_registros.xlsx",
        stored_filename="excel_teste_empresa_1000_registros.xlsx",
        status=JOB_PENDING
    )

    db.session.add(job)
    db.session.commit()

    print(f"Job criado: {job.id}")
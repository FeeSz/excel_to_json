from app import create_app

from app.core.database import db

from app.models.conversion_job import ConversionJob

from app.core.constants import JOB_PENDING

app = create_app()

with app.app_context():

    job = ProcessingService.processar_job(
        print(f"Processando Job {job.id}")
        print(f"Arquivo: {job.stored_filename}")
    1
)
    db.session.add(job)

    db.session.commit()

    print(
        f"Job criado: {job.id}"
    )
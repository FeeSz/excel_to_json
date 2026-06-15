from app import create_app

from app.processing.service import (
    ProcessingService
)

app = create_app()

with app.app_context():

    job = ProcessingService.processar_job(
        1
    )

    print(job.id)
    print(job.status)
    print(job.records_processed)
    print(job.output_filename)
from app import create_app

from app.processing.service import (
    ProcessingService
)

app = create_app()

with app.app_context():
    JOB_ID = 2
    job = ProcessingService.processar_job(
        JOB_ID
    )

    print(job.id)
    print(job.status)
    print(job.records_processed)
    print(job.output_filename)
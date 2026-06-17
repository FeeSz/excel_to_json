from app import create_app

from app.worker.service import (
    WorkerService
)

app = create_app()

with app.app_context():

    job = (
        WorkerService
        .buscar_job_pendente()
    )

    print(job)
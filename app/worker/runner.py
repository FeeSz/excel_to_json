import time

from app import create_app

from app.worker.service import (
    WorkerService
)

from app.processing.service import (
    ProcessingService
)

from app.core.logger import logger

app = create_app()


def executar_worker():

    logger.info(
        "WORKER_INICIADO"
    )

    while True:

        with app.app_context():

            job = (
                WorkerService
                .buscar_job_pendente()
            )

            if not job:

                time.sleep(5)
                continue

            logger.info(
                f"JOB_CAPTURADO | "
                f"job_id={job.id}"
            )

            try:

                ProcessingService.processar_job(
                    job.id
                )

                logger.info(
                    f"JOB_FINALIZADO | "
                    f"job_id={job.id}"
                )

            except Exception as erro:

                logger.exception(
                    f"WORKER_ERRO | "
                    f"job_id={job.id}"
                )

        time.sleep(1)


if __name__ == "__main__":

    executar_worker()
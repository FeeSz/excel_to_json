from app import create_app
from app.models.conversion_job import ConversionJob

app = create_app()

with app.app_context():

    job = ConversionJob.query.get(2)

    print("Status:", job.status)
    print("Processados:", job.records_processed)
    print("JSON:", job.output_filename)
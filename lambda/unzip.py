import os
import boto3

def handler(event, context):
    source_key = event['Records'][0]['s3']['object']['key']
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    job_name = os.getenv('JOB_NAME')
    destination_bucket = os.getenv('DEST_BUCKET')
    destination_key = os.getenv('DEST_KEY')
    args = {
        '--source_bucket': source_bucket,
        '--source_key': source_key,
        '--destination_bucket': destination_bucket,
        '--destination_key': destination_key,
    }
    result = boto3.client('glue').start_job_run(JobName=job_name, Arguments=args)
    return result

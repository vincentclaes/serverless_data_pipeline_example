import os
import boto3


def handler(event, context):
    """
    trigger a glue job that will unzip zip files stored on s3.
    """
    # get the source key and bucket from
    # the event that triggered this lambda_function function.
    source_key = event['Records'][0]['s3']['object']['key']
    source_bucket = event['Records'][0]['s3']['bucket']['name']

    # get the destination key and bucket from
    # the environment variables
    glue_job = os.getenv('GLUE_JOB')
    destination_bucket = os.getenv('DEST_BUCKET')
    destination_key = os.getenv('DEST_KEY')

    # build args object and start the glue job
    args = {
        '--source_bucket': source_bucket,
        '--source_key': source_key,
        '--destination_bucket': destination_bucket,
        '--destination_key': destination_key,
    }
    print('args for glue job: {}'.format(args))

    result = boto3.client('glue')\
        .start_job_run(JobName=glue_job, Arguments=args)
    return result

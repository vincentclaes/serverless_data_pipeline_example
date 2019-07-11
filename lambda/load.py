import os
import boto3


def handler(event, context):
    job_name = os.getenv('GLUE_CRAWLER')
    glue_client = boto3.client('glue')
    crawler_metadata = glue_client.get_crawler(Name=job_name)
    crawler_state = crawler_metadata.get('Crawler').get('State')
    if crawler_state == 'READY':
        print('crawler is ready, so we are starting it ...')
        result = glue_client.start_crawler(Name=job_name)
        print('crawler result {}'.format(result))
    print('crawler is in state {}. only start crawler when in state READY'.format(crawler_state))
    return crawler_state

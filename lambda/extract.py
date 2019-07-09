import json
import os
from email import policy
from email.parser import BytesParser

import boto3


def handle(event, context):
    source_key = event['Records'][0]['s3']['object']['key']
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    destination_bucket = os.getenv('DEST_BUCKET')
    destination_key = os.getenv('DEST_KEY')
    s3_object = boto3.client('s3').get_object(Bucket=source_bucket, Key=source_key)["Body"].read()
    email_object = extract_message(s3_object)
    boto3.client('s3').put_object(Body=email_object, Bucket=destination_bucket, Key=destination_key)


def get_address_field_from_email(email_object, field):
    if email_object[field]:
        return email_object[field].addresses[0].addr_spec
    return ''


def extract_message(message_object):
    message_byte_object = BytesParser(policy=policy.default).parse(message_object)
    email_object = {
        'from': get_address_field_from_email(message_byte_object, 'From'),
        'to': get_address_field_from_email(message_byte_object, 'To'),
        'cc': get_address_field_from_email(message_byte_object, 'CC'),
        'subject': str(message_byte_object['subject']),
        'date': str(message_byte_object['Date'].datetime),
        'body': message_byte_object.get_body(preferencelist=('plain')).get_content()
    }

    return json.dumps(email_object)


extract_message(open("/Users/vincent/Desktop/message1.eml", 'rb'))

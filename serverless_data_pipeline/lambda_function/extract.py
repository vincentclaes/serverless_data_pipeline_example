import json
import os
from email import policy
from email.parser import BytesParser

import boto3


def handler(event, context):
    """
    extract the contents from the emails and
    put the resulting object back to s3.
    """
    # get the source key and bucket from
    # the event that triggered this lambda_function function.
    source_key = event['Records'][0]['s3']['object']['key']
    source_bucket = event['Records'][0]['s3']['bucket']['name']

    # get the email name from the key
    email_name = source_key.split('/')[-1]

    # get email from s3,
    s3_client = boto3.client('s3')
    s3_object = s3_client.get_object(Bucket=source_bucket,
                                     Key=source_key)["Body"].read()
    # extract the contents
    email_object = extract_contents(s3_object, email_name)

    # get the destination key and bucket
    # from the environment variables
    destination_bucket = os.getenv('DEST_BUCKET')
    destination_key = os.getenv('DEST_KEY')
    full_s3_key = destination_key + email_name + '.json'

    # dump the result back to s3
    s3_client.put_object(Body=email_object,
                         Bucket=destination_bucket,
                         Key=full_s3_key)
    return full_s3_key


def get_address_from_email(email_object, field):
    if email_object[field]:
        return email_object[field].addresses[0].addr_spec
    return ''


def get_date_field_from_email(email_object):
    if email_object['Date']:
        return str(email_object['Date'].datetime)
    return ''


def extract_contents(message_object, email_name):
    message_byte_object = BytesParser(policy=policy.default) \
        .parsebytes(message_object)

    email_object = {
    'id': email_name,
    'from': get_address_from_email(message_byte_object, 'From'),
    'to': get_address_from_email(message_byte_object, 'To'),
    'cc': get_address_from_email(message_byte_object, 'CC'),
    'subject': str(message_byte_object['subject']),
    'date': get_date_field_from_email(message_byte_object),
    'body': message_byte_object
        .get_body(preferencelist='plain')
        .get_content()
    }

    print('email object {}'.format(email_object))

    return json.dumps(email_object)

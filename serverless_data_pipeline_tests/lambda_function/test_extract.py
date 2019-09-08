import unittest
import os
from serverless_data_pipeline.lambda_function import extract
from moto import mock_s3
import boto3
import json


@mock_s3
class TestExtract(unittest.TestCase):
    DIR_PATH = os.path.dirname(os.path.realpath(__file__))

    SOURCE_BUCKET = "source_bucket"
    DEST_BUCKET = "destination_bucket"
    DEST_KEY = "s3/key/"

    ENV_DEST_KEY = "DEST_KEY"
    ENV_DEST_BUCKET = "DEST_BUCKET"

    def setUp(self):
        os.environ[TestExtract.ENV_DEST_KEY] = TestExtract.DEST_KEY
        os.environ[TestExtract.ENV_DEST_BUCKET] = TestExtract.DEST_BUCKET

        conn = boto3.resource('s3')
        conn.create_bucket(Bucket=TestExtract.SOURCE_BUCKET)
        conn.create_bucket(Bucket=TestExtract.DEST_BUCKET)

    def tearDown(self):
        del os.environ[TestExtract.ENV_DEST_KEY]
        del os.environ[TestExtract.ENV_DEST_BUCKET]

        self.remove_bucket(TestExtract.SOURCE_BUCKET)
        self.remove_bucket(TestExtract.DEST_BUCKET)

    @staticmethod
    def remove_bucket(bucket_name):
        s3_bucket = boto3.resource('s3').Bucket(bucket_name)
        s3_bucket.objects.all().delete()
        s3_bucket.delete()

    @staticmethod
    def get_s3_event(bucket, key):
        return {
            "Records": [
                {
                    "eventVersion": "2.0",
                    "eventSource": "aws:s3",
                    "awsRegion": "us-east-1",
                    "eventTime": "2016-09-25T05:15:44.261Z",
                    "eventName": "ObjectCreated:Put",
                    "userIdentity": {
                        "principalId": "AWS:AROAW5C"
                    },
                    "requestParameters": {
                        "sourceIPAddress": "222.24.107.21"
                    },
                    "responseElements": {
                        "x-amz-request-id": "00093EEAA5C7G7F2",
                        "x-amz-id-2": "9tTklyI/OEj"
                    },
                    "s3": {
                        "s3SchemaVersion": "1.0",
                        "configurationId": "151dfa64",
                        "bucket": {
                            "name": bucket,
                            "ownerIdentity": {
                                "principalId": "A3QLJ3P3P5QY05"
                            },
                            "arn": "arn:aws:s3:::" + bucket
                        },
                        "object": {
                            "key": key,
                            "size": 11,
                            "eTag": "5eb63bbb",
                            "sequencer": "0057E75D80IA35C3E0"
                        }
                    }
                }
            ]
        }

    @staticmethod
    def read_object_bytewise(path):
        return open(path, 'rb')

    @staticmethod
    def put_data_to_s3_object(object_, bucket, s3_source_key):
        boto3.client('s3').put_object(Body=object_,
                                      Bucket=bucket, Key=s3_source_key)

    @staticmethod
    def get_s3_object(bucket, key):
        return boto3.client('s3').get_object(Bucket=bucket, Key=key)

    @staticmethod
    def read_s3_object(bucket, key):
        object_ = TestExtract.get_s3_object(bucket, key)
        return object_['Body'].read()

    def put_email_to_s3(self, test_email_path, email_name):
        with self.read_object_bytewise(test_email_path) as email_object:
            self.put_data_to_s3_object(email_object,
                                       TestExtract.SOURCE_BUCKET, email_name)

    def test_extract_the_contents_of_an_email_successfully(self):
        # arrange
        email_name = 'test_extract_the_contents_of_an_email_successfully.eml'
        test_email_path = os.path.join(self.DIR_PATH, 'resources', email_name)
        self.put_email_to_s3(test_email_path, email_name)

        event = self.get_s3_event(TestExtract.SOURCE_BUCKET, email_name)

        # act
        s3_key_extracted_message = extract.handler(event, None)

        # assert
        email_as_json = self.read_s3_object(TestExtract.DEST_BUCKET, s3_key_extracted_message)
        expected_json = {'id': 'test_extract_the_contents_of_an_email_successfully.eml',
                         'from': 'vclaes1986@gmail.com',
                         'to': 'vincent.v.claes@gmail.com',
                         'cc': '', 'subject': 'Hey how are you doing',
                         'date': '2019-07-09 13:42:54+02:00',
                         'body': '\nCash Me Outside How Bout Dah'}
        self.assertDictEqual(json.loads(email_as_json), expected_json)


if __name__ == '__main__':
    unittest.main()

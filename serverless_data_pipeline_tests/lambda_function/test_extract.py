import unittest
import os
from serverless_data_pipeline.lambda_function import extract
from moto import mock_s3
import boto3
import json


class TestExtract(unittest.TestCase):
    DIR_PATH = os.path.dirname(os.path.realpath(__file__))

    SOURCE_BUCKET = "source_bucket"
    DESTINATION_BUCKET = "destination_bucket"
    DESTINATION_KEY = "s3/key/"

    def setup_test_environment(self):
        os.environ["DEST_KEY"] = TestExtract.DESTINATION_KEY
        os.environ["DEST_BUCKET"] = TestExtract.DESTINATION_BUCKET

        conn = boto3.resource('s3')
        conn.create_bucket(Bucket=TestExtract.SOURCE_BUCKET)
        conn.create_bucket(Bucket=TestExtract.DESTINATION_BUCKET)

    def get_s3_event(self, bucket, key):
        return {
            "Records": [
                {
                    "eventVersion": "2.0",
                    "eventSource": "aws:s3",
                    "awsRegion": "us-east-1",
                    "eventTime": "2016-09-25T05:15:44.261Z",
                    "eventName": "ObjectCreated:Put",
                    "userIdentity": {
                        "principalId": "AWS:AROAW5CA2KAGZPAWYRL7K:cli"
                    },
                    "requestParameters": {
                        "sourceIPAddress": "222.24.107.21"
                    },
                    "responseElements": {
                        "x-amz-request-id": "00093EEAA5C7G7F2",
                        "x-amz-id-2": "9tTklyI/OEj4mco12PgsNksgxAV3KePn7WlNSq2rs+LXD3xFG0tlzgvtH8hClZzI963KYJgVnXw="
                    },
                    "s3": {
                        "s3SchemaVersion": "1.0",
                        "configurationId": "151dfa64-d57a-4383-85ac-620bce65f269",
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
                            "eTag": "5eb63bbbe01eetd093cb22bb8f5acdc3",
                            "sequencer": "0057E75D80IA35C3E0"
                        }
                    }
                }
            ]
        }

    @staticmethod
    def read_object_bytewise(file_name, dir_path, resources='resources'):
        return open(os.path.join(dir_path, resources, file_name), 'rb')

    @staticmethod
    def put_data_to_s3_object(object_, bucket, s3_source_key):
        boto3.client('s3').put_object(Body=object_, Bucket=bucket, Key=s3_source_key)

    @staticmethod
    def get_s3_object(bucket, key):
        return boto3.client('s3').get_object(Bucket=bucket, Key=key)

    @staticmethod
    def read_s3_object(bucket, key):
        """Return a file object as a byte stream."""
        object_ = TestExtract.get_s3_object(bucket, key)
        return object_['Body'].read()

    @mock_s3
    def test_extract_the_contents_of_an_email_successfully(self):
        self.setup_test_environment()
        email_name = 'test_extract_the_contents_of_an_email_successfully.eml'
        email_object = self.read_object_bytewise(email_name, self.DIR_PATH)
        self.put_data_to_s3_object(email_object, TestExtract.SOURCE_BUCKET, email_name)

        event = self.get_s3_event(TestExtract.SOURCE_BUCKET, email_name)
        s3_key_extracted_message = extract.handler(event, None)

        email_as_json = self.read_s3_object(TestExtract.DESTINATION_BUCKET, s3_key_extracted_message)
        expected_json = {'id': 'test_extract_the_contents_of_an_email_successfully.eml', 'from': 'vclaes1986@gmail.com',
                         'to': 'vincent.v.claes@gmail.com', 'cc': '', 'subject': 'Hey how are you doing',
                         'date': '2019-07-09 13:42:54+02:00', 'body': '\nCash Me Outside How Bout Dah'}
        self.assertDictEqual(json.loads(email_as_json), expected_json)


if __name__ == '__main__':
    unittest.main()

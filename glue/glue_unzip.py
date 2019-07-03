# TODO - we should create aws glue job using serverless (or something else)
import io
import logging
import sys
import zipfile

import boto3

"""
aws glue job that unzips email messages.

this job get's triggered by a lambda function, takes source and destination, unzips the object and puts back
the extracted objects back to s3.

this script runs on python 2.7 and uses awsglue libs that only exist in the aws glue environment and only uses default python libraries
because it's a b*tch to add custom libs.

"""


def get_resolved_options():
    # we import this function here because we cannot import this at the beginning of the script
    # when testing the script locally
    from awsglue.utils import getResolvedOptions
    return getResolvedOptions(sys.argv, ['source_bucket', 'source_key', 'destination_bucket', 'destination_key'])


def main():
    # logging.basicConfig(
    #     format='%(levelname)s %(asctime)s: %(message)s',
    #     level=logging.DEBUG
    # )
    # logger = logging.getLogger(__name__)
    # logger.info('starting unzip')
    # args = get_resolved_options()
    # logger.info('args parsed : {}'.format(args))

    # source_bucket = args["source_bucket"]
    # source_key = args["source_key"]
    # destination_bucket = args["destination_bucket"]
    # destination_key = args["destination_key"]

    # s3 = boto3.client('s3')
    # s3_object = boto3.resource('s3').Object(bucket_name=source_bucket, key=source_key)
    # zip_file_byte_object = io.BytesIO(s3_object.get()["Body"].read())
    # zip_file = zipfile.ZipFile(zip_file_byte_object)
    # name_list = zip_file.namelist()
    # ret_val = []
    # for email_path in name_list:
    #     logger.debug('processing email path {}'.format(email_path))
    #     email = zip_file.open(email_path)
    #     email_byte_object = io.BytesIO(email.read())
    #     full_destination_key = destination_key + email_path
    #     logger.debug('uploading object to {}'.format(full_destination_key))
    #     s3.upload_fileobj(email_byte_object, destination_bucket, full_destination_key)
    #     email.close()
    #     ret_val.append(full_destination_key)
    # logger.info('stopped unzip')
    print('helllooooooooooooooo')
    # return ret_val


if __name__ == '__main__':
    main()

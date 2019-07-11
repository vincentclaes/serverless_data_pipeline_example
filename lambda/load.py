import os
import boto3

database = os.getenv('ATHENA_DB')
table = os.getenv('ATHENA_TABLE')
bucket = os.getenv('DEST_BUCKET')
s3_key = os.getenv('DEST_KEY')
athena_client = boto3.client('athena')
config = {'OutputLocation': 's3://{}/athena_output'.format(bucket)}
result_create_db = athena_client.start_query_execution(
    QueryString='CREATE DATABASE IF NOT EXISTS {};'.format(database),
    ResultConfiguration=config
)
print('create db {}'.format(result_create_db))
context = {'Database': '{}'.format(bucket)}
result_create_table = athena_client.start_query_execution(QueryString='''
CREATE EXTERNAL TABLE IF NOT EXISTS {}.{} (
      `id` string,
      `from` string,
      `to` string,
      `cc` string,
      `subject` string,
      `date` string,
      `body` string
      )
      ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
      WITH SERDEPROPERTIES ('serialization.format' = '1')
      LOCATION 's3://{}/{}'
      TBLPROPERTIES ('has_encrypted_data'='false');
'''.format(database, table, bucket, s3_key), QueryExecutionContext=context, ResultConfiguration=config)

print('create table {}'.format(result_create_table))

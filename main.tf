variable "stage" {}

provider "aws" {
  region = "eu-central-1"
}
resource "aws_s3_bucket" "example" {
  bucket = "serverless-data-pipeline-${var.stage}-glue-script"
  acl    = "private"
}
resource "aws_s3_bucket_object" "object" {
  bucket = "serverless-data-pipeline-${var.stage}-glue-script"
  key    = "glue_unzip.py"
  source = "glue/glue_unzip.py"

  # The filemd5() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the md5() function and the file() function:
  # etag = "${md5(file("path/to/file"))}"
  etag = "${filemd5("glue/glue_unzip.py")}"
}
resource "aws_glue_job" "glue_unzip" {
  name     = "serverless-data-pipeline-${var.stage}"
  role_arn = "arn:aws:iam::077590795309:role/glue-admin"
  max_capacity = 1
  command {
    name="pythonshell"
    script_location = "s3://${aws_s3_bucket.example.bucket}/glue_unzip.py"
  }
  execution_property {
    max_concurrent_runs = 2
  }

}

# resource "aws_lambda_function" "lambda_function" {
#   role             = "arn:aws:iam::077590795309:role/serverless-data-pipeline-lambda"
#   handler          = "${var.handler}"
#   runtime          = "python3.6"
#   filename         = "lambda.zip"
#   function_name    = "${var.function_name}"
#   source_code_hash = "${base64sha256(file("lambda.zip"))}"
# }
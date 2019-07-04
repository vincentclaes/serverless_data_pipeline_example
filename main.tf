variable "stage" {}

provider "aws" {
  region = "eu-central-1"
}
resource "aws_s3_bucket" "example" {
  bucket = "serverless-data-pipeline-${var.stage}-example"
  acl    = "private"

  tags = {
    Name        = "My bucket"
    Environment = "Dev"
    Stage = "${var.stage}"
  }
}
resource "aws_glue_job" "example" {
  name     = "serverless-data-pipelinep-${var.stage}"
  role_arn = "arn:aws:iam::077590795309:role/glue-admin"

  command {
    script_location = "s3://${aws_s3_bucket.example.bucket}/example.py"
  }
}
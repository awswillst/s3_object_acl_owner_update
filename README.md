# Overview
This function does an in-place copy of objects as they are created in an S3 bucket to force ownership update to the bucket owner.  This is to solve for cases where objects are created by external accounts and services, such as VPC Flow logs and load-balancer logs.

## How-to
1. Create IAM role and permissions policy for Lambda function.  Requires:
* AWSLambdaBasicExecutionRole policy
* Policy with s3 APIs on the bucket and/or prefix
  * PutObject
  * GetObjectAcl
  * s3:GetObject
  * s3:GetObjectTagging
  * PutObjectTagging
  * PutObjectAcl

1. Create a Lambda function, using execution role from previous step

1. Add an event to the S3 bucket, with these parameters:
* Event: All object create events
* Prefix: Prefix where logs are stored
* Suffix: Suffix for logs being created
* Send to: Lambda function
* Lambda: Lambda created in previous step

Recommend: Monitor the function's CloudWatch Logs for any errors or looping conditions.

## To do
* Nice to have: CloudFormation support for deployment


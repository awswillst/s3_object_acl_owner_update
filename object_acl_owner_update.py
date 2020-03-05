import boto3
import json
import logging

logging.basicConfig(format='%(levelname)s: %(asctime)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    s3 = boto3.client('s3')

    for record in event['Records']:
        bucketName = record['s3']['bucket']['name']
        objectKey = record['s3']['object']['key']

        logger.info('Getting ACL for {0}'.format(objectKey))

        currentOwner = s3.get_object_acl(
            Bucket = bucketName, Key = objectKey
        )['Owner']['ID']
        
        ownerCanonicalAccountId = s3.get_bucket_acl(Bucket = bucketName)['Owner']['ID']
        if currentOwner == ownerCanonicalAccountId:
            logger.info('Owner already set for {}'.format(objectKey))
            aclSuccess = True
        else:
            s3cp = s3.copy_object(
                Bucket = bucketName,
                Key = objectKey,
                CopySource = {'Bucket': bucketName, 'Key': objectKey},
                ACL = 'bucket-owner-full-control',
                MetadataDirective = 'REPLACE'
            )
            
            if s3cp['ResponseMetadata']['HTTPStatusCode'] == 200:
                logger.info('Successfully set ACL for {0}'.format(objectKey))
                aclSuccess = True
            else:
                logger.error('Failed to set ACL for {0}'.format(objectKey))
                logger.error(s3cp)
                aclSuccess = False


    # TODO implement
    return aclSuccess

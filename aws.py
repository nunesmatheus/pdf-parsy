import boto3
import os


def s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=os.environ.get('S3_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('S3_SECRET_ACCESS_KEY')
    )


def s3_bucket():
    return os.environ.get('S3_BUCKET')

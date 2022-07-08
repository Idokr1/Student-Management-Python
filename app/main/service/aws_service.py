from app.main import Config
import logging
import boto3
from botocore.exceptions import ClientError

def upload_file(file , path):
  account_key = Config.AWS_ACCESSKEY
  account_secret = Config.AWS_SECRETKEY
  bucket_url = Config.BUCKET_URL

  s3_resource = boto3.resource(
    's3',
    aws_access_key_id=account_key,
    aws_secret_access_key=account_secret)

  bucket = s3_resource.Bucket(bucket_url)

  bucket.Object(path).put(Body=file.read())


def create_presigned_url(object_name, expiration=3600):
    account_key = Config.AWS_ACCESSKEY
    account_secret = Config.AWS_SECRETKEY
    bucket_name = Config.BUCKET_URL

    s3_client = boto3.client('s3',
                             region_name='eu-central-1',
                             aws_access_key_id=account_key,
                             aws_secret_access_key=account_secret)
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    return response
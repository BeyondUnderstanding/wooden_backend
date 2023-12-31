import boto3
import smsto
from mypy_boto3_s3.client import S3Client

from src.config import AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, SMSTO_TOKEN


def make_s3() -> S3Client:
    session = boto3.session.Session()
    s3: S3Client = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    return s3


sms = smsto.SMSTo(token=SMSTO_TOKEN)
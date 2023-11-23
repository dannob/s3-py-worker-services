import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import logging
from typing import List

# Initialize the S3 client
s3_client = boto3.client('s3')

def upload_file_to_s3(file_path: str, bucket_name: str, object_name: str) -> bool:
    """
    Upload a file to an S3 bucket.
    
    :param file_path: Path to the file to upload
    :param bucket_name: Name of the S3 bucket
    :param object_name: Object name in S3
    :return: True if upload was successful, False otherwise
    """
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        return True
    except NoCredentialsError:
        logging.error("Credentials not available")
        return False
    except ClientError as e:
        logging.error(e)
        return False

def download_file_from_s3(bucket_name: str, object_name: str, file_path: str) -> bool:
    """
    Download a file from an S3 bucket.
    
    :param bucket_name: Name of the S3 bucket
    :param object_name: Object name in S3
    :param file_path: Path where the file will be saved
    :return: True if download was successful, False otherwise
    """
    try:
        s3_client.download_file(bucket_name, object_name, file_path)
        return True
    except NoCredentialsError:
        logging.error("Credentials not available")
        return False
    except ClientError as e:
        logging.error(e)
        return False

def list_files_in_s3(bucket_name: str) -> List[str]:
    """
    List all files in an S3 bucket.
    
    :param bucket_name: Name of the S3 bucket
    :return: List of file names
    """
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        return [obj['Key'] for obj in response.get('Contents', [])]
    except ClientError as e:
        logging.error(e)
        return []

def delete_file_from_s3(bucket_name: str, object_name: str) -> bool:
    """
    Delete a file from an S3 bucket.
    
    :param bucket_name: Name of the S3 bucket
    :param object_name: Object name in S3
    :return: True if deletion was successful, False otherwise
    """
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=object_name)
        return True
    except ClientError as e:
        logging.error(e)
        return False

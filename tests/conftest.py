import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
from moto import mock_aws
import boto3


@pytest.fixture
def mock_s3_service():
    """Mock S3 service for integration tests using moto."""
    with mock_aws():
        # Create a mock S3 client and bucket
        s3_client = boto3.client('s3', region_name='us-east-1')
        bucket_name = 'test-bucket'
        s3_client.create_bucket(Bucket=bucket_name)
        yield s3_client, bucket_name


@pytest.fixture
def temp_file():
    """Create a temporary file for testing."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(b"This is test file content for testing purposes")
        tmp_file.flush()
        yield tmp_file.name
    
    # Cleanup
    if os.path.exists(tmp_file.name):
        os.unlink(tmp_file.name)


@pytest.fixture
def sample_files():
    """Create multiple sample files for testing."""
    files = []
    for i in range(3):
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'_test_{i}.txt') as tmp_file:
            tmp_file.write(f"Content of test file {i}".encode())
            tmp_file.flush()
            files.append(tmp_file.name)
    
    yield files
    
    # Cleanup
    for file_path in files:
        if os.path.exists(file_path):
            os.unlink(file_path)


@pytest.fixture
def temp_directory():
    """Create a temporary directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    
    # Cleanup
    import shutil
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


@pytest.fixture(autouse=True)
def cleanup_temp_files():
    """Automatically cleanup temp files created during tests."""
    yield
    
    # Cleanup any temp files that might have been created
    temp_dir = "temp"
    if os.path.exists(temp_dir):
        import shutil
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
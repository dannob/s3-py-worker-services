import pytest
from unittest.mock import Mock, patch, MagicMock
from botocore.exceptions import NoCredentialsError, ClientError
import my_services


class TestUploadFileToS3:
    
    @patch('my_services.s3_client')
    def test_upload_file_success(self, mock_s3_client):
        mock_s3_client.upload_file.return_value = None
        
        result = my_services.upload_file_to_s3(
            file_path="/test/path/file.txt",
            bucket_name="test-bucket",
            object_name="test-object"
        )
        
        assert result is True
        mock_s3_client.upload_file.assert_called_once_with(
            "/test/path/file.txt", "test-bucket", "test-object"
        )
    
    @patch('my_services.s3_client')
    def test_upload_file_no_credentials(self, mock_s3_client):
        mock_s3_client.upload_file.side_effect = NoCredentialsError()
        
        result = my_services.upload_file_to_s3(
            file_path="/test/path/file.txt",
            bucket_name="test-bucket",
            object_name="test-object"
        )
        
        assert result is False
    
    @patch('my_services.s3_client')
    def test_upload_file_client_error(self, mock_s3_client):
        mock_s3_client.upload_file.side_effect = ClientError(
            error_response={'Error': {'Code': 'NoSuchBucket', 'Message': 'Bucket does not exist'}},
            operation_name='upload_file'
        )
        
        result = my_services.upload_file_to_s3(
            file_path="/test/path/file.txt",
            bucket_name="test-bucket",
            object_name="test-object"
        )
        
        assert result is False


class TestDownloadFileFromS3:
    
    @patch('my_services.s3_client')
    def test_download_file_success(self, mock_s3_client):
        mock_s3_client.download_file.return_value = None
        
        result = my_services.download_file_from_s3(
            bucket_name="test-bucket",
            object_name="test-object",
            file_path="/test/path/file.txt"
        )
        
        assert result is True
        mock_s3_client.download_file.assert_called_once_with(
            "test-bucket", "test-object", "/test/path/file.txt"
        )
    
    @patch('my_services.s3_client')
    def test_download_file_no_credentials(self, mock_s3_client):
        mock_s3_client.download_file.side_effect = NoCredentialsError()
        
        result = my_services.download_file_from_s3(
            bucket_name="test-bucket",
            object_name="test-object",
            file_path="/test/path/file.txt"
        )
        
        assert result is False
    
    @patch('my_services.s3_client')
    def test_download_file_client_error(self, mock_s3_client):
        mock_s3_client.download_file.side_effect = ClientError(
            error_response={'Error': {'Code': 'NoSuchKey', 'Message': 'Key does not exist'}},
            operation_name='download_file'
        )
        
        result = my_services.download_file_from_s3(
            bucket_name="test-bucket",
            object_name="test-object",
            file_path="/test/path/file.txt"
        )
        
        assert result is False


class TestListFilesInS3:
    
    @patch('my_services.s3_client')
    def test_list_files_success(self, mock_s3_client):
        mock_s3_client.list_objects_v2.return_value = {
            'Contents': [
                {'Key': 'file1.txt'},
                {'Key': 'file2.txt'},
                {'Key': 'folder/file3.txt'}
            ]
        }
        
        result = my_services.list_files_in_s3("test-bucket")
        
        assert result == ['file1.txt', 'file2.txt', 'folder/file3.txt']
        mock_s3_client.list_objects_v2.assert_called_once_with(Bucket="test-bucket")
    
    @patch('my_services.s3_client')
    def test_list_files_empty_bucket(self, mock_s3_client):
        mock_s3_client.list_objects_v2.return_value = {}
        
        result = my_services.list_files_in_s3("test-bucket")
        
        assert result == []
    
    @patch('my_services.s3_client')
    def test_list_files_client_error(self, mock_s3_client):
        mock_s3_client.list_objects_v2.side_effect = ClientError(
            error_response={'Error': {'Code': 'NoSuchBucket', 'Message': 'Bucket does not exist'}},
            operation_name='list_objects_v2'
        )
        
        result = my_services.list_files_in_s3("test-bucket")
        
        assert result == []


class TestDeleteFileFromS3:
    
    @patch('my_services.s3_client')
    def test_delete_file_success(self, mock_s3_client):
        mock_s3_client.delete_object.return_value = None
        
        result = my_services.delete_file_from_s3(
            bucket_name="test-bucket",
            object_name="test-object"
        )
        
        assert result is True
        mock_s3_client.delete_object.assert_called_once_with(
            Bucket="test-bucket", Key="test-object"
        )
    
    @patch('my_services.s3_client')
    def test_delete_file_client_error(self, mock_s3_client):
        mock_s3_client.delete_object.side_effect = ClientError(
            error_response={'Error': {'Code': 'NoSuchKey', 'Message': 'Key does not exist'}},
            operation_name='delete_object'
        )
        
        result = my_services.delete_file_from_s3(
            bucket_name="test-bucket",
            object_name="test-object"
        )
        
        assert result is False
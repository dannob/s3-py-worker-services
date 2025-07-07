import pytest
from pydantic import ValidationError
from my_schemas import (
    FileUploadRequest,
    FileUploadResponse,
    FileDownloadRequest,
    FileDownloadResponse,
    FileListResponse,
    FileDeleteRequest,
    FileDeleteResponse
)


class TestFileUploadRequest:
    
    def test_valid_upload_request(self):
        data = {
            "bucket_name": "test-bucket",
            "file_path": "/path/to/file.txt",
            "object_name": "uploads/file.txt",
            "description": "Test file upload"
        }
        
        request = FileUploadRequest(**data)
        
        assert request.bucket_name == "test-bucket"
        assert request.file_path == "/path/to/file.txt"
        assert request.object_name == "uploads/file.txt"
        assert request.description == "Test file upload"
    
    def test_upload_request_without_optional_fields(self):
        data = {
            "bucket_name": "test-bucket",
            "file_path": "/path/to/file.txt"
        }
        
        request = FileUploadRequest(**data)
        
        assert request.bucket_name == "test-bucket"
        assert request.file_path == "/path/to/file.txt"
        assert request.object_name is None
        assert request.description is None
    
    def test_upload_request_missing_required_fields(self):
        with pytest.raises(ValidationError):
            FileUploadRequest(bucket_name="test-bucket")
        
        with pytest.raises(ValidationError):
            FileUploadRequest(file_path="/path/to/file.txt")


class TestFileUploadResponse:
    
    def test_valid_upload_response(self):
        data = {
            "message": "File uploaded successfully",
            "object_name": "uploads/file.txt",
            "bucket_name": "test-bucket"
        }
        
        response = FileUploadResponse(**data)
        
        assert response.message == "File uploaded successfully"
        assert response.object_name == "uploads/file.txt"
        assert response.bucket_name == "test-bucket"
    
    def test_upload_response_missing_required_fields(self):
        with pytest.raises(ValidationError):
            FileUploadResponse(message="Success", object_name="file.txt")


class TestFileDownloadRequest:
    
    def test_valid_download_request(self):
        data = {
            "bucket_name": "test-bucket",
            "object_name": "downloads/file.txt"
        }
        
        request = FileDownloadRequest(**data)
        
        assert request.bucket_name == "test-bucket"
        assert request.object_name == "downloads/file.txt"
    
    def test_download_request_missing_required_fields(self):
        with pytest.raises(ValidationError):
            FileDownloadRequest(bucket_name="test-bucket")
        
        with pytest.raises(ValidationError):
            FileDownloadRequest(object_name="file.txt")


class TestFileDownloadResponse:
    
    def test_valid_download_response(self):
        data = {
            "message": "File downloaded successfully",
            "file_path": "/tmp/downloaded_file.txt"
        }
        
        response = FileDownloadResponse(**data)
        
        assert response.message == "File downloaded successfully"
        assert response.file_path == "/tmp/downloaded_file.txt"
    
    def test_download_response_missing_required_fields(self):
        with pytest.raises(ValidationError):
            FileDownloadResponse(message="Success")
        
        with pytest.raises(ValidationError):
            FileDownloadResponse(file_path="/tmp/file.txt")


class TestFileListResponse:
    
    def test_valid_list_response(self):
        data = {
            "bucket_name": "test-bucket",
            "files": ["file1.txt", "file2.txt", "folder/file3.txt"]
        }
        
        response = FileListResponse(**data)
        
        assert response.bucket_name == "test-bucket"
        assert response.files == ["file1.txt", "file2.txt", "folder/file3.txt"]
    
    def test_list_response_empty_files(self):
        data = {
            "bucket_name": "test-bucket",
            "files": []
        }
        
        response = FileListResponse(**data)
        
        assert response.bucket_name == "test-bucket"
        assert response.files == []
    
    def test_list_response_missing_required_fields(self):
        with pytest.raises(ValidationError):
            FileListResponse(bucket_name="test-bucket")
        
        with pytest.raises(ValidationError):
            FileListResponse(files=["file1.txt"])


class TestFileDeleteRequest:
    
    def test_valid_delete_request(self):
        data = {
            "bucket_name": "test-bucket",
            "object_name": "file-to-delete.txt"
        }
        
        request = FileDeleteRequest(**data)
        
        assert request.bucket_name == "test-bucket"
        assert request.object_name == "file-to-delete.txt"
    
    def test_delete_request_missing_required_fields(self):
        with pytest.raises(ValidationError):
            FileDeleteRequest(bucket_name="test-bucket")
        
        with pytest.raises(ValidationError):
            FileDeleteRequest(object_name="file.txt")


class TestFileDeleteResponse:
    
    def test_valid_delete_response(self):
        data = {
            "message": "File deleted successfully"
        }
        
        response = FileDeleteResponse(**data)
        
        assert response.message == "File deleted successfully"
    
    def test_delete_response_missing_required_fields(self):
        with pytest.raises(ValidationError):
            FileDeleteResponse()
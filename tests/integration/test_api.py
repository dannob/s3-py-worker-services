import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import tempfile
import os
from io import BytesIO

from main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample_file():
    content = b"This is a test file content"
    return BytesIO(content)


class TestRootEndpoint:
    
    def test_root_redirects_to_docs(self, client):
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/docs"


class TestFileUploadEndpoint:
    
    @patch('my_services.upload_file_to_s3')
    def test_upload_file_success(self, mock_upload, client):
        mock_upload.return_value = True
        
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(b"test content")
            tmp_file.flush()
            
            with open(tmp_file.name, 'rb') as f:
                response = client.post(
                    "/upload/?bucket=test-bucket",
                    files={"file_upload": ("test.txt", f, "text/plain")}
                )
            
            os.unlink(tmp_file.name)
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "File uploaded successfully"
        assert data["object_name"] == "test.txt"
        assert data["bucket_name"] == "test-bucket"
    
    @patch('my_services.upload_file_to_s3')
    def test_upload_file_failure(self, mock_upload, client):
        mock_upload.return_value = False
        
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(b"test content")
            tmp_file.flush()
            
            with open(tmp_file.name, 'rb') as f:
                response = client.post(
                    "/upload/?bucket=test-bucket",
                    files={"file_upload": ("test.txt", f, "text/plain")}
                )
            
            os.unlink(tmp_file.name)
        
        assert response.status_code == 500
        data = response.json()
        assert data["detail"] == "File upload failed"
    
    def test_upload_file_missing_file(self, client):
        response = client.post("/upload/?bucket=test-bucket")
        assert response.status_code == 422


class TestFileDownloadEndpoint:
    
    @patch('my_services.download_file_from_s3')
    def test_download_file_success(self, mock_download, client):
        mock_download.return_value = True
        
        response = client.get("/download/?bucket=test-bucket&object_name=test.txt")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "File downloaded successfully"
        assert data["file_path"] == "temp/test.txt"
    
    @patch('my_services.download_file_from_s3')
    def test_download_file_failure(self, mock_download, client):
        mock_download.return_value = False
        
        response = client.get("/download/?bucket=test-bucket&object_name=test.txt")
        
        assert response.status_code == 500
        data = response.json()
        assert data["detail"] == "File download failed"
    
    def test_download_file_missing_params(self, client):
        response = client.get("/download/?bucket=test-bucket")
        assert response.status_code == 422
        
        response = client.get("/download/?object_name=test.txt")
        assert response.status_code == 422


class TestFileListEndpoint:
    
    @patch('my_services.list_files_in_s3')
    def test_list_files_success(self, mock_list, client):
        mock_list.return_value = ["file1.txt", "file2.txt", "folder/file3.txt"]
        
        response = client.get("/list/?bucket=test-bucket")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["bucket_name"] == "test-bucket"
        assert data[0]["files"] == ["file1.txt", "file2.txt", "folder/file3.txt"]
    
    @patch('my_services.list_files_in_s3')
    def test_list_files_empty(self, mock_list, client):
        mock_list.return_value = []
        
        response = client.get("/list/?bucket=test-bucket")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["bucket_name"] == "test-bucket"
        assert data[0]["files"] == []
    
    def test_list_files_missing_bucket(self, client):
        response = client.get("/list/")
        assert response.status_code == 422


class TestFileDeleteEndpoint:
    
    @patch('my_services.delete_file_from_s3')
    def test_delete_file_success(self, mock_delete, client):
        mock_delete.return_value = True
        
        response = client.delete("/delete/?bucket=test-bucket&object_name=test.txt")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "File deleted successfully"
    
    @patch('my_services.delete_file_from_s3')
    def test_delete_file_failure(self, mock_delete, client):
        mock_delete.return_value = False
        
        response = client.delete("/delete/?bucket=test-bucket&object_name=test.txt")
        
        assert response.status_code == 500
        data = response.json()
        assert data["detail"] == "File deletion failed"
    
    def test_delete_file_missing_params(self, client):
        response = client.delete("/delete/?bucket=test-bucket")
        assert response.status_code == 422
        
        response = client.delete("/delete/?object_name=test.txt")
        assert response.status_code == 422


class TestEndToEndWorkflow:
    
    @patch('my_services.upload_file_to_s3')
    @patch('my_services.list_files_in_s3')
    @patch('my_services.download_file_from_s3')
    @patch('my_services.delete_file_from_s3')
    def test_complete_file_lifecycle(self, mock_delete, mock_download, mock_list, mock_upload, client):
        # Mock all service calls to succeed
        mock_upload.return_value = True
        mock_list.return_value = ["test.txt"]
        mock_download.return_value = True
        mock_delete.return_value = True
        
        # 1. Upload file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(b"test content")
            tmp_file.flush()
            
            with open(tmp_file.name, 'rb') as f:
                upload_response = client.post(
                    "/upload/?bucket=test-bucket",
                    files={"file_upload": ("test.txt", f, "text/plain")}
                )
            
            os.unlink(tmp_file.name)
        
        assert upload_response.status_code == 200
        
        # 2. List files
        list_response = client.get("/list/?bucket=test-bucket")
        assert list_response.status_code == 200
        assert "test.txt" in list_response.json()[0]["files"]
        
        # 3. Download file
        download_response = client.get("/download/?bucket=test-bucket&object_name=test.txt")
        assert download_response.status_code == 200
        
        # 4. Delete file
        delete_response = client.delete("/delete/?bucket=test-bucket&object_name=test.txt")
        assert delete_response.status_code == 200
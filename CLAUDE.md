# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI-based S3 file management service that provides CRUD operations for AWS S3 buckets. The application allows users to upload, download, list, and delete files from S3 buckets through REST API endpoints.

## Architecture

- **main.py**: FastAPI application with endpoints for S3 operations (upload, download, list, delete)
- **my_services.py**: Core S3 service functions using boto3 client
- **my_schemas.py**: Pydantic models for request/response validation
- **test_main.http**: HTTP test file for endpoint testing

## Development Commands

### Setup and Installation
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running the Application
```bash
uvicorn main:app --reload
```
Note: The README mentions `uvicorn app.main:app --reload` but the correct command is `uvicorn main:app --reload` based on the actual file structure.

### Testing

#### Running Tests
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/unit/test_services.py

# Run specific test class
pytest tests/unit/test_services.py::TestUploadFileToS3

# Run specific test method
pytest tests/unit/test_services.py::TestUploadFileToS3::test_upload_file_success

# Run integration tests only
pytest tests/integration/

# Run unit tests only
pytest tests/unit/
```

#### Test Structure
- **Unit Tests**: `tests/unit/` - Mock S3 client, test individual functions
- **Integration Tests**: `tests/integration/` - Test API endpoints with FastAPI TestClient
- **Fixtures**: `tests/conftest.py` - Shared test utilities and cleanup
- **Configuration**: `pytest.ini` - Test runner configuration and coverage settings

#### Manual Testing
- Use the provided `test_main.http` file for HTTP endpoint testing
- Access interactive API docs at http://127.0.0.1:8000/docs (root endpoint redirects here)

## AWS Configuration

The application requires AWS credentials to be configured. These can be set via:
- AWS credentials file (~/.aws/credentials)
- Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
- IAM roles (for EC2/ECS deployments)

## Key Implementation Details

### File Upload Flow
1. Files are temporarily stored in `temp/` directory
2. Files are uploaded to S3 using boto3 client
3. Local temp files should be cleaned up after upload

### Error Handling
- All S3 operations include error handling for NoCredentialsError and ClientError
- HTTP exceptions are raised with appropriate status codes (500 for service errors)

### Schema Issue
There's a bug in my_schemas.py:60 - `FileDeleteRequest` is missing the `class` keyword and should be `class FileDeleteRequest(BaseModel):`

## Development Notes

- The application uses a simple file-based temporary storage approach
- S3 client is initialized globally in my_services.py
- All endpoints follow RESTful conventions with appropriate HTTP methods
- Response models ensure consistent API contract
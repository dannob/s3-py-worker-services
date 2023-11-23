from pydantic import BaseModel
from typing import Optional, List


class FileUploadRequest(BaseModel):
    bucket_name: str
    file_path: str
    object_name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "bucket_name": "my-s3-bucket",
                "file_path": "/path/to/local/file.jpg",
                "object_name": "folder/file.jpg",
                "description": "An example file"
            }
        }


class FileUploadResponse(BaseModel):
    message: str
    object_name: str
    bucket_name: str

    class Config:
        schema_extra = {
            "example": {
                "message": "File uploaded successfully",
                "object_name": "folder/file.jpg",
                "bucket_name": "my-s3-bucket"
            }
        }


class FileDownloadRequest(BaseModel):
    bucket_name: str
    object_name: str

    class Config:
        schema_extra = {
            "example": {
                "bucket_name": "my-s3-bucket",
                "object_name": "folder/file.jpg"
            }
        }


class FileDownloadResponse(BaseModel):
    message: str
    file_path: str


class FileListResponse(BaseModel):
    bucket_name: str
    files: List[str]


def FileDeleteRequest(BaseModel):
    bucket_name: str
    object_name: str

    class Config:
        schema_extra = {
            "example": {
                "bucket_name": "my-s3-bucket",
                "object_name": "folder/file.jpg"
            }
        }


class FileDeleteResponse(BaseModel):
    message: str

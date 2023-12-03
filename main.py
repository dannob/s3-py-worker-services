"""Module providing CRUD operations for S3."""
from typing import List

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import RedirectResponse

import my_schemas
import my_services


app = FastAPI()

@app.get("/")
async def root():
    """Redirect to OpenAPI docs"""
    return RedirectResponse(url='/docs')


@app.post("/upload/", response_model=my_schemas.FileUploadRequest)
async def upload_file(file_upload: UploadFile = File(...), bucket: str = "your-default-bucket"):
    """Upload file to S3"""
    file_location = f"temp/{file_upload.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file_upload.file.read())

    success = my_services.upload_file_to_s3(file_location, bucket, file_upload.filename)
    if success:
        return {"message": "File uploaded successfully",
                "object_name": file_upload.filename, "bucket_name": bucket}
    raise HTTPException(status_code=500, detail="File upload failed")


@app.get("/download/", response_model=my_schemas.FileDownloadResponse)
async def download_file(bucket: str, object_name: str):
    """Download file from S3"""
    file_path = f"temp/{object_name}"
    success = my_services.download_file_from_s3(bucket, object_name, file_path)
    if success:
        return {"message": "File downloaded successfully", "file_path": file_path}
    raise HTTPException(status_code=500, detail="File download failed")


@app.get("/list/", response_model=List[my_schemas.FileListResponse])
async def list_files(bucket: str):
    """List files from S3"""
    file_names = my_services.list_files_in_s3(bucket)
    return [{"bucket_name": bucket, "files": file_names}]


@app.delete("/delete/", response_model=my_schemas.FileDeleteResponse)
async def delete_file(bucket: str, object_name: str):
    """Delete file from S3"""
    success = my_services.delete_file_from_s3(bucket, object_name)
    if success:
        return {"message": "File deleted successfully"}
    raise HTTPException(status_code=500, detail="File deletion failed")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

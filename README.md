# s3 Py FastAPI Services

This project is built using FastAPI and demonstrates a simple CRUD API with file handling operations against an AWS S3 bucket.

## Prerequisites

Before you begin, ensure you have met the following requirements:
* You have installed Python 3.10 or higher.
* You have a basic understanding of Python and FastAPI.

## Installing s3 Py FastAPI Project

To install the s3 Python FastAPI Project, follow these steps:

Linux and macOS:

```bash
git clone https://github.com/dannob/s3-py-worker-services.git
cd s3-py-worker-services
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Running the project
```bash
uvicorn app.main:app --reload


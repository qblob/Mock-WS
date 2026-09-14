from minio import Minio

from core.config import (
    MINIO_ACCESS_KEY,
    MINIO_BROWSER_URL,
    MINIO_BUCKET,
    MINIO_HOST,
    MINIO_SECRET_KEY,
)

MINIO_CLIENT = Minio(
    MINIO_HOST,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False,
)

BUCKET_NAME = MINIO_BUCKET
BROWSER_URL = MINIO_BROWSER_URL
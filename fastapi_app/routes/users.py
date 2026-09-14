import base64

from fastapi import APIRouter, Depends, HTTPException
from minio.error import S3Error
from sqlalchemy import select

from core.database import async_session
from core.models import Profile, User
from fastapi_app.auth import verify_api_key
from django_app.users.minio_client import BUCKET_NAME, MINIO_CLIENT


router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
    dependencies=[Depends(verify_api_key)],
)


@router.get("/get/profile/{userid}")
async def get_profile(userid: int):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.id == userid)
        )

        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )

        return {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }


@router.get("/get/photo/{userid}")
async def get_photo(userid: int):
    async with async_session() as session:
        result = await session.execute(
            select(Profile).where(Profile.user_id == userid)
        )

        profile = result.scalar_one_or_none()

        if profile is None:
            raise HTTPException(
                status_code=404,
                detail="Profile not found",
            )

        if not profile.photo:
            raise HTTPException(
                status_code=404,
                detail="User has no photo",
            )

        object_name = profile.photo

    try:
        response = MINIO_CLIENT.get_object(
            BUCKET_NAME,
            object_name,
        )

        image_data = response.read()

        response.close()
        response.release_conn()

    except S3Error:
        raise HTTPException(
            status_code=404,
            detail="Photo not found in storage",
        )

    encoded_image = base64.b64encode(image_data).decode("utf-8")

    return {
        "userid": userid,
        "photo": encoded_image,
    }
from fastapi import APIRouter, Depends

from core.worker_status import get_worker_status
from fastapi_app.auth import verify_api_key


router = APIRouter(
    prefix="/api/workers",
    tags=["Workers"],
    dependencies=[Depends(verify_api_key)],
)


@router.get("/status")
async def get_status():
    return await get_worker_status()
from fastapi import Header, HTTPException

from core.config import FASTAPI_API_KEY


async def verify_api_key(
    x_api_key: str | None = Header(default=None),
):
    if x_api_key != FASTAPI_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key",
        )
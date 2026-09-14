from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from core.database import async_session
from core.models import RTDS
from fastapi_app.auth import verify_api_key


router = APIRouter(
    prefix="/api/RTDS",
    tags=["RTDS"],
    dependencies=[Depends(verify_api_key)],
)


@router.get("/get/current/{id}")
async def get_current(id: str):
    async with async_session() as session:
        result = await session.execute(
            select(RTDS)
            .where(RTDS.instrument_id == id)
            .order_by(RTDS.timestamp.desc())
            .limit(1)
        )

        record = result.scalar_one_or_none()

        if record is None:
            raise HTTPException(
                status_code=404,
                detail="RTDS record not found",
            )

        return {
            "id": record.id,
            "instrument_id": record.instrument_id,
            "price": record.price,
            "timestamp": record.timestamp,
        }


@router.get("/get/historical/{id}")
async def get_historical(id: str):
    async with async_session() as session:
        result = await session.execute(
            select(RTDS)
            .where(RTDS.instrument_id == id)
            .order_by(RTDS.timestamp)
        )

        records = result.scalars().all()

        if not records:
            raise HTTPException(
                status_code=404,
                detail="No RTDS records found",
            )

        return [
            {
                "id": record.id,
                "instrument_id": record.instrument_id,
                "price": record.price,
                "timestamp": record.timestamp,
            }
            for record in records
        ]
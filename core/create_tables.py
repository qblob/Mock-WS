import asyncio

from core.database import engine
from core.models import RTDS


async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(
            RTDS.metadata.create_all,
            tables=[RTDS.__table__],
        )


if __name__ == "__main__":
    asyncio.run(create_tables())
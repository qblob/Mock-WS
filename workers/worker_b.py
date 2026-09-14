import asyncio
import json
from datetime import datetime

from core.database import async_session
from core.logging import get_logger
from core.models import RTDS
from core.redis import redis_client
from core.worker_status import update_worker_status


CHANNEL_NAME = "Mock-WS"

STATUS_UPDATE_INTERVAL = 10

logger = get_logger("WorkerB")


def validate_market_data(data: dict) -> None:
    required_fields = {
        "instrument_id",
        "price",
        "timestamp",
    }

    missing_fields = required_fields - data.keys()

    if missing_fields:
        raise ValueError(
            f"Missing fields: {', '.join(missing_fields)}"
        )

    if not isinstance(data["instrument_id"], str):
        raise ValueError("instrument_id must be a string")

    if not isinstance(data["price"], (int, float)):
        raise ValueError("price must be a number")

    datetime.fromisoformat(data["timestamp"])


async def save_to_database(data: dict):
    async with async_session() as session:
        async with session.begin():
            record = RTDS(
                instrument_id=data["instrument_id"],
                price=data["price"],
                timestamp=datetime.fromisoformat(
                    data["timestamp"]
                ),
            )

            session.add(record)


async def status_loop():
    while True:
        await update_worker_status("WorkerB")
        await asyncio.sleep(STATUS_UPDATE_INTERVAL)


async def main():
    pubsub = redis_client.pubsub()

    await pubsub.subscribe(CHANNEL_NAME)

    status_task = asyncio.create_task(status_loop())

    logger.info(
        f"WorkerB listening on: {CHANNEL_NAME}"
    )

    try:
        async for message in pubsub.listen():
            if message["type"] != "message":
                continue

            try:
                data = json.loads(message["data"])

                validate_market_data(data)

                await save_to_database(data)

                logger.info(
                    f"Saved: {data['instrument_id']} "
                    f"{data['price']} "
                    f"{data['timestamp']}"
                )

            except json.JSONDecodeError:
                logger.error("Invalid JSON message")

            except ValueError as error:
                logger.error(
                    f"Invalid market data: {error}"
                )

            except Exception as error:
                logger.exception(
                    f"Failed to process message: {error}"
                )

    finally:
        status_task.cancel()

        await pubsub.unsubscribe(CHANNEL_NAME)
        await pubsub.aclose()
        await redis_client.aclose()

        logger.info("WorkerB stopped")


if __name__ == "__main__":
    asyncio.run(main())
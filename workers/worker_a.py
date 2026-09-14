import asyncio
import json

import redis.asyncio as redis
import websockets

from core.config import (
    REDIS_HOST,
    REDIS_PASSWORD,
    REDIS_PORT,
)
from core.logging import get_logger
from core.worker_status import update_worker_status
from market_data import parse_message


REDIS_CHANNEL = "Mock-WS"

WEBSOCKET_URL = "ws://mock-websocket:8765"

RECONNECT_DELAY = 3

STATUS_UPDATE_INTERVAL = 10

logger = get_logger("WorkerA")


def create_redis_client():
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        decode_responses=True,
    )


async def status_loop():
    while True:
        await update_worker_status("WorkerA")
        await asyncio.sleep(STATUS_UPDATE_INTERVAL)


async def main():
    redis_client = create_redis_client()

    status_task = asyncio.create_task(status_loop())

    logger.info("WorkerA started")

    try:
        while True:
            try:
                logger.info(
                    f"Connecting to WebSocket: {WEBSOCKET_URL}"
                )

                async with websockets.connect(
                    WEBSOCKET_URL
                ) as websocket:

                    logger.info("Connected to WebSocket")

                    async for raw_message in websocket:
                        try:
                            raw_data = json.loads(raw_message)

                            market_data = parse_message(
                                raw_data
                            )

                            message = json.dumps(
                                market_data,
                                separators=(",", ":"),
                            )

                            while True:
                                try:
                                    await redis_client.publish(
                                        REDIS_CHANNEL,
                                        message,
                                    )
                                    break

                                except Exception as exc:
                                    logger.error(
                                        f"Redis error: {exc}"
                                    )

                                    await redis_client.aclose()

                                    logger.info(
                                        f"Reconnecting to Redis "
                                        f"in {RECONNECT_DELAY} "
                                        f"seconds..."
                                    )

                                    await asyncio.sleep(
                                        RECONNECT_DELAY
                                    )

                                    redis_client = (
                                        create_redis_client()
                                    )

                            logger.info(
                                f"Published: {message}"
                            )

                        except Exception as exc:
                            logger.error(
                                f"Error processing message: {exc}"
                            )

            except (
                websockets.exceptions.ConnectionClosed,
                ConnectionRefusedError,
                OSError,
            ) as exc:
                logger.warning(
                    f"WebSocket connection lost: {exc}"
                )

                logger.info(
                    f"Reconnecting in "
                    f"{RECONNECT_DELAY} seconds..."
                )

                await asyncio.sleep(RECONNECT_DELAY)

    finally:
        status_task.cancel()

        await redis_client.aclose()

        logger.info("WorkerA stopped")


if __name__ == "__main__":
    asyncio.run(main())
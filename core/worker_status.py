import json
from datetime import datetime, timezone

from core.redis import redis_client


STATUS_KEY = "Mock-WS:worker_status"


async def update_worker_status(worker_name: str) -> None:
    status = {
        "status": "running",
        "last_seen": datetime.now(timezone.utc).isoformat(),
    }

    await redis_client.hset(
        STATUS_KEY,
        worker_name,
        json.dumps(status),
    )


async def get_worker_status() -> dict:
    data = await redis_client.hgetall(STATUS_KEY)

    return {
        worker_name: json.loads(status)
        for worker_name, status in data.items()
    }
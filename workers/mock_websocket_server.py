import asyncio
import json
import random
from datetime import datetime, timezone

import websockets


ASSETS = [
    "AAPL",
    "MSFT",
    "GOOGL",
    "AMZN",
    "META",
    "NVDA",
    "TSLA",
    "SPY",
    "QQQ",
    "IWM",
]


async def market_data_stream(websocket):
    prices = {
        asset: random.uniform(50, 500)
        for asset in ASSETS
    }

    while True:
        asset = random.choice(ASSETS)

        prices[asset] += random.uniform(-1.0, 1.0)

        last_price = round(prices[asset], 2)

        message = {
            "instrument_id": asset,
            "LastTradedPrice": last_price,
            "ClosingPrice": round(
                last_price - random.uniform(-2, 2),
                2,
            ),
            "LowPrice": round(
                last_price - random.uniform(0, 3),
                2,
            ),
            "HighPrice": round(
                last_price + random.uniform(0, 3),
                2,
            ),
            "TradedQuantity": random.randint(1, 1000),
            "TotalNumberOfTrades": random.randint(1, 500),
            "TotalNumberOfSharesTraded": random.randint(
                100,
                100000,
            ),
            "TotalTradeValue": round(
                last_price * random.randint(100, 100000),
                2,
            ),
            "TradeDate": datetime.now(
                timezone.utc
            ).isoformat(),
        }

        await websocket.send(
            json.dumps(message)
        )

        await asyncio.sleep(1)


async def main():
    async with websockets.serve(
        market_data_stream,
        "0.0.0.0",
        8765,
    ):
        print(
            "Mock WebSocket server listening on "
            "ws://0.0.0.0:8765"
        )

        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
import asyncio
import random
from datetime import datetime, timezone


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


async def mock_stream():
    """
    Mock Lightstreamer-like market-data stream.
    """

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
            "ClosingPrice": round(last_price - random.uniform(-2, 2), 2),
            "LowPrice": round(last_price - random.uniform(0, 3), 2),
            "HighPrice": round(last_price + random.uniform(0, 3), 2),
            "TradedQuantity": random.randint(1, 1000),
            "TotalNumberOfTrades": random.randint(1, 500),
            "TotalNumberOfSharesTraded": random.randint(100, 100000),
            "TotalTradeValue": round(
                last_price * random.randint(100, 100000),
                2,
            ),
            "TradeDate": datetime.now(timezone.utc).isoformat(),
        }

        yield message

        await asyncio.sleep(1)


def parse_message(raw_message: dict) -> dict:
    """
    Convert a Lightstreamer-like market-data message
    into the application's standard format.
    """

    return {
        "instrument_id": raw_message["instrument_id"],
        "price": float(raw_message["LastTradedPrice"]),
        "timestamp": raw_message["TradeDate"],
    }
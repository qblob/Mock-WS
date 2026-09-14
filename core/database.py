from urllib.parse import quote_plus

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import (
    MYSQL_DATABASE,
    MYSQL_HOST,
    MYSQL_PASSWORD,
    MYSQL_PORT,
    MYSQL_USER,
)


user = quote_plus(MYSQL_USER)
password = quote_plus(MYSQL_PASSWORD)

DATABASE_URL = (
    f"mysql+asyncmy://"
    f"{user}:{password}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}"
    f"/{MYSQL_DATABASE}"
)


engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)


async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
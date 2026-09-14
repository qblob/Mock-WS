from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class RTDS(Base):
    __tablename__ = "RTDS"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    instrument_id: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )
    price: Mapped[float] = mapped_column(Float)
    timestamp: Mapped[datetime] = mapped_column(DateTime)


class User(Base):
    __tablename__ = "auth_user"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    username: Mapped[str] = mapped_column(String(150))
    first_name: Mapped[str] = mapped_column(String(150))
    last_name: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(254))


class Profile(Base):
    __tablename__ = "users_profile"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        index=True,
    )
    photo: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
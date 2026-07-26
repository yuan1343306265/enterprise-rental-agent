from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Property(Base):
    __tablename__ = "properties"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    title: Mapped[str] = mapped_column(String(100))
    district: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(String(200))
    monthly_rent: Mapped[int] = mapped_column(Integer)
    area: Mapped[float] = mapped_column(Float)
    bedroom_count: Mapped[int] = mapped_column(Integer)
    commute_minutes: Mapped[int] = mapped_column(Integer)
    allows_pet: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    pet_deposit: Mapped[int] = mapped_column(Integer, default=0)
    floor: Mapped[str] = mapped_column(String(30))
    deposit_months: Mapped[int] = mapped_column(Integer, default=1)
    description: Mapped[str] = mapped_column(
        String(500),
        default="",
    )


class ConversationMessage(Base):
    __tablename__ = "conversation_messages"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    session_id: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )
    role: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )
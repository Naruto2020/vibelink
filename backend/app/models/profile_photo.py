import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ProfilePhoto(Base):
    __tablename__ = "profile_photos"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("profiles.id"),
        nullable=False
    )

    storage_key: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    profile: Mapped["Profile"] = relationship(
        back_populates="photos"
    )

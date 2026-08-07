import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class MatchBlock(Base):
    __tablename__ = "match_blocks"

    __table_args__ = (
        UniqueConstraint(
            "match_id",
            name="uq_match_block"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    match_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("matches.id"),
        nullable=False
    )

    blocked_by_user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


    match: Mapped["Match"] = relationship(
        back_populates="blocks"
    )

    blocked_by_user: Mapped["User"] = relationship(
        back_populates="match_blocks"
    )

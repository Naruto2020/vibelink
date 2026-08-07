import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.enums.match_status import MatchStatus


class Match(Base):
    __tablename__ = "matches"

    __table_args__ = (
        UniqueConstraint(
            "user_one_id",
            "user_two_id",
            name="uq_match_users"
        ),
        CheckConstraint(
            "user_one_id <> user_two_id",
            name="ck_match_users_different"
        ),
    )


    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )


    user_one_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )


    user_two_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )


    status: Mapped[MatchStatus] = mapped_column(
        Enum(MatchStatus),
        nullable=False,
        default=MatchStatus.ACTIVE
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


    user_one: Mapped["User"] = relationship(
        foreign_keys=[user_one_id],
        back_populates="matches_as_user_one"
    )


    user_two: Mapped["User"] = relationship(
        foreign_keys=[user_two_id],
        back_populates="matches_as_user_two"
    )

    conversation: Mapped["Conversation"] = relationship(
        back_populates="match",
        uselist=False
    )

import uuid
from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.venue_session_participant import VenueSessionParticipant


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="USER"
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
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

    profile: Mapped["Profile"] = relationship(
        back_populates="user",
        uselist=False
    )

    match_preferences: Mapped["MatchPreference"] = relationship(
        back_populates="user",
        uselist=False
    )

    venue_session_participations: Mapped[list["VenueSessionParticipant"]] = relationship(
        back_populates="user"
    )

    sent_likes: Mapped[list["Like"]] = relationship(
        foreign_keys="Like.sender_id",
        back_populates="sender"
    )

    received_likes: Mapped[list["Like"]] = relationship(
        foreign_keys="Like.receiver_id",
        back_populates="receiver"
    )

    matches_as_user_one: Mapped[list["Match"]] = relationship(
        foreign_keys="Match.user_one_id",
        back_populates="user_one"
    )


    matches_as_user_two: Mapped[list["Match"]] = relationship(
        foreign_keys="Match.user_two_id",
        back_populates="user_two"
    )

    match_blocks: Mapped[list["MatchBlock"]] = relationship(
        back_populates="blocked_by_user"
    )

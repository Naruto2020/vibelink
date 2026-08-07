import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class MatchMeeting(Base):
    __tablename__ = "match_meetings"

    __table_args__ = (
        UniqueConstraint(
            "match_id",
            "venue_session_id",
            name="uq_match_meeting_session"
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

    venue_session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("venue_sessions.id"),
        nullable=False
    )

    user_one_confirmed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    user_two_confirmed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    confirmed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )


    match: Mapped["Match"] = relationship(
        back_populates="meeting_confirmations"
    )

    venue_session: Mapped["VenueSession"] = relationship(
        back_populates="meeting_confirmations"
    )

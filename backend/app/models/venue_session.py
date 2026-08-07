import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.enums.venue_session_status import VenueSessionStatus

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.venue_session_participant import VenueSessionParticipant


class VenueSession(Base):
    __tablename__ = "venue_sessions"

    __table_args__ = (
        UniqueConstraint(
            "venue_id",
            "session_date",
            name="uq_venue_session_date"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    venue_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("venues.id"),
        nullable=False
    )

    session_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    start_datetime: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    end_datetime: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    status: Mapped[VenueSessionStatus] = mapped_column(
        Enum(VenueSessionStatus),
        nullable=False,
        default=VenueSessionStatus.PLANNED
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


    venue: Mapped["Venue"] = relationship(
        back_populates="sessions"
    )

    participants: Mapped[list["VenueSessionParticipant"]] = relationship(
        back_populates="venue_session"
    )

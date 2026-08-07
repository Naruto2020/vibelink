import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.enums.venue_participant_status import VenueParticipantStatus

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.venue_session import VenueSession


class VenueSessionParticipant(Base):
    __tablename__ = "venue_session_participants"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "venue_session_id",
            name="uq_user_venue_session"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    venue_session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("venue_sessions.id"),
        nullable=False
    )

    registered_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    checked_in_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    status: Mapped[VenueParticipantStatus] = mapped_column(
        Enum(VenueParticipantStatus),
        nullable=False,
        default=VenueParticipantStatus.REGISTERED
    )

    user: Mapped["User"] = relationship(
        back_populates="venue_session_participations"
    )

    venue_session: Mapped["VenueSession"] = relationship(
        back_populates="participants"
    )

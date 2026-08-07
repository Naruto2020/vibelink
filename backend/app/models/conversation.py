import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.enums.conversation_status import ConversationStatus


class Conversation(Base):
    __tablename__ = "conversations"

    __table_args__ = (
        UniqueConstraint(
            "match_id",
            name="uq_conversation_match"
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

    status: Mapped[ConversationStatus] = mapped_column(
        Enum(ConversationStatus),
        nullable=False,
        default=ConversationStatus.LOCKED
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

    match: Mapped["Match"] = relationship(
        back_populates="conversation"
    )

    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation"
    )

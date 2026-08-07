import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Like(Base):
    __tablename__ = "likes"

    __table_args__ = (
        UniqueConstraint(
            "sender_id",
            "receiver_id",
            name="uq_sender_receiver_like"
        ),
        CheckConstraint(
            "sender_id <> receiver_id",
            name="ck_like_sender_receiver_different"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    sender_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    receiver_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


    sender: Mapped["User"] = relationship(
        foreign_keys=[sender_id],
        back_populates="sent_likes"
    )

    receiver: Mapped["User"] = relationship(
        foreign_keys=[receiver_id],
        back_populates="received_likes"
    )

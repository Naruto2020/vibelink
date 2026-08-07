from enum import Enum


class ConversationStatus(str, Enum):
    LOCKED = "LOCKED"
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"

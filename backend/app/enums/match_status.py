from enum import Enum


class MatchStatus(str, Enum):
    ACTIVE = "ACTIVE"
    UNMATCHED = "UNMATCHED"
    BLOCKED = "BLOCKED"

from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

JST = ZoneInfo("Asia/Tokyo")

class SimpleLevel(int, Enum):
    NORMAL = 0
    MODERATE = 1
    HIGH = 2
    SPECIAL = 3

@dataclass
class VenPayload:
    """
    Simplified OpenADR 2.0 VEN (Virtual End Node) payload.
    Based on the oadrDistributeEvent structure.
    """
    request_id: str
    event_id: str
    signal_level: SimpleLevel
    duration_seconds: int
    start_at: datetime
    issued_at: datetime
    reason: str

    def is_active(self) -> bool:
        now = datetime.now(JST)
        start = self.start_at.replace(tzinfo=JST)
        elapsed = (now - start).total_seconds()
        return elapsed <= self.duration_seconds

    def expires_at(self) -> datetime:
        start = self.start_at.replace(tzinfo=JST)
        return start + timedelta(seconds=self.duration_seconds)
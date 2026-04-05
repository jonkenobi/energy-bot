from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class SignalLevel(str, Enum):
    NORMAL = "NORMAL"        # no override, bot runs freely
    MODERATE = "MODERATE"    # reduce discharge
    HIGH = "HIGH"            # stop discharging entirely
    SPECIAL = "SPECIAL"      # charge as much as possible

@dataclass
class AdrSignal:
    signal_level: SignalLevel
    duration_seconds: int
    issued_at: datetime
    reason: str
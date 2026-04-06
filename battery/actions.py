from enum import Enum

class BatteryAction(Enum):
    CHARGE = 1
    HOLD = 0
    DISCHARGE = -1
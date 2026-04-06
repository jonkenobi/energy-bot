from constants import BATTERY_CAPACITY_KWH, PRICE_THRESHOLD, MIN_SOC_KWH, MAX_SOC_KWH
from battery import Battery
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Decision:
    timestamp: datetime
    action: str
    price: float
    battery_level: float
    profit: float

class ArbitrageEngine:
    def __init__(self):
        self.battery = Battery()
        self.total_profit = 0.0

    def evaluate(self, price: float) -> Decision:
        if price < PRICE_THRESHOLD and self.battery.current_charge < MAX_SOC_KWH:
            action = 1
            label = "CHARGE"
        elif price > PRICE_THRESHOLD and self.battery.current_charge > MIN_SOC_KWH:
            action = -1
            label = "DISCHARGE"
        else:
            action = 0
            label = "WAIT"

        money = self.battery.update(action, price)
        self.total_profit += money

        return Decision(
            timestamp=datetime.now(),
            action=label,
            price=price,
            battery_level=self.battery.current_charge,
            profit=self.total_profit
        )
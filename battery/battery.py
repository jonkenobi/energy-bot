from battery.actions import BatteryAction
from battery.constants import BATTERY_CAPACITY_KWH, MAX_POWER_KW, EFFICIENCY, MIN_SOC_KWH, MAX_SOC_KWH

class Battery:
    """Represents the battery unit and executes the charge/discharge logic."""
    def __init__(self):
        self.current_charge = MIN_SOC_KWH  # Start at minimum safe level

    def update(self, action, price, discharge_rate: float = 1.0):
        """
        Action: +1 (Charge), -1 (Discharge), 0 (Hold). Returns: Profit/Cost ($)
        discharge_rate: multiplier on max discharge power (1.0 = full, 0.5 = half)
        """

        if action == BatteryAction.CHARGE:
            possible_charge = min(MAX_POWER_KW, MAX_SOC_KWH - self.current_charge)
            if possible_charge <= 0:
                return 0.0
            self.current_charge += possible_charge * EFFICIENCY
            cost = possible_charge * price
            return -cost

        elif action == BatteryAction.DISCHARGE:
            # Apply discharge_rate to limit how much we can discharge
            max_discharge = MAX_POWER_KW * discharge_rate
            possible_discharge = min(max_discharge, self.current_charge - MIN_SOC_KWH)
            if possible_discharge <= 0:
                return 0.0
            self.current_charge -= possible_discharge
            # Note: Efficiency is not applied here as round-trip efficiency discount was accounted for already during charging
            revenue = possible_discharge * price
            return revenue

        return 0.0  # Hold
from constants import BATTERY_CAPACITY_KWH, MAX_POWER_KW, EFFICIENCY, MIN_SOC_KWH, MAX_SOC_KWH

class Battery:
    """Represents the battery unit and executes the charge/discharge logic."""
    def __init__(self):
        self.current_charge = MIN_SOC_KWH  # Start at minimum safe level

    def update(self, action, price):
        """Action: +1 (Charge), -1 (Discharge), 0 (Hold). Returns: Profit/Cost ($)"""

        if action == 1:  # CHARGING
            # Cannot charge beyond 90% SoC
            possible_charge = min(MAX_POWER_KW, MAX_SOC_KWH - self.current_charge)
            if possible_charge <= 0:
                return 0.0  # Already at max, do nothing
            self.current_charge += possible_charge * EFFICIENCY
            cost = possible_charge * price
            return -cost

        elif action == -1:  # DISCHARGING
            # Cannot discharge below 10% SoC
            possible_discharge = min(MAX_POWER_KW, self.current_charge - MIN_SOC_KWH)
            if possible_discharge <= 0:
                return 0.0  # Already at min, do nothing
            self.current_charge -= possible_discharge
            # Note: Revenue calculation is simpler here as efficiency was applied during charging
            revenue = possible_discharge * price
            return revenue

        return 0.0  # Hold
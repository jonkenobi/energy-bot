from constants import BATTERY_CAPACITY_KWH, MAX_POWER_KW, EFFICIENCY

class Battery:
    """Represents the battery unit and executes the charge/discharge logic."""
    def __init__(self):
        self.current_charge = 0.0  # Start empty

    def update(self, action, price):
        """Action: +1 (Charge), -1 (Discharge), 0 (Hold). Returns: Profit/Cost ($)"""
        
        # 1. Determine maximum possible flow based on physical limits
        if action == 1:  # CHARGING
            # Cannot charge more than capacity - current charge
            possible_charge = min(MAX_POWER_KW, BATTERY_CAPACITY_KWH - self.current_charge)
            
            # Apply efficiency loss here (less energy makes it into the battery)
            self.current_charge += possible_charge * EFFICIENCY 
            cost = possible_charge * price
            return -cost # Money OUT (Cost)

        elif action == -1: # DISCHARGING
            # Cannot discharge more than what is currently stored
            possible_discharge = min(MAX_POWER_KW, self.current_charge)
            self.current_charge -= possible_discharge
            
            # Note: Revenue calculation is simpler here as efficiency was applied during charging
            revenue = possible_discharge * price 
            return revenue # Money IN (Revenue)
            
        return 0.0 # Hold

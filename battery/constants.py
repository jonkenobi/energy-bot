# --- CONFIGURATION ( The "Physics" ) ---
BATTERY_CAPACITY_KWH = 13.5  # Size of a standard home battery 
MAX_POWER_KW = 5.0           # Max speed we can charge/discharge (kW)
EFFICIENCY = 0.90            # We lose 10% energy in heat (90% round-trip)
PRICE_THRESHOLD = 0.15       # Simple Logic: Buy below 15c, Sell above 15c

# --- SOC BOUNDARIES ---
MIN_SOC_KWH = BATTERY_CAPACITY_KWH * 0.10   # Don't discharge below 10% (1.35 kWh)
MAX_SOC_KWH = BATTERY_CAPACITY_KWH * 0.90   # Don't charge above 90% (12.15 kWh)
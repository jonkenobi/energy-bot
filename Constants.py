# --- CONFIGURATION ( The "Physics" ) ---
BATTERY_CAPACITY_KWH = 13.5  # Size of a standard home battery (e.g., Powerwall)
MAX_POWER_KW = 5.0           # Max speed we can charge/discharge (kW)
EFFICIENCY = 0.90            # We lose 10% energy in heat (90% round-trip)
PRICE_THRESHOLD = 0.15       # Simple Logic: Buy below 15c, Sell above 15c
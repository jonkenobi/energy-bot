import asyncio
import numpy as np
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PriceEvent:
    timestamp: datetime
    price: float
    hour: float  # fractional hour of day, e.g. 14.5 = 2:30pm

async def simulate_price_feed():
    """Emits a PriceEvent every second, simulating a live price feed."""
    start = datetime.now()
    while True:
        now = datetime.now()
        elapsed_seconds = (now - start).total_seconds()

        # compress 24 hours into 24 seconds for demo purposes
        hour = (elapsed_seconds % 24)
        price = 0.20 - 0.15 * np.cos(2 * np.pi * (hour - 14) / 24)

        yield PriceEvent(timestamp=now, price=round(price, 4), hour=round(hour, 2))
        await asyncio.sleep(1)
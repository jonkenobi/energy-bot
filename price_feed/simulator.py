import asyncio
import numpy as np
import random
import logging
from dataclasses import dataclass
from datetime import datetime
from reliability.circuit_breaker import CircuitBreaker
from reliability.retry import RetryPolicy

logger = logging.getLogger("price_feed")

@dataclass
class PriceEvent:
    timestamp: datetime
    price: float
    hour: float

async def fetch_price(hour: float) -> float:
    if random.random() < 0.2:
        raise Exception("Price feed API unavailable")
    price = 0.20 - 0.15 * np.cos(2 * np.pi * (hour - 14) / 24)
    return round(price, 4)

async def simulate_price_feed():
    breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=10)
    retry = RetryPolicy(max_attempts=3, base_delay=0.5, max_delay=5.0)
    start = datetime.now()

    while True:
        now = datetime.now()
        elapsed_seconds = (now - start).total_seconds()
        hour = elapsed_seconds % 24

        try:
            # retry first, then circuit breaker wraps the whole thing
            price = await breaker.call(retry.call, fetch_price, hour)
            yield PriceEvent(timestamp=now, price=price, hour=round(hour, 2))
        except Exception as e:
            logger.warning(f"Skipping tick — {e}")

        await asyncio.sleep(1)


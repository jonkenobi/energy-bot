import asyncio
import random
from datetime import datetime

class RetryPolicy:
    def __init__(
        self,
        max_attempts: int = 3,
        base_delay: float = 1.0,      # seconds
        max_delay: float = 10.0,      # cap on backoff
        jitter: bool = True           # randomize delay slightly
    ):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.jitter = jitter

    async def call(self, func, *args, **kwargs):
        attempt = 0

        while attempt < self.max_attempts:
            try:
                result = await func(*args, **kwargs)
                if attempt > 0:
                    print(f"[Retry] Price fetch succeeded on attempt {attempt + 1}")
                return result
            except Exception as e:
                attempt += 1
                if attempt >= self.max_attempts:
                    print(f"[Retry] All {self.max_attempts} price fetch attempts failed — giving up")
                    raise e

                delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                if self.jitter:
                    delay = delay * (0.5 + random.random() * 0.5)

                print(f"[Retry] Price fetch failed on attempt {attempt} — retrying in {delay:.1f}s")
                await asyncio.sleep(delay)
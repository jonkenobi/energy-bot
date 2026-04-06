import asyncio
import logging
from enum import Enum
from datetime import datetime, timedelta

logger = logging.getLogger("reliability.circuit_breaker")

class CircuitState(Enum):
    CLOSED = "CLOSED"       # normal, requests go through
    OPEN = "OPEN"           # failing, requests blocked
    HALF_OPEN = "HALF_OPEN" # testing if service recovered

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 3,       # failures before opening
        recovery_timeout: int = 10,        # seconds before trying again
        success_threshold: int = 2         # successes in HALF_OPEN to close again
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: datetime | None = None

    def _should_attempt_reset(self) -> bool:
        if self.last_failure_time is None:
            return False
        elapsed = datetime.now() - self.last_failure_time
        return elapsed >= timedelta(seconds=self.recovery_timeout)

    def _on_success(self):
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                logger.warning("Circuit CLOSED — service recovered")
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                self.success_count = 0
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        if self.failure_count >= self.failure_threshold:
            logger.warning("Circuit OPEN — too many failures, blocking requests")
            self.state = CircuitState.OPEN
            self.success_count = 0

    async def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                logger.warning("Circuit HALF_OPEN — testing recovery")
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit is OPEN — request blocked")

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
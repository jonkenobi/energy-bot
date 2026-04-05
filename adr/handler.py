from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from adr.models import VenPayload, SimpleLevel, JST
import asyncio
import uuid

app = FastAPI()

current_signal: VenPayload | None = None
signal_lock = asyncio.Lock()

class SignalRequest(BaseModel):
    event_id: str
    signal_level: SimpleLevel
    duration_seconds: int
    start_at: datetime | None = None
    reason: str

@app.post("/adr/signal")
async def receive_signal(request: SignalRequest):
    global current_signal
    now = datetime.now(JST)
    async with signal_lock:
        current_signal = VenPayload(
            request_id=str(uuid.uuid4()),
            event_id=request.event_id,
            signal_level=request.signal_level,
            duration_seconds=request.duration_seconds,
            start_at=now, #Setting it as now for convenience of testing, but use request.start_at or now for real implementation
            issued_at=now,
            reason=request.reason
        )
        print(f"[ADR] Event received: {request.event_id} level={request.signal_level} duration={request.duration_seconds}s expires={current_signal.expires_at().strftime('%H:%M:%S %Z')}")
    return {
        "status": "accepted",
        "request_id": current_signal.request_id,
        "event_id": current_signal.event_id,
        "signal_level": current_signal.signal_level,
        "expires_at": current_signal.expires_at()
    }

@app.get("/adr/status")
async def get_status():
    if current_signal is None:
        return {"signal_level": 0, "active": False}
    return {
        "event_id": current_signal.event_id,
        "signal_level": current_signal.signal_level,
        "active": current_signal.is_active(),
        "expires_at": current_signal.expires_at(),
        "reason": current_signal.reason
    }

def get_current_signal() -> VenPayload | None:
    if current_signal is None:
        return None
    if not current_signal.is_active():
        return None
    return current_signal
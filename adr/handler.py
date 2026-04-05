from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from adr.models import AdrSignal, SignalLevel
import asyncio

app = FastAPI()

# This is the shared signal — the bot reads from this
current_signal: AdrSignal | None = None
signal_lock = asyncio.Lock()

class SignalRequest(BaseModel):
    signal_level: SignalLevel
    duration_seconds: int
    reason: str

@app.post("/adr/signal")
async def receive_signal(request: SignalRequest):
    global current_signal
    async with signal_lock:
        current_signal = AdrSignal(
            signal_level=request.signal_level,
            duration_seconds=request.duration_seconds,
            issued_at=datetime.now(),
            reason=request.reason
        )
    print(f"[ADR] Signal received: {request.signal_level} for {request.duration_seconds}s — {request.reason}")
    return {"status": "accepted", "signal": request.signal_level}

@app.get("/adr/status")
async def get_status():
    if current_signal is None:
        return {"signal": "NORMAL", "active": False}
    return {
        "signal": current_signal.signal_level,
        "duration_seconds": current_signal.duration_seconds,
        "issued_at": current_signal.issued_at,
        "reason": current_signal.reason,
        "active": True
    }

def get_current_signal() -> AdrSignal | None:
    return current_signal
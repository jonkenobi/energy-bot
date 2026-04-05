# Energy Arbitrage Bot

A real-time energy arbitrage bot that simulates a home battery system, making live charge/discharge decisions based on electricity prices and responding to demand-response signals (ADR).

## How It Works

- **Real-time price feed** — simulates a live electricity price stream, ticking every second
- **Arbitrage engine** — decides whether to charge, discharge, or wait based on price thresholds
- **OpenADR signal handler** — HTTP endpoint that accepts demand-response signals from a grid operator, overriding the bot's normal logic
- **Circuit breaker** — detects price feed failures and blocks requests until the service recovers, preventing cascading failures
- **Retry policy** — retries transient failures with exponential backoff and jitter before escalating to the circuit breaker

## Project Structure
```
energy-bot/
├── main.py                  # entry point, runs bot and HTTP server concurrently
├── battery.py               # battery model (SoC, charge/discharge logic)
├── constants.py             # battery and pricing parameters
│
├── price_feed/
│   └── simulator.py         # async price feed with simulated failures
│
├── arbitrage/
│   └── engine.py            # threshold-based decision engine
│
├── adr/
│   ├── models.py            # OpenADR signal data classes
│   └── handler.py           # FastAPI HTTP endpoint
│
└── reliability/
    ├── circuit_breaker.py   # CLOSED/OPEN/HALF_OPEN state machine
    └── retry.py             # exponential backoff with jitter
```


## Running the Project

1. Install Python dependencies:
    ```
    pip install -r requirements.txt
    ```
2. Run the simulation:
    ```
    python main.py
    ```

The bot starts ticking immediately. The HTTP server runs concurrently on port 8000.

## Sending ADR Signals

Visit `http://localhost:8000/docs` for the interactive API UI, or send a signal manually:

**Windows PowerShell:**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/adr/signal" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"signal_level": "HIGH", "duration_seconds": 30, "reason": "Grid stress event"}'
```

**Mac/Linux:**
```bash
curl -X POST http://localhost:8000/adr/signal \
  -H "Content-Type: application/json" \
  -d '{"signal_level": "HIGH", "duration_seconds": 30, "reason": "Grid stress event"}'
```

Available signal levels: `NORMAL`, `MODERATE`, `HIGH`, `SPECIAL`

## Reliability Patterns

The price feed is wrapped in two layers of protection:

- **Retry** — on a failed request, retries up to 3 times with exponential backoff before reporting a failure
- **Circuit breaker** — after 3 consecutive failures, opens the circuit and blocks requests for 10 seconds before probing for recovery

This mirrors real-world energy system design where communication failures are expected and must be handled gracefully.
## Running unit tests
1. In the root directory, run this:
    ```
    python -m pytest
    ```

## Motivation

Energy arbitrage helps home and grid-scale batteries increase value by buying energy when cheap and selling when expensive. 
This project demonstrates the core logic simply and transparently. 

I am building this energy arbitrage bot to get a feel for what arbitrage bots do and how the work, while learning the key concepts in the energy industry. 


## Disclaimer
Select portions of this code were generated or assisted by AI
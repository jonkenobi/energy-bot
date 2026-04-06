# Energy Arbitrage Bot

A real-time energy arbitrage bot that simulates a home battery system, making live charge/discharge decisions based on electricity prices and responding to demand-response signals (ADR).

## How It Works

- **Real-time price feed** — simulates a live electricity price stream, ticking every second
- **Arbitrage engine** — decides whether to charge, discharge, or wait based on a fixed price threshold
- **Battery simulator** — models a real home battery with SoC boundaries (10%-90%), charge rate limits, and efficiency loss
- **OpenADR 2.0 signal handler** — HTTP endpoint that accepts demand-response signals from a grid operator, overriding or modifying the bot's normal logic. Signals expire automatically after their duration
- **Circuit breaker** — detects price feed failures and blocks requests until the service recovers, preventing cascading failures
- **Retry policy** — retries transient failures with exponential backoff and jitter before escalating to the circuit breaker

## Project Structure
```
energy-bot/
├── main.py                  # entry point, runs bot and HTTP server concurrently
├── adr/
│   ├── models.py            # OpenADR 2.0 VEN payload data classes
│   └── handler.py           # FastAPI HTTP endpoint
│
├── arbitrage/
│   └── engine.py            # threshold-based decision engine
│
├── battery/
│   ├── actions.py           # BatteryAction enum (CHARGE, DISCHARGE, HOLD)
│   ├── battery.py           # battery model (SoC, charge/discharge logic)
│   └── constants.py         # battery and pricing parameters
│
├── config/
│   └── log_config.py        # logging setup
│
├── logs/
│   └── system_events.log    # infrastructure logs (circuit breaker, retry, ADR events)
│
├── price_feed/
│   └── simulator.py         # async price feed with simulated failures
│
├── reliability/
│   ├── circuit_breaker.py   # CLOSED/OPEN/HALF_OPEN state machine
│   └── retry.py             # exponential backoff with jitter
│
└── tests/
    └── test_battery.py      # pytest test suite
```

## Running the Bot

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the bot:
```bash
python main.py
```

The bot starts ticking immediately. The HTTP server runs concurrently on port 8000.

### Sample output
```
Time            Price       Action    Battery       Profit        ADR
----------------------------------------------------------------------
23:08:57     $0.3176         WAIT      1.35kWh $   0.0000   NORMAL(0)
23:08:58     $0.2895         WAIT      1.35kWh $   0.0000   NORMAL(0)
23:08:59     $0.1220       CHARGE      5.85kWh $  -0.6100   NORMAL(0)
23:09:00     $0.0703       CHARGE     10.35kWh $  -0.9615   NORMAL(0)
23:09:01     $0.0547       CHARGE     12.15kWh $  -1.2077   NORMAL(0)
23:09:02     $0.1640    DISCHARGE      7.15kWh $  -0.4130   NORMAL(0)
23:09:03     $0.2035    DISCHARGE      2.15kWh $   0.6045   NORMAL(0)
23:09:04     $0.2807         WAIT      1.35kWh $   0.6045   NORMAL(0)
23:09:05     $0.1220    WAIT (ADR)     1.35kWh $   0.6045    HIGH(2)
23:09:06     $0.0703    WAIT (ADR)     1.35kWh $   0.6045    HIGH(2)
```

## ADR Signal Levels

Signals follow the OpenADR 2.0 SIMPLE signal standard with integer levels 0-3:

| Level | Name | Effect |
|-------|------|--------|
| 0 | NORMAL | No override, bot runs freely |
| 1 | MODERATE | Discharge rate reduced to 50% |
| 2 | HIGH | Charging and discharging blocked (hold) |
| 3 | SPECIAL | Force charge regardless of price |

Signals expire automatically after `duration_seconds` and the bot returns to normal operation.

## Sending ADR Signals

Visit `http://localhost:8000/docs` for the interactive API UI, or send a signal manually:

**Windows PowerShell:**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/adr/signal" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"event_id": "EVT-001", "signal_level": 2, "duration_seconds": 30, "reason": "Grid stress event"}'
```

**Mac/Linux:**
```bash
curl -X POST http://localhost:8000/adr/signal \
  -H "Content-Type: application/json" \
  -d '{"event_id": "EVT-001", "signal_level": 2, "duration_seconds": 30, "reason": "Grid stress event"}'
```

## Reliability Patterns

The price feed is wrapped in two layers of protection:

- **Retry** — on a failed request, retries up to 3 times with exponential backoff and jitter before reporting a failure
- **Circuit breaker** — after 3 consecutive failures, opens the circuit and blocks requests for 10 seconds before probing for recovery

Infrastructure logs (retry attempts, circuit breaker state changes, ADR events) are written to `logs/system_events.log` to keep the console output clean.

This mirrors real-world energy system design where communication failures over consumer-grade networks are expected and must be handled gracefully.

## Running Tests
```bash
python -m pytest tests/ -v
```

## Motivation

Energy arbitrage helps home and grid-scale batteries increase value by buying energy when cheap and selling when expensive. I built this project to understand how arbitrage bots work in practice while learning key concepts in the energy industry — real-time data ingestion, demand-response protocols, battery domain modelling, and backend reliability patterns.

## Disclaimer
Select portions of this code were generated or assisted by AI
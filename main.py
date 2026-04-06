import asyncio
import logging
import uvicorn
from price_feed.simulator import simulate_price_feed
from arbitrage.engine import ArbitrageEngine
from adr.handler import app, get_current_adr_signal
from adr.models import SimpleLevel, VenPayload
from datetime import datetime
from config.log_config import setup_logging

setup_logging() 

async def run_bot():
    engine = ArbitrageEngine()

    print(f"{'Time':<12} {'Price':>8} {'Action':>12} {'Battery':>10} {'Profit':>10} {'ADR':>10}")
    print("-" * 70)

    async for price_event in simulate_price_feed():
        signal = get_current_adr_signal()

        is_adr_override, discharge_rate = handle_adr(signal, engine, price_event)
        if is_adr_override: 
            continue # skip normal arbitrage if ADR took an action

        decision = engine.evaluate(price_event.price, discharge_rate=discharge_rate)
        
        signal_label = get_signal_label(signal)
        time_str = decision.timestamp.strftime("%H:%M:%S")
        print_decision(time_str, decision.price, decision.action, decision.battery_level, decision.profit, signal_label)

def handle_adr(signal: VenPayload | None, engine: ArbitrageEngine, event) -> tuple[bool, float]:
    """
    Returns (overridden, discharge_rate).
    If overridden is True, the main loop should skip normal arbitrage.
    """
    if signal is None:
        return False, 1.0

    time_str = datetime.now().strftime("%H:%M:%S")

    if signal.signal_level == SimpleLevel.HIGH:
        engine.battery.update(0, event.price)
        print_decision(time_str, event.price, "WAIT (ADR)", engine.battery.current_charge, engine.total_profit, get_signal_label(signal))
        return True, 1.0

    if signal.signal_level == SimpleLevel.SPECIAL:
        engine.battery.update(1, event.price)
        print_decision(time_str, event.price, "CHARGE (ADR)", engine.battery.current_charge, engine.total_profit, get_signal_label(signal))
        return True, 1.0

    if signal.signal_level == SimpleLevel.MODERATE:
        return False, 0.5  # let arbitrage run, but at half discharge rate

    return False, 1.0  # NORMAL — full rate

def get_signal_label(signal: VenPayload | None) -> str:
    if signal is None:
        return "NORMAL(0)"
    labels = {
        SimpleLevel.NORMAL:   "NORMAL(0)",
        SimpleLevel.MODERATE: "MODERATE(1)",
        SimpleLevel.HIGH:     "HIGH(2)",
        SimpleLevel.SPECIAL:  "SPECIAL(3)",
    }
    return labels.get(signal.signal_level, "NORMAL(0)")

def print_decision(time_str, price, action, battery_level, profit, signal_label):
    print(f"{time_str:<12} ${price:>7.4f} {action:>12} {battery_level:>9.2f}kWh ${profit:>8.4f} {signal_label:>10}")

async def run_adr_handler_server():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="warning")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    await asyncio.gather(
        run_bot(),
        run_adr_handler_server()
    )

if __name__ == "__main__":
    asyncio.run(main())
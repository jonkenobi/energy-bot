import asyncio
import uvicorn
from price_feed.simulator import simulate_price_feed
from arbitrage.engine import ArbitrageEngine
from adr.handler import app, get_current_signal
from adr.models import SimpleLevel
from datetime import datetime

async def run_bot():
    engine = ArbitrageEngine()

    print(f"{'Time':<12} {'Price':>8} {'Action':>12} {'Battery':>10} {'Profit':>10} {'ADR':>10}")
    print("-" * 70)

    async for event in simulate_price_feed():
        signal = get_current_signal()

        # ADR logic
        if signal and signal.signal_level == SimpleLevel.HIGH:
            engine.battery.update(0, event.price)
            time_str = datetime.now().strftime("%H:%M:%S")
            print(f"{time_str:<12} ${event.price:>7.4f} {'WAIT (ADR)':>12} {engine.battery.current_charge:>9.2f}kWh ${engine.total_profit:>8.4f} {'HIGH(2)':>10}")
            continue
        elif signal and signal.signal_level == SimpleLevel.SPECIAL:
            engine.battery.update(1, event.price)
            time_str = datetime.now().strftime("%H:%M:%S")
            print(f"{time_str:<12} ${event.price:>7.4f} {'CHARGE (ADR)':>12} {engine.battery.current_charge:>9.2f}kWh ${engine.total_profit:>8.4f} {'SPECIAL(3)':>10}")
            continue

        # Normal arbitrage logic
        decision = engine.evaluate(event.price)
        signal_label = f"MODERATE(1)" if signal and signal.signal_level == SimpleLevel.MODERATE else "NORMAL(0)"
        time_str = decision.timestamp.strftime("%H:%M:%S")
        print(f"{time_str:<12} ${decision.price:>7.4f} {decision.action:>12} {decision.battery_level:>9.2f}kWh ${decision.profit:>8.4f} {signal_label:>10}")

async def run_server():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="warning")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    await asyncio.gather(
        run_bot(),
        run_server()
    )

if __name__ == "__main__":
    asyncio.run(main())
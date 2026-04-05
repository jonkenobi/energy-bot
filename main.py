import asyncio
from price_feed.simulator import simulate_price_feed
from arbitrage.engine import ArbitrageEngine

async def run_bot():
    engine = ArbitrageEngine()

    print(f"{'Time':<12} {'Price':>8} {'Action':>12} {'Battery':>10} {'Profit':>10}")
    print("-" * 56)

    async for event in simulate_price_feed():
        decision = engine.evaluate(event.price)
        time_str = decision.timestamp.strftime("%H:%M:%S")
        print(f"{time_str:<12} ${decision.price:>7.4f} {decision.action:>12} {decision.battery_level:>9.2f}kWh ${decision.profit:>8.4f}")

if __name__ == "__main__":
    asyncio.run(run_bot())
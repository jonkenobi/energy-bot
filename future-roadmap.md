# Energy Bot — Future Roadmap

A rough roadmap from where the project is now to something resembling a real production system.
Can look into these items if interested in developing the project further.

## Near term — make the logic smarter

- **Dynamic thresholds** — instead of a fixed 0.15 price threshold, calculate it based on a rolling average of recent prices. Buy when price is X% below the average, sell when above
- **JEPX integration** — swap the simulated price curve for real Japan Electric Power Exchange spot price data. They publish 30-minute settlement prices publicly
- **Forecast-aware decisions** — instead of reacting to the current price, look ahead. If prices are predicted to spike in 2 hours, don't discharge now

## Medium term — make it more realistic

- **Multiple batteries** — simulate a small fleet of 3-5 batteries with different capacities and SoC states, all managed by one engine. This forces you to think about state management at scale
- **Degradation model** — batteries lose capacity over time with charge cycles. Track cycle count and factor it into decisions — a degraded battery has lower arbitrage value
- **MODERATE signal financial modelling** — right now MODERATE reduces discharge rate but you could model the actual financial impact of demand response compliance vs non-compliance

## Longer term — production-grade thinking

- **Persistent storage** — replace in-memory state with a database so the bot survives restarts without losing battery state or decision history
- **Metrics and observability** — expose a `/metrics` endpoint with Prometheus-style data: total profit, cycle count, signal events, circuit breaker trips
- **Backtesting** — run the arbitrage engine against historical JEPX price data to evaluate how profitable different threshold strategies would have been
- **WebSocket feed** — replace the polling price feed with a proper WebSocket connection, which is closer to how real market data is consumed
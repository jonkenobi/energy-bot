# Simple Energy Arbitrage Bot

This project simulates a basic energy arbitrage bot that charges a home battery when electricity prices are low and sells/discharges when prices are high.

## How It Works

- **Battery Model:** Represents a home battery with realistic parameters (capacity, max power, efficiency).
- **Pricing Simulation:** Creates a mock 24-hour price curve.
- **Bot Logic:** Uses a simple threshold: charge when price is low, discharge when price is high.
- **Visualization:** Plots electricity prices and battery state-of-charge over the day, showing the arbitrage strategy in action.

## Files

- **main.py:** Runs the simulation and displays results.
- **battery.py:** Implements the battery logic.
- **constants.py:** Stores battery and model parameters.

## Running the Project

1. Install Python dependencies:
    ```
    pip install -r requirements.txt
    ```
2. Run the simulation:
    ```
    python main.py
    ```
## Example Output

- Console shows total profit from arbitrage for one simulated day.
- Matplotlib graph visualizes prices and battery charge cycle.

## Running unit tests
1. In the root directory, run this:
    ```
    python -m pytest
    ```

## Motivation

Energy arbitrage helps home and grid-scale batteries increase value by buying energy when cheap and selling when expensive. This project demonstrates the core logic simply and transparently.

## Disclaimer
Select portions of this code were generated or assisted by AI
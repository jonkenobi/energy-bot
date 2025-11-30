import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from battery import Battery
from constants import BATTERY_CAPACITY_KWH, MAX_POWER_KW, EFFICIENCY, PRICE_THRESHOLD

# --- PHASE 1: GENERATE DATA (Mock 24-hour prices) ---
hours = np.arange(24)
# Create a price curve that is low overnight and peaks in the evening
prices = 0.20 - 0.15 * np.cos(2 * np.pi * (hours - 14) / 24) 

df = pd.DataFrame({'Hour': hours, 'Price': prices})

# --- PHASE 2: RUN THE BOT ---
bot = Battery()
profits = []
battery_level = []

for _, row in df.iterrows():
    price = row['Price']
    
    # --- THE BRAIN (Simple Threshold Logic) ---
    if price < PRICE_THRESHOLD and bot.current_charge < BATTERY_CAPACITY_KWH:
        action = 1 # Buy (Charge)!
    elif price > PRICE_THRESHOLD and bot.current_charge > 0:
        action = -1 # Sell (Discharge)!
    else:
        action = 0 # Wait
        
    # Execute the action and record the financial outcome
    money = bot.update(action, price)
    profits.append(money)
    battery_level.append(bot.current_charge)

df['Battery_Level'] = battery_level
df['Hourly_Profit'] = profits
df['Cumulative_Profit'] = df['Hourly_Profit'].cumsum()

# --- PHASE 3: VISUALIZE ---
print(f"Total Profit from Arbitrage: ${df['Cumulative_Profit'].iloc[-1]:.2f}")

fig, ax1 = plt.subplots(figsize=(10, 6))


color = 'tab:blue'
ax1.set_xlabel('Hour of Day')
ax1.set_ylabel('Price ($/kWh)', color=color)
ax1.plot(df['Hour'], df['Price'], color=color, linestyle='--', label='Energy Price')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:green'
ax2.set_ylabel('Battery Level (kWh)', color=color)
ax2.step(df['Hour'], df['Battery_Level'], color=color, where='post', label='Battery Charge')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Energy Arbitrage Simulation: Simple Threshold Strategy')
plt.show()
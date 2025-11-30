from battery import Battery
from constants import BATTERY_CAPACITY_KWH, MAX_POWER_KW, EFFICIENCY
import pytest

# Could define some test constants or fixtures here for different tests
TEST_PRICE_THRESHOLD = 0.15

def test_battery_initialization():
    battery = Battery()
    assert battery.current_charge == 0.0

def test_battery_charge():
    battery = Battery()
    initial_charge = battery.current_charge
    price = 0.10 # A price below threshold to encourage charging
    action = 1
    cost = battery.update(action, price)

    # Expected charge should account for efficiency
    expected_charge_increase = min(MAX_POWER_KW, BATTERY_CAPACITY_KWH - initial_charge) * EFFICIENCY
    assert battery.current_charge == initial_charge + expected_charge_increase
    assert cost < 0 # Charging should result in a cost

def test_battery_discharge():
    battery = Battery()
    battery.current_charge = 5.0 # Pre-charge the battery
    initial_charge = battery.current_charge
    price = 0.20 # A price above threshold to encourage discharging
    action = -1
    revenue = battery.update(action, price)

    # Expected discharge should be MAX_POWER_KW or current_charge, whichever is smaller
    expected_discharge_decrease = min(MAX_POWER_KW, initial_charge)
    assert battery.current_charge == initial_charge - expected_discharge_decrease
    assert revenue > 0 # Discharging should result in revenue

def test_battery_hold():
    battery = Battery()
    battery.current_charge = 2.0
    initial_charge = battery.current_charge
    price = 0.15 # Price at threshold, so no action
    action = 0
    profit_cost = battery.update(action, price)

    assert battery.current_charge == initial_charge
    assert profit_cost == 0.0

# You can also add tests for edge cases, like charging a full battery or discharging an empty one
def test_battery_charge_full():
    battery = Battery()
    battery.current_charge = BATTERY_CAPACITY_KWH # Make battery full
    initial_charge = battery.current_charge
    price = 0.10
    action = 1
    cost = battery.update(action, price)

    assert battery.current_charge == initial_charge # Should not charge further
    assert cost == 0.0 # No cost if no charging occurred

def test_battery_discharge_empty():
    battery = Battery()
    battery.current_charge = 0.0 # Make battery empty
    initial_charge = battery.current_charge
    price = 0.20
    action = -1
    revenue = battery.update(action, price)

    assert battery.current_charge == initial_charge # Should not discharge further
    assert revenue == 0.0 # No revenue if no discharging occurred
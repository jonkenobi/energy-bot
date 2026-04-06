import pytest
from battery.constants import BATTERY_CAPACITY_KWH, PRICE_THRESHOLD, MIN_SOC_KWH, MAX_SOC_KWH, MAX_POWER_KW, EFFICIENCY
from battery.battery import Battery
from battery.actions import BatteryAction
from arbitrage.engine import ArbitrageEngine, Decision
from adr.models import VenPayload, SimpleLevel
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

JST = ZoneInfo("Asia/Tokyo")

# --- Battery tests ---

def test_battery_initialization():
    battery = Battery()
    assert battery.current_charge == MIN_SOC_KWH  # starts at min, not 0

def test_battery_charge():
    battery = Battery()
    initial_charge = battery.current_charge
    cost = battery.update(BatteryAction.CHARGE, 0.10)

    expected_increase = min(MAX_POWER_KW, MAX_SOC_KWH - initial_charge) * EFFICIENCY
    assert battery.current_charge == pytest.approx(initial_charge + expected_increase)
    assert cost < 0

def test_battery_discharge():
    battery = Battery()
    battery.current_charge = 5.0
    initial_charge = battery.current_charge
    revenue = battery.update(BatteryAction.DISCHARGE, 0.20)

    expected_decrease = min(MAX_POWER_KW, initial_charge - MIN_SOC_KWH)
    assert battery.current_charge == pytest.approx(initial_charge - expected_decrease)
    assert revenue > 0

def test_battery_hold():
    battery = Battery()
    battery.current_charge = 5.0
    initial_charge = battery.current_charge
    result = battery.update(0, 0.15)

    assert battery.current_charge == initial_charge
    assert result == 0.0

def test_battery_does_not_exceed_max_soc():
    battery = Battery()
    battery.current_charge = MAX_SOC_KWH  # already at ceiling
    cost = battery.update(1, 0.10)

    assert battery.current_charge == pytest.approx(MAX_SOC_KWH)
    assert cost == 0.0

def test_battery_does_not_go_below_min_soc():
    battery = Battery()
    battery.current_charge = MIN_SOC_KWH  # already at floor
    revenue = battery.update(-1, 0.20)

    assert battery.current_charge == pytest.approx(MIN_SOC_KWH)
    assert revenue == 0.0

# --- ArbitrageEngine tests ---

def test_engine_charges_when_price_low():
    engine = ArbitrageEngine()
    engine.battery.current_charge = 5.0
    decision = engine.evaluate(0.10)  # below threshold
    assert decision.action == "CHARGE"

def test_engine_discharges_when_price_high():
    engine = ArbitrageEngine()
    engine.battery.current_charge = 5.0
    decision = engine.evaluate(0.20)  # above threshold
    assert decision.action == "DISCHARGE"

def test_engine_waits_at_threshold():
    engine = ArbitrageEngine()
    engine.battery.current_charge = 5.0
    decision = engine.evaluate(0.15)  # at threshold
    assert decision.action == "HOLD"

def test_engine_waits_when_battery_full():
    engine = ArbitrageEngine()
    engine.battery.current_charge = MAX_SOC_KWH
    decision = engine.evaluate(0.10)  # low price but battery full
    assert decision.action == "HOLD"

def test_engine_waits_when_battery_empty():
    engine = ArbitrageEngine()
    engine.battery.current_charge = MIN_SOC_KWH
    decision = engine.evaluate(0.20)  # high price but battery empty
    assert decision.action == "HOLD"

def test_engine_tracks_profit():
    engine = ArbitrageEngine()
    engine.battery.current_charge = 5.0
    engine.evaluate(0.10)  # charge — costs money
    assert engine.total_profit < 0

# --- VenPayload / ADR signal tests ---

def test_signal_is_active():
    signal = VenPayload(
        request_id="req-001",
        event_id="evt-001",
        signal_level=SimpleLevel.HIGH,
        duration_seconds=60,
        start_at=datetime.now(JST),
        issued_at=datetime.now(JST),
        reason="Test"
    )
    assert signal.is_active() is True

def test_signal_expires():
    signal = VenPayload(
        request_id="req-002",
        event_id="evt-002",
        signal_level=SimpleLevel.HIGH,
        duration_seconds=1,
        start_at=datetime.now(JST) - timedelta(seconds=10),  # started 10s ago
        issued_at=datetime.now(JST) - timedelta(seconds=10),
        reason="Test"
    )
    assert signal.is_active() is False

def test_signal_levels():
    assert SimpleLevel.NORMAL == 0
    assert SimpleLevel.MODERATE == 1
    assert SimpleLevel.HIGH == 2
    assert SimpleLevel.SPECIAL == 3
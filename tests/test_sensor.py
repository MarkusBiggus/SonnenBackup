"""Tests for the sensor module."""
from unittest.mock import AsyncMock, MagicMock

from sonnen_api_v2 import BatterieError
import pytest

from custom_components.sonnenbackup.sensor import BatterieSensorEntity


@pytest.mark.asyncio
async def test_async_update_success(hass):
    """Tests a fully successful async_update."""
    UpdateCoordinator = MagicMock()
    UpdateCoordinator.getitem = AsyncMock(
        side_effect=[
            {
                "state_sonnenbackup": "Charging",
                "state_system_status": "On Grid",
                "state_consumption_avg": 555,
                "state_battery_backup_buffer": 20,
                "state_battery_state_of_charge_real": 98,
                "state_battery_state_of_charge_usable": 91,
                "state_operating_mode": "2",
                "battery_system_cycles": 111
            },
        ]
    )
    sensor = BatterieSensorEntity(UpdateCoordinator, {"path": "homeassistant/core"})
    await sensor.async_update()

    expected = {
        "state_sonnenbackup": "Charging",
        "state_system_status": "On Grid",
        "state_consumption_avg": 555,
        "state_battery_backup_buffer": 20,
        "state_battery_state_of_charge_real": 98,
        "state_battery_state_of_charge_usable": 91,
        "state_operating_mode": "2",
        "battery_system_cycles": 111
    }
    assert expected == sensor.attrs
    assert expected == sensor.extra_state_attributes
    assert sensor.available is True


@pytest.mark.asyncio
async def test_async_update_failed():
    """Tests a failed async_update."""
    UpdateCoordinator = MagicMock()
    UpdateCoordinator.getitem = AsyncMock(side_effect=BatterieError)

    sensor = BatterieSensorEntity(UpdateCoordinator, {"path": "homeassistant/core"})
    await sensor.async_update()

    assert sensor.available is False
    assert {"path": "homeassistant/core"} == sensor.attrs

"""Tests for the sensor module.
    Uses config_flow test to instantiate HASS and test sensor values.
    Relies on conftest.py to setup default mock data for tests.

    pytest tests/test_sensors.py -s -v -x  -k test_form_works
"""

import pytest
from unittest.mock import patch
import logging

import urllib3
#from freezegun.api import FakeDatetime
import tzlocal

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntryState, ConfigEntry
from homeassistant.const import (
        CONF_IP_ADDRESS,
        CONF_API_TOKEN,
        CONF_PORT,
        CONF_MODEL,
        CONF_DEVICE_ID,
        CONF_SCAN_INTERVAL,
        )
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType, InvalidData

#from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.sonnenbackup.sensor import BatterieSensorEntity
from custom_components.sonnenbackup.config_flow import CannotConnect, InvalidAuth, DeviceAPIError
from custom_components.sonnenbackup.const import DOMAIN, DEFAULT_SCAN_INTERVAL, DEFAULT_PORT
from .mock_battery_responses import (
    __battery_auth200,
)

CONFIG_DATA = {
    CONF_IP_ADDRESS: "1.1.1.1",
    CONF_PORT: DEFAULT_PORT,
    CONF_API_TOKEN: "fakeToken-111-222-4444-3333",
#    "details": {
    CONF_MODEL: 'Power unit Evo IP56',
    CONF_DEVICE_ID: "321123"
#    }
}
CONFIG_OPTIONS = {
    CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL#,
#    "sonnenbackup_debug": True,
}

_LOGGER = logging.getLogger(__name__)


@patch.object(urllib3.HTTPConnectionPool, 'urlopen', __battery_auth200)
async def test_form_works(hass: HomeAssistant) -> None:
    """Test the form works."""

    logging.basicConfig(level=logging.DEBUG)
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

#    print(f'result: {result}')
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {}

    # with patch(
    #     "custom_components.sonnenbackup.config_flow._validate_api",
    #     return_value=True,
    # ):
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        CONFIG_DATA,
    )
    await hass.async_block_till_done()

    config_entry:ConfigEntry = result["result"]
    assert config_entry.state == ConfigEntryState.LOADED
    config_data = config_entry.data
    assert config_data['model'] == CONFIG_DATA['model']
#    assert len(mock_setup_entry.mock_calls) == 1

    print(f'sensor_data: {hass.states.get("sensor.sonnenbackup_321123_led_state").state}')
    assert hass.states.get("sensor.sonnenbackup_321123_led_state").state == "Pulsing White 100%"
    assert hass.states.get("sensor.sonnenbackup_321123_led_state_text").state == "Normal Operation."
    assert hass.states.get("sensor.sonnenbackup_321123_led_status").state == "0x01 - ONGRID_READY"
    assert hass.states.get("sensor.sonnenbackup_321123_interval_to_fully_charged").state == "0d 01:46:52"
    assert hass.states.get("sensor.sonnenbackup_321123_status_timestamp").state == "2023-11-20T07:00:55+00:00"
    assert hass.states.get("sensor.sonnenbackup_321123_last_time_full").state == "2023-11-20T05:58:55+00:00"
    assert hass.states.get("sensor.sonnenbackup_321123_microgrid_enabled").state == 'False'
    assert hass.states.get("sensor.sonnenbackup_321123_usable_charge").state == '81'

#   Sensors used by Energy dashboard from integral helpers
    assert hass.states.get("sensor.sonnenbackup_321123_charge_power").state == '1394'
    assert hass.states.get("sensor.sonnenbackup_321123_consumption_now").state == '1578'
    assert hass.states.get("sensor.sonnenbackup_321123_production_now").state == '2972'
    assert hass.states.get("sensor.sonnenbackup_321123_discharge_power").state == '0'
    assert hass.states.get("sensor.sonnenbackup_321123_grid_export").state == '0'
    assert hass.states.get("sensor.sonnenbackup_321123_grid_import").state == '0'


# @pytest.mark.asyncio
# async def test_async_update_success(hass):
#     """Tests a fully successful async_update."""
#     UpdateCoordinator = MagicMock()
#     UpdateCoordinator.getitem = AsyncMock(
#         side_effect=[
#             {
#                 "state_sonnenbackup": "Charging",
#                 "state_system_status": "On Grid",
#                 "state_consumption_avg": 555,
#                 "state_battery_backup_buffer": 20,
#                 "state_battery_state_of_charge_real": 98,
#                 "state_battery_state_of_charge_usable": 91,
#                 "state_operating_mode": "2",
#                 "battery_system_cycles": 111
#             },
#         ]
#     )
#     sensor = BatterieSensorEntity(UpdateCoordinator, {"path": "homeassistant/core"})
#     await sensor.async_update()

#     expected = {
#         "state_sonnenbackup": "Charging",
#         "state_system_status": "On Grid",
#         "state_consumption_avg": 555,
#         "state_battery_backup_buffer": 20,
#         "state_battery_state_of_charge_real": 98,
#         "state_battery_state_of_charge_usable": 91,
#         "state_operating_mode": "2",
#         "battery_system_cycles": 111
#     }
#     assert expected == sensor.attrs
#     assert expected == sensor.extra_state_attributes
#     assert sensor.available is True


# @pytest.mark.asyncio
# async def test_async_update_failed():
#     """Tests a failed async_update."""
#     UpdateCoordinator = MagicMock()
#     UpdateCoordinator.getitem = AsyncMock(side_effect=BatterieError)

#     sensor = BatterieSensorEntity(UpdateCoordinator, {"path": "homeassistant/core"})
#     await sensor.async_update()

#     assert sensor.available is False
#     assert {"path": "homeassistant/core"} == sensor.attrs

"""Common fixtures for the SonnenBackup tests."""

from sonnen_api_v2 import Batterie

#for testing only
from collections.abc import Generator
from unittest.mock import AsyncMock, patch

import pytest
# from tests.common import MockConfigEntry
# from homeassistant.const import (
#         CONF_IP_ADDRESS,
#         CONF_API_TOKEN,
#         CONF_PORT,
#         CONF_MODEL,
#         CONF_DEVICE_ID,
#         CONF_SCAN_INTERVAL,
#         )

# from custom_components.sonnenbackup.const import DOMAIN, DEFAULT_SCAN_INTERVAL, DEFAULT_PORT
from . mock_sonnenbatterie_v2_charging import __mock_status_charging, __mock_latest_charging, __mock_configurations, __mock_battery, __mock_powermeter, __mock_inverter


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Override async_setup_entry."""
    with patch(
#        "homeassistant.components.sonnenbackup.async_setup_entry", return_value=True
        "custom_components.sonnenbackup.async_setup_entry", return_value=True
    ) as mock_setup_entry:
        yield mock_setup_entry

@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    yield

@pytest.fixture(autouse=True)
def mock_batterie_async(mocker):
    """Batterie charging using mock data for BackupBatterie.refresh_response()"""
    mocker.patch.object(Batterie, "async_fetch_configurations", AsyncMock(return_value=__mock_configurations()))
    mocker.patch.object(Batterie, "async_fetch_status", AsyncMock(return_value=__mock_status_charging()))
    mocker.patch.object(Batterie, "async_fetch_latest_details", AsyncMock(return_value=__mock_latest_charging()))
    mocker.patch.object(Batterie, "async_fetch_battery_status", AsyncMock(return_value=__mock_battery()))
    mocker.patch.object(Batterie, "async_fetch_powermeter", AsyncMock(return_value=__mock_powermeter()))
    mocker.patch.object(Batterie, "async_fetch_inverter", AsyncMock(return_value=__mock_inverter()))
    yield


# @pytest.fixture
# def mock_config_entry() -> MockConfigEntry:
#     """Mock a config entry."""
#     return MockConfigEntry(
#         domain=DOMAIN,
#         title="SonnenBackup Power unit Evo IP56 (321123)",
#         data={
#             CONF_IP_ADDRESS: "1.1.1.1",
#             CONF_PORT: DEFAULT_PORT,
#             CONF_API_TOKEN: "fakeToken",
#             "details": {
#                 CONF_MODEL: 'Power unit Evo IP56',
#                 CONF_DEVICE_ID: "321123"
#             }
#         },
#         options={
#             CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL,
#             "sonnen_debug": True,
#         },
#         unique_id='00JGB93KKQ0GYJ5K97CRGHQZHQ',
#     )
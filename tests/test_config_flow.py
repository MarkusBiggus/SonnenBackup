"""Test the SonnenBackup config flow.

    pytest tests/test_config_flow.py -s -v -x  -k test_form
"""

import pytest
from unittest.mock import patch
import datetime

from sonnen_api_v2 import Batterie, BatterieBackup, BatterieResponse
from . mock_sonnenbatterie_v2_charging import __mock_configurations

from homeassistant import config_entries
# from homeassistant.components.sonnenbackup.config_flow import CannotConnect, InvalidAuth
# from homeassistant.components.sonnenbackup.const import DOMAIN
from homeassistant.const import (
        CONF_IP_ADDRESS,
        CONF_API_TOKEN,
        CONF_PORT,
        CONF_MODEL,
        CONF_DEVICE_ID,
        CONF_SCAN_INTERVAL,
        )
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.sonnenbackup.config_flow import CannotConnect, InvalidAuth, DeviceAPIError
from custom_components.sonnenbackup.const import DOMAIN, DEFAULT_SCAN_INTERVAL

async def test_form(hass: HomeAssistant) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {}

    with patch(
        "custom_components.sonnenbackup.config_flow._validate_api",
        return_value=True,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_IP_ADDRESS: "1.1.1.1",
                CONF_PORT: 80,
                CONF_API_TOKEN: "fakeToken",
                "details": {
                    CONF_MODEL: 'Power unit Evo IP56',
                    CONF_DEVICE_ID: "321123"
                }
            },
        )
        await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "SonnenBackup Power unit Evo IP56 (321123)"
    assert result["data"] == {
        CONF_IP_ADDRESS: "1.1.1.1",
        CONF_PORT: 80,
        CONF_API_TOKEN: "fakeToken",
        "details": {
            CONF_MODEL: 'Power unit Evo IP56',
            CONF_DEVICE_ID: "321123"
        }
    }
#    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_invalid_auth(
    hass: HomeAssistant
) -> None:
    """Test we handle invalid auth."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.sonnenbackup.config_flow._validate_api",
        side_effect=InvalidAuth,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_IP_ADDRESS: "1.1.1.1",
                CONF_PORT: 80,
                CONF_API_TOKEN: "fakeToken",
                "details": {
                    CONF_MODEL: 'Power unit Evo IP56',
                    CONF_DEVICE_ID: "321123"
                }
            },
        )

    assert result["type"] == FlowResultType.FORM
#    assert result["errors"] == {"base": "invalid_auth"}
    assert result["errors"]["base"] == "invalid_auth"

    # Make sure the config flow tests finish with either an
    # FlowResultType.CREATE_ENTRY or FlowResultType.ABORT so
    # we can show the config flow is able to recover from an error.
    with patch(
        "custom_components.sonnenbackup.config_flow._validate_api",
        return_value=True,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_IP_ADDRESS: "1.1.1.1",
                CONF_PORT: 80,
                CONF_API_TOKEN: "fakeToken",
                "details": {
                    CONF_MODEL: 'Power unit Evo IP56',
                    CONF_DEVICE_ID: "321123"
                }
            },
        )
        await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "SonnenBackup Power unit Evo IP56 (321123)"
    assert result["data"] == {
        CONF_IP_ADDRESS: "1.1.1.1",
        CONF_PORT: 80,
        CONF_API_TOKEN: "fakeToken",
        "details": {
            CONF_MODEL: 'Power unit Evo IP56',
            CONF_DEVICE_ID: "321123"
        }
    }
#    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_cannot_connect(
    hass: HomeAssistant
) -> None:
    """Test we handle cannot connect error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.sonnenbackup.config_flow._validate_api",
        side_effect=CannotConnect,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_IP_ADDRESS: "1.1.1.1",
                CONF_PORT: 80,
                CONF_API_TOKEN: "fakeToken",
                "details": {
                    CONF_MODEL: 'Power unit Evo IP56',
                    CONF_DEVICE_ID: "321123"
                }
            },
        )

    assert result["type"] == FlowResultType.FORM
#    assert result["errors"] == {"base": "cannot_connect"}
    assert result["errors"]["base"] == "cannot_connect"

    # Make sure the config flow tests finish with either an
    # FlowResultType.CREATE_ENTRY or FlowResultType.ABORT so
    # we can show the config flow is able to recover from an error.

    with patch(
        "custom_components.sonnenbackup.config_flow._validate_api",
        return_value=True,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_IP_ADDRESS: "1.1.1.1",
                CONF_PORT: 80,
                CONF_API_TOKEN: "fakeToken",
                "details": {
                    CONF_MODEL: 'Power unit Evo IP56',
                    CONF_DEVICE_ID: "321123"
                }
            },
        )
        await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "SonnenBackup Power unit Evo IP56 (321123)"
    assert result["data"] == {
        CONF_IP_ADDRESS: "1.1.1.1",
        CONF_PORT: 80,
        CONF_API_TOKEN: "fakeToken",
        "details": {
            CONF_MODEL: 'Power unit Evo IP56',
            CONF_DEVICE_ID: "321123"
        }
    }
#    assert len(mock_setup_entry.mock_calls) == 1

async def test_form_device_error(
    hass: HomeAssistant
) -> None:
    """Test we handle device API HTTP error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.sonnenbackup.config_flow._validate_api",
        side_effect=DeviceAPIError,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_IP_ADDRESS: "1.1.1.1",
                CONF_PORT: 80,
                CONF_API_TOKEN: "fakeToken",
                "details": {
                    CONF_MODEL: 'Power unit Evo IP56',
                    CONF_DEVICE_ID: "321123"
                }
            },
        )

    assert result["type"] == FlowResultType.FORM
#    assert result["errors"] == {"base": "device_api_error"}
    assert result["errors"]["base"] == "device_api_error"

    # Make sure the config flow tests finish with either an
    # FlowResultType.CREATE_ENTRY or FlowResultType.ABORT so
    # we can show the config flow is able to recover from an error.

    with patch(
        "custom_components.sonnenbackup.config_flow._validate_api",
        return_value=True,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_IP_ADDRESS: "1.1.1.1",
                CONF_PORT: 80,
                CONF_API_TOKEN: "fakeToken",
                "details": {
                    CONF_MODEL: 'Power unit Evo IP56',
                    CONF_DEVICE_ID: "321123"
                }
            },
        )
        await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "SonnenBackup Power unit Evo IP56 (321123)"
    assert result["data"] == {
        CONF_IP_ADDRESS: "1.1.1.1",
        CONF_PORT: 80,
        CONF_API_TOKEN: "fakeToken",
        "details": {
            CONF_MODEL: 'Power unit Evo IP56',
            CONF_DEVICE_ID: "321123"
        }
    }
#    assert len(mock_setup_entry.mock_calls) == 1

@pytest.mark.asyncio
@patch.object(Batterie, 'fetch_configurations', __mock_configurations)
async def test_form_mocked(hass: HomeAssistant) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {}

    with patch(
        "custom_components.sonnenbackup.config_flow._validate_api",
        return_value=True,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_IP_ADDRESS: "1.1.1.1",
                CONF_PORT: 80,
                CONF_API_TOKEN: "fakeToken",
                "details": {
                    CONF_MODEL: 'Power unit Evo IP56',
                    CONF_DEVICE_ID: "321123"
                }
            },
        )
        await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "SonnenBackup Power unit Evo IP56 (321123)"
    assert result["data"] == {
        CONF_IP_ADDRESS: "1.1.1.1",
        CONF_PORT: 80,
        CONF_API_TOKEN: "fakeToken",
        "details": {
            CONF_MODEL: 'Power unit Evo IP56',
            CONF_DEVICE_ID: "321123"
        }
    }
#    assert len(mock_setup_entry.mock_calls) == 1


def __mock_BatterieResponse(*args):
    return BatterieResponse(
                version = '1.14.5',
                last_updated = datetime.datetime.now(),
                configurations = __mock_configurations()
                )

@pytest.mark.asyncio
#@patch("custom_components.sonnenbackup.sensor.SonnenBackupAPI")
#@patch.object("custom_components.sonnenbackup.BatterieBackup","get_response",
@patch.object(BatterieBackup, "get_response", __mock_BatterieResponse)
            # side_effect=lambda: BatterieResponse(
            #     version = '1.14.5',
            #     last_updated = datetime.datetime.now(),
            #     configurations = __mock_configurations()
            #     )
            #)
@patch.object(Batterie, 'fetch_configurations', __mock_configurations)
async def test_options_flow(hass):
    """Test config flow options."""

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="fake_unique_id",
        data={
            CONF_IP_ADDRESS: "1.1.1.1",
            CONF_PORT: 80,
            CONF_API_TOKEN: "fakeToken",
            CONF_MODEL: 'Power unit Evo IP56',
            CONF_DEVICE_ID: "321123",
            CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL,
            "sonnen_debug": False,
        },
    )
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    # show initial form
    result = await hass.config_entries.options.async_init(config_entry.entry_id)
    assert "form" == result["type"]
    assert "init" == result["step_id"]
    assert {} == result["errors"]

    # submit form with options
    result = await hass.config_entries.options.async_configure(
        result["flow_id"], user_input={
            CONF_SCAN_INTERVAL: 5,
            "sonnen_debug": True,
        }
    )
    assert "create_entry" == result["type"]
    assert "" == result["title"]
    assert result["result"] is True
    assert {
            CONF_SCAN_INTERVAL: 5,
            "sonnen_debug": True,
            } == result["data"]

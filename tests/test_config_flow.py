"""Test the SonnenBackup config flow.

    pytest tests/test_config_flow.py -s -v -x  -k test_form
"""

import pytest
from unittest.mock import AsyncMock, patch

from sonnen_api_v2 import Batterie
from . mock_sonnenbatterie_v2_charging import __mock_configurations

from homeassistant import config_entries
# from homeassistant.components.sonnenbackup.config_flow import CannotConnect, InvalidAuth
# from homeassistant.components.sonnenbackup.const import DOMAIN
from homeassistant.const import CONF_IP_ADDRESS, CONF_API_TOKEN, CONF_MODEL, CONF_DEVICE_ID
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.sonnenbackup.config_flow import CannotConnect, InvalidAuth, DeviceAPIError
from custom_components.sonnenbackup.const import DOMAIN

async def test_form(hass: HomeAssistant, mock_setup_entry: AsyncMock) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {}

    with patch(
#        "homeassistant.components.sonnenbackup.config_flow.validate_api",
        "custom_components.sonnenbackup.config_flow.validate_api",
        return_value=True,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_IP_ADDRESS: "1.1.1.1",
                CONF_API_TOKEN: "fakeToken",
                CONF_MODEL: 'Power unit Evo IP56',
                CONF_DEVICE_ID: "321123",
            },
        )
        await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "SonnenBackup Power unit Evo IP56 (321123)"
    assert result["data"] == {
        CONF_IP_ADDRESS: "1.1.1.1",
        CONF_API_TOKEN: "fakeToken",
        CONF_MODEL: 'Power unit Evo IP56',
        CONF_DEVICE_ID: "321123",
    }
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_invalid_auth(
    hass: HomeAssistant, mock_setup_entry: AsyncMock
) -> None:
    """Test we handle invalid auth."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
#        "homeassistant.components.sonnenbackup.config_flow.validate_api",
        "custom_components.sonnenbackup.config_flow.validate_api",
        side_effect=InvalidAuth,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_IP_ADDRESS: "1.1.1.1",
                CONF_API_TOKEN: "fakeToken",
                CONF_MODEL: 'Power unit Evo IP56',
                CONF_DEVICE_ID: "321123",
            },
        )

    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {"base": "invalid_auth"}

    # Make sure the config flow tests finish with either an
    # FlowResultType.CREATE_ENTRY or FlowResultType.ABORT so
    # we can show the config flow is able to recover from an error.
    with patch(
#        "homeassistant.components.sonnenbackup.config_flow.validate_api",
        "custom_components.sonnenbackup.config_flow.validate_api",
        return_value=True,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_IP_ADDRESS: "1.1.1.1",
                CONF_API_TOKEN: "fakeToken",
                CONF_MODEL: 'Power unit Evo IP56',
                CONF_DEVICE_ID: "321123",
            },
        )
        await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "SonnenBackup Power unit Evo IP56 (321123)"
    assert result["data"] == {
        CONF_IP_ADDRESS: "1.1.1.1",
        CONF_API_TOKEN: "fakeToken",
        CONF_DEVICE_ID: "321123",
    }
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_cannot_connect(
    hass: HomeAssistant, mock_setup_entry: AsyncMock
) -> None:
    """Test we handle cannot connect error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
#        "homeassistant.components.sonnenbackup.config_flow.validate_api",
        "custom_components.sonnenbackup.config_flow.validate_api",
        side_effect=CannotConnect,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_IP_ADDRESS: "1.1.1.1",
                CONF_API_TOKEN: "fakeToken",
                CONF_MODEL: 'Power unit Evo IP56',
                CONF_DEVICE_ID: "321123",
            },
        )

    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}

    # Make sure the config flow tests finish with either an
    # FlowResultType.CREATE_ENTRY or FlowResultType.ABORT so
    # we can show the config flow is able to recover from an error.

    with patch(
#        "homeassistant.components.sonnenbackup.config_flow.validate_api",
        "custom_components.sonnenbackup.config_flow.validate_api",
        return_value=True,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_IP_ADDRESS: "1.1.1.1",
                CONF_API_TOKEN: "fakeToken",
                CONF_MODEL: 'Power unit Evo IP56',
                CONF_DEVICE_ID: "321123",
            },
        )
        await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "SonnenBackup Power unit Evo IP56 (321123)"
    assert result["data"] == {
        CONF_IP_ADDRESS: "1.1.1.1",
        CONF_API_TOKEN: "fakeToken",
        CONF_MODEL: 'Power unit Evo IP56',
        CONF_DEVICE_ID: "321123",
    }
    assert len(mock_setup_entry.mock_calls) == 1

async def test_form_device_error(
    hass: HomeAssistant, mock_setup_entry: AsyncMock
) -> None:
    """Test we handle device API HTTP error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
#        "homeassistant.components.sonnenbackup.config_flow.validate_api",
        "custom_components.sonnenbackup.config_flow.validate_api",
        side_effect=DeviceAPIError,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_IP_ADDRESS: "1.1.1.1",
                CONF_API_TOKEN: "fakeToken",
                CONF_MODEL: 'Power unit Evo IP56',
                CONF_DEVICE_ID: "321123",
            },
        )

    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}

    # Make sure the config flow tests finish with either an
    # FlowResultType.CREATE_ENTRY or FlowResultType.ABORT so
    # we can show the config flow is able to recover from an error.

    with patch(
#        "homeassistant.components.sonnenbackup.config_flow.validate_api",
        "custom_components.sonnenbackup.config_flow.validate_api",
        return_value=True,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_IP_ADDRESS: "1.1.1.1",
                CONF_API_TOKEN: "fakeToken",
                CONF_MODEL: 'Power unit Evo IP56',
                CONF_DEVICE_ID: "321123",
            },
        )
        await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "SonnenBackup Power unit Evo IP56 (321123)"
    assert result["data"] == {
        CONF_IP_ADDRESS: "1.1.1.1",
        CONF_API_TOKEN: "fakeToken",
        CONF_MODEL: 'Power unit Evo IP56',
        CONF_DEVICE_ID: "321123",
    }
    assert len(mock_setup_entry.mock_calls) == 1

@pytest.mark.asyncio
@patch.object(Batterie, 'fetch_configurations', __mock_configurations)
async def test_form_mocked(hass: HomeAssistant, mock_setup_entry: AsyncMock) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {}

    with patch(
#        "homeassistant.components.sonnenbackup.config_flow.validate_api",
        "custom_components.sonnenbackup.config_flow.validate_api",
        return_value=True,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_IP_ADDRESS: "1.1.1.1",
                CONF_API_TOKEN: "fakeToken",
                CONF_MODEL: 'Power unit Evo IP56',
                CONF_DEVICE_ID: "321123",
            },
        )
        await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "SonnenBackup Power unit Evo IP56 (321123)"
    assert result["data"] == {
        CONF_IP_ADDRESS: "1.1.1.1",
        CONF_API_TOKEN: "fakeToken",
        CONF_MODEL: 'Power unit Evo IP56',
        CONF_DEVICE_ID: "321123",
    }
    assert len(mock_setup_entry.mock_calls) == 1

"""Test the SonnenBackup config flow.

    pytest tests/test_config_flow.py -s -v -x  -k test_form
"""

import pytest
from unittest.mock import patch, AsyncMock
from responses import Response

import datetime
import urllib3

from sonnen_api_v2 import Batterie, BatterieBackup, BatterieResponse
from .mock_sonnenbatterie_v2_charging import __mock_configurations
from .mock_batterieresponse import __mock_batterieresponse

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
from custom_components.sonnenbackup.const import DOMAIN, DEFAULT_SCAN_INTERVAL, DEFAULT_PORT

CONFIG_DATA = {
    CONF_IP_ADDRESS: "1.1.1.1",
    CONF_PORT: DEFAULT_PORT,
    CONF_API_TOKEN: "fakeToken",
    "details": {
        CONF_MODEL: 'Power unit Evo IP56',
        CONF_DEVICE_ID: "321123"
    }
}
CONFIG_OPTIONS = {
    CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL,
    "sonnen_debug": True,
}


def __battery_configurations(self, _method, _url, _body, _headers, _retries):
    """Mock configurations to validate Auth naturally."""
    resp = Response(
        method=_method, #'GET',
        url=_url, #(f'http://fakeHost:80/api/v2/configurations'),
        json=__mock_configurations(),
        status=200,
        headers=_headers,
    )
    return resp


async def test_form(hass: HomeAssistant) -> None:
    """Test we get the form."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {}

    with patch(
        "custom_components.sonnenbackup.config_flow._validate_api",
        return_value=True,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            CONFIG_DATA,
        )
        await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "SonnenBackup Power unit Evo IP56 (321123)"
    assert result["data"] == CONFIG_DATA
#    assert len(mock_setup_entry.mock_calls) == 1


@patch.object(urllib3.HTTPConnectionPool, 'urlopen', __battery_configurations)
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
            CONFIG_DATA,
        )

    # Make sure the config flow tests finish with either an
    # FlowResultType.CREATE_ENTRY or FlowResultType.ABORT so
    # we can show the config flow is able to recover from an error.
    assert result["type"] == FlowResultType.FORM
    assert result["errors"]["base"] == "invalid_auth"

    # with patch(
    #     "custom_components.sonnenbackup.config_flow._validate_api",
    #     return_value=True,
    # ):

    # use mocked battery response to cache data (more code gets tested)
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        CONFIG_DATA,
    )
    await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "SonnenBackup Power unit Evo IP56 (321123)"
    assert result["data"] == CONFIG_DATA
#    assert len(mock_setup_entry.mock_calls) == 1


@patch.object(urllib3.HTTPConnectionPool, 'urlopen', __battery_configurations)
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
            CONFIG_DATA,
        )

    assert result["type"] == FlowResultType.FORM
    assert result["errors"]["base"] == "cannot_connect"

    # Make sure the config flow tests finish with either an
    # FlowResultType.CREATE_ENTRY or FlowResultType.ABORT so
    # we can show the config flow is able to recover from an error.

    # with patch(
    #     "custom_components.sonnenbackup.config_flow._validate_api",
    #     return_value=True,
    # ):

    # use mocked battery response to cache data (more code gets tested)
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        CONFIG_DATA,
    )

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "SonnenBackup Power unit Evo IP56 (321123)"
    assert result["data"] == CONFIG_DATA
#    assert len(mock_setup_entry.mock_calls) == 1


@patch.object(urllib3.HTTPConnectionPool, 'urlopen', __battery_configurations)
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
            CONFIG_DATA,
        )

    assert result["type"] == FlowResultType.FORM
    assert result["errors"]["base"] == "device_api_error"

    # Make sure the config flow tests finish with either an
    # FlowResultType.CREATE_ENTRY or FlowResultType.ABORT so
    # we can show the config flow is able to recover from an error.

    # with patch(
    #     "custom_components.sonnenbackup.config_flow._validate_api",
    #     return_value=True,
    # ):

    # use mocked battery response to cache data (more code gets tested)
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        CONFIG_DATA,
    )

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "SonnenBackup Power unit Evo IP56 (321123)"
    assert result["data"] == CONFIG_DATA
#    assert len(mock_setup_entry.mock_calls) == 1


@pytest.mark.asyncio
#@patch.object(Batterie, 'fetch_configurations', __mock_configurations)
@patch.object(urllib3.HTTPConnectionPool, 'urlopen', __battery_configurations)
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
            CONFIG_DATA,
        )
        await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "SonnenBackup Power unit Evo IP56 (321123)"
    assert result["data"] == CONFIG_DATA
#    assert len(mock_setup_entry.mock_calls) == 1


@pytest.mark.asyncio
@patch.object(BatterieBackup, "refresh_response", __mock_batterieresponse)
@patch.object(BatterieBackup, "validate_token", __mock_batterieresponse)
async def test_options_flow(hass):
    """Test config flow options."""

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="fake_unique_id",
        data=CONFIG_DATA,
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
        result["flow_id"],
        user_input={
            CONF_SCAN_INTERVAL: 5,
            "sonnen_debug": True,
        }
    )
    assert FlowResultType.CREATE_ENTRY == result["type"]
    assert "" == result["title"]
    assert result["result"] is True
    assert {
            CONF_SCAN_INTERVAL: 5,
            "sonnen_debug": True,
            } == result["data"]


@pytest.mark.asyncio
@patch.object(urllib3.HTTPConnectionPool, 'urlopen', __battery_configurations)
async def test_config_flow_fail_non_unique(
    hass: HomeAssistant
) -> None:
    """Test that the config flow fails when user tries to add duplicate batterie."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {}

    with patch(
        "custom_components.sonnenbackup.config_flow._validate_api",
        return_value=True,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            CONFIG_DATA,
        )
        await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "SonnenBackup Power unit Evo IP56 (321123)"
    assert result["data"] == CONFIG_DATA


    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {}

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], CONFIG_DATA
    )

#    print(f'result: {dict(result)}')
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"

"""Test the SonnenBackup config flow.

    pytest tests/test_config_flow.py -s -v -x  -k test_form_works
"""

import pytest
from unittest.mock import patch, AsyncMock
from responses import Response
import logging

import datetime
import urllib3
from  voluptuous.error import MultipleInvalid

from sonnen_api_v2 import Batterie, BatterieBackup, BatterieResponse
from .mock_sonnenbatterie_v2_charging import __mock_configurations

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntryState, ConfigEntry
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
from homeassistant.data_entry_flow import FlowResultType, InvalidData

#from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.sonnenbackup.config_flow import CannotConnect, InvalidAuth, DeviceAPIError
from custom_components.sonnenbackup.const import DOMAIN, DEFAULT_SCAN_INTERVAL, DEFAULT_PORT
from .mock_battery_responses import (
    __battery_auth200,
    # __battery_AuthError_401,
    # __battery_AuthError_403,
    # __battery_HTTPError_301,
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
    CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL,
    "sonnenbackup_debug": True,
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

#    print(f'result: {result}')
#    config_entry = getattr(hass.config_entries, self.domain)
#    assert config_entry.state == ConfigEntryState.LOADED
    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "SonnenBackup Power unit Evo IP56 (321123)"
    assert result["data"] == CONFIG_DATA
    config_entry:ConfigEntry = result["result"]
    assert config_entry.state == ConfigEntryState.LOADED
    config_data = config_entry.data #hass_data[config_entry.entry_id]
#    print(f'config_data: {config_data}')
    assert config_data['model'] == CONFIG_DATA['model']
#    assert len(mock_setup_entry.mock_calls) == 1


@patch.object(urllib3.HTTPConnectionPool, 'urlopen', __battery_auth200)
async def test_form_invalid_auth(hass: HomeAssistant) -> None:
    """Test invalid auth."""

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

    config_entry = result["result"]
    assert config_entry.state == ConfigEntryState.LOADED
#    assert len(mock_setup_entry.mock_calls) == 1


@patch.object(urllib3.HTTPConnectionPool, 'urlopen', __battery_auth200)
async def test_form_cannot_connect(hass: HomeAssistant) -> None:
    """Test cannot connect error."""

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

    config_entry = result["result"]
    assert config_entry.state == ConfigEntryState.LOADED
#    assert len(mock_setup_entry.mock_calls) == 1


@patch.object(urllib3.HTTPConnectionPool, 'urlopen', __battery_auth200)
async def test_form_device_error(hass: HomeAssistant) -> None:
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

    config_entry = result["result"]
    assert config_entry.state == ConfigEntryState.LOADED
#    assert len(mock_setup_entry.mock_calls) == 1


@pytest.mark.asyncio
@patch.object(urllib3.HTTPConnectionPool, 'urlopen', __battery_auth200)
async def test_form_mocked(hass: HomeAssistant) -> None:
    """Test the form with mock validaton."""

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

    config_entry = result["result"]
    assert config_entry.state == ConfigEntryState.LOADED

#    assert len(mock_setup_entry.mock_calls) == 1


@pytest.mark.asyncio
#@patch.object(BatterieBackup, "refresh_response", __mock_batterieresponse)
#@patch.object(BatterieBackup, "validate_token", __mock_batterieresponse)
@patch.object(urllib3.HTTPConnectionPool, 'urlopen', __battery_auth200)
async def test_options_flow(hass: HomeAssistant) -> None:
    """Test config flow options."""

    # config_entry = MockConfigEntry(
    #     domain=DOMAIN,
    #     unique_id="fake_unique_id",
    #     data=CONFIG_DATA,
    # )
    # config_entry.add_to_hass(hass)
    # assert await hass.config_entries.async_setup(config_entry.entry_id)
    # await hass.async_block_till_done()
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        CONFIG_DATA,
    )
    await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "SonnenBackup Power unit Evo IP56 (321123)"
    assert result["data"] == CONFIG_DATA
#    print(f'config: {dict(result)}')

    # show initial form
    config_entry:config_entries.ConfigEntry = result["result"]
    assert config_entry.state == ConfigEntryState.LOADED

    result = await hass.config_entries.options.async_init(config_entry.entry_id)
    assert FlowResultType.FORM == result["type"]
    assert "init" == result["step_id"]
    assert {} == result["errors"]

    # submit form with invalid options
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={
            CONF_SCAN_INTERVAL: 2,
            "sonnenbackup_debug": True,
        }
    )
    assert FlowResultType.FORM == result["type"]
    assert "init" == result["step_id"]
#    print(f'result: {result}')
    assert result["errors"]["base"] == 'invalid_interval'
    assert result["description_placeholders"]["error_detail"] == 'Scan interval "2" must be at least 3 seconds and no more than 120.'
    # assert {
    #         CONF_SCAN_INTERVAL: 2,
    #         "sonnenbackup_debug": True,
    #         } == result["data"]

    # submit form with invalid options
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={
            CONF_SCAN_INTERVAL: 200,
            "sonnenbackup_debug": True,
        }
    )
    assert FlowResultType.FORM == result["type"]
    assert "init" == result["step_id"]
    assert result["errors"]["base"] == 'invalid_interval'
    assert result["description_placeholders"]["error_detail"] == 'Scan interval "200" must be at least 3 seconds and no more than 120.'
    # # assert {
    # #         CONF_SCAN_INTERVAL: 2,
    # #         "sonnenbackup_debug": True,
    # #         } == result["data"]
    # #print(f'result: {dict(result)}')

    # # submit form with valid options
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input=CONFIG_OPTIONS
    )
    assert FlowResultType.CREATE_ENTRY == result["type"]
    assert "" == result["title"]
    assert result["result"] is True
    #print(f'result: {dict(result)}')
    assert CONFIG_OPTIONS == result["data"]

    hass.config_entries.async_update_entry(
        config_entry,
        options=result["data"]
    )
    #print(f'config: {config_entry.as_dict()}')
    assert config_entry.options == result["data"]
    assert config_entry.data == CONFIG_DATA

@pytest.mark.asyncio
@patch.object(urllib3.HTTPConnectionPool, 'urlopen', __battery_auth200)
async def test_config_flow_fail_non_unique(hass: HomeAssistant) -> None:
    """Test config flow fails adding duplicate batterie."""

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

    #print(f'result: {dict(result)}')
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"

@pytest.mark.asyncio
async def test_form_invalid_port(hass: HomeAssistant) -> None:
    """Various kinds of invalid port numbers."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

#     with patch(
# #        "custom_components.sonnenbackup.config_flow",
# #        "homeassistant.data_entry_flow",
#         "homeassistant.config_entries.ConfigEntriesFlowManager._async_configure",
# #        "voluptuous.error",
#         side_effect=InvalidData,
# #        side_effect=MultipleInvalid,
#     ):
#         result = await hass.config_entries.flow.async_configure(
#             result["flow_id"],
#             {
#                 CONF_IP_ADDRESS: "1.1.1.1",
#                 CONF_PORT: 99999, # above 65535
#                 CONF_API_TOKEN: "fakeToken-111-222-4444-3333",
#                 "details": {
#                     CONF_MODEL: 'Power unit Evo IP56',
#                     CONF_DEVICE_ID: "321123"
#                 }
#             }
#         )

#     assert result["errors"] == {"base": "invalid_port"}

    # with patch(
    #     "custom_components.sonnenbackup.config_flow",
    #     side_effect=InvalidData,
    # ):
    #     result = await hass.config_entries.flow.async_configure(
    #         result["flow_id"],
    #         {
    #             CONF_IP_ADDRESS: "1.1.1.1",
    #             CONF_PORT: '9ABC8', # hexadecimal
    #             CONF_API_TOKEN: "fakeToken-111-222-4444-3333",
    #             "details": {
    #                 CONF_MODEL: 'Power unit Evo IP56',
    #                 CONF_DEVICE_ID: "321123"
    #             }
    #         }
    #     )

    # assert result["errors"] == {"base": "invalid_port"}

    # if result.get("errors", {}) != {"base": "invalid_port"}:
    #     msg = "Expected invalid port error."
    #     raise ValueError(msg)
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_IP_ADDRESS: "1.1.1.1",
            CONF_PORT: 59999,# above 49151 (ephemeral port)
            CONF_API_TOKEN: "fakeToken-111-222-4444-3333",
            # "details": {
            CONF_MODEL: 'Power unit Evo IP56',
            CONF_DEVICE_ID: "321123"
            # }
        }
    )
    assert result["errors"] == {"base": "invalid_port"}



@pytest.mark.asyncio
@patch.object(urllib3.HTTPConnectionPool, 'urlopen', __battery_auth200)
async def test_options_flow_works(hass: HomeAssistant) -> None:
    """Test config flow options work."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        CONFIG_DATA,
    )
    await hass.async_block_till_done()

#    print(f'result: {dict(result)}')

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "SonnenBackup Power unit Evo IP56 (321123)"
    assert result["data"] == CONFIG_DATA

    # show initial form
    config_entry:config_entries.ConfigEntry = result["result"]
    result = await hass.config_entries.options.async_init(config_entry.entry_id)

    assert FlowResultType.FORM == result["type"]
    assert "init" == result["step_id"]
    assert {} == result["errors"]

    # submit form with valid options
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input=CONFIG_OPTIONS
    )

#    print(f'result: {dict(result)}')

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == ''
    assert result["result"] is True
#    print(f'result: {dict(result)}')
    assert CONFIG_OPTIONS == result["data"]

    # update entry with options
    success = hass.config_entries.async_update_entry(
        config_entry,
        options=result["data"]
    )

    assert success is True
#    print(f'config: {config_entry.as_dict()}')
    assert config_entry.options == result["data"]
    assert config_entry.data == CONFIG_DATA

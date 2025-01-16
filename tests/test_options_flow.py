"""Test the Scenario config flow."""

import pytest
from homeassistant import config_entries
from homeassistant.const import CONF_DELAY
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry
from homeassistant.const import (
        CONF_IP_ADDRESS,
        CONF_API_TOKEN,
        CONF_PORT,
        CONF_MODEL,
        CONF_DEVICE_ID,
        CONF_SCAN_INTERVAL,
        )

from custom_components.sonnenbackup.const import (
    _DOMAIN,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_PORT,
)

DOMAIN = _DOMAIN

CONFIG_DATA = {
    CONF_IP_ADDRESS: "1.1.1.1",
    CONF_PORT: DEFAULT_PORT,
    CONF_API_TOKEN: "fakeToken-111-222-4444-3333",
    "details": {
        CONF_MODEL: 'Power unit Evo IP56',
        CONF_DEVICE_ID: "321123"
    }
}
CONFIG_OPTIONS = {
    CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL,
    "sonnen_debug": True,
}

@pytest.mark.asyncio
async def test_options_flow(hass: HomeAssistant) -> None:
    """Test config flow options."""

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data=CONFIG_DATA,
        options=CONFIG_OPTIONS,
    )
    config_entry.add_to_hass(hass)

    # Test options flow
    result = await hass.config_entries.options.async_init(config_entry.entry_id)

    assert FlowResultType.FORM == result["type"]
    assert "init" == result["step_id"]
    assert {} == result["errors"]

    # if result.get("type", {}) != FlowResultType.FORM:
    #     msg = "Expected form."
    #     raise ValueError(msg)

    # if result.get("step_id", {}) != "init":
    #     msg = "Expected init step."
    #     raise ValueError(msg)

    # Test updating options flow
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={
            CONF_SCAN_INTERVAL: 15,
            "sonnen_debug": True,
        },
    )

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "SonnenBackup Power unit Evo IP56 (321123)"
    assert config_entry.options == {
            CONF_SCAN_INTERVAL: 15,
            "sonnen_debug": True,
    }

    # if result.get("type", {}) != FlowResultType.CREATE_ENTRY:
    #     msg = "Expected create entry."
    #     raise ValueError(msg)

    # if config_entry.options != {
    #         CONF_SCAN_INTERVAL: 15,
    #         "sonnen_debug": True,
    # }:
    #     msg = "Expected options updated."
    #     raise ValueError(msg)

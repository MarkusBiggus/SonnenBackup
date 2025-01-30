"""Test the Scenario config flow.

    pytest tests/test_options_flow.py -s -v -x  -k test_options_flow
"""

import pytest
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
    DOMAIN,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_PORT,
)

CONFIG_DATA = {
    CONF_IP_ADDRESS: "1.1.1.1",
    CONF_PORT: DEFAULT_PORT,
    CONF_API_TOKEN: "fakeToken-111-222-4444-3333",
    # "details": {
    CONF_MODEL: 'Power unit Evo IP56',
    CONF_DEVICE_ID: "321123"
    # }
}
CONFIG_OPTIONS = {
    CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL,
    "sonnenbackup_debug": True,
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

    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "init"
    assert result["errors"] == {}
#    print(f'result: {result}')

    # Test updating options flow
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={
            CONF_SCAN_INTERVAL: 15 #,
#            "sonnenbackup_debug": True,
        },
    )

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == '' # "SonnenBackup Power unit Evo IP56 (321123)"
    assert config_entry.options == {
            CONF_SCAN_INTERVAL: 15#,
#            "sonnenbackup_debug": True,
    }
    assert result["result"] is True # is config_entry when config_flow
#    print(f'result: {result}')

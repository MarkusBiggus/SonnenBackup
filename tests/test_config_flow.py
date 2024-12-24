"""Tests for the sonnenbackup config flow."""

from unittest.mock import patch

from homeassistant import config_entries
from homeassistant.const import CONF_IP_ADDRESS, CONF_PASSWORD, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from sonnenbackup.const import DOMAIN
from sonnen_api_v2 import BatterieResponse, BatterieBackup
from .mock_batterieresponse import __mock_batterieresponse


def __mock_real_time_api_success():
    return BatterieBackup('fakeUsername', 'fakeToken', 'fakeHost')


async def test_form_success(hass: HomeAssistant) -> None:
    """Test successful form."""
    flow = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert flow["type"] is FlowResultType.FORM
    assert flow["errors"] == {}

    with (
        patch(
            "homeassistant.custom_components.sonnen.config_flow.real_time_api",
            return_value=__mock_real_time_api_success(),
        ),
        patch("sonnen.BatterieBackup.get_response", return_value=__mock_batterieresponse()),
        patch(
            "homeassistant.custom_components.sonnenbackup.async_setup_entry",
            return_value=True,
        ) as mock_setup_entry,
    ):
        entry_result = await hass.config_entries.flow.async_configure(
            flow["flow_id"],
            {CONF_IP_ADDRESS: "192.168.100.200", CONF_PORT: 80, CONF_PASSWORD: "password"},
        )
        await hass.async_block_till_done()

    assert entry_result["type"] is FlowResultType.CREATE_ENTRY
    assert entry_result["title"] == "ABCDEFGHIJ"
    assert entry_result["data"] == {
        CONF_IP_ADDRESS: "192.168.100.200",
        CONF_PORT: 80,
        CONF_PASSWORD: "password",
    }
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_connect_error(hass: HomeAssistant) -> None:
    """Test cannot connect form."""
    flow = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert flow["type"] is FlowResultType.FORM
    assert flow["errors"] == {}

    with patch(
        "homeassistant.custom_components.sonnenbackup.config_flow.real_time_api",
        side_effect=ConnectionError,
    ):
        entry_result = await hass.config_entries.flow.async_configure(
            flow["flow_id"],
            {CONF_IP_ADDRESS: "192.168.100.200", CONF_PORT: 80, CONF_PASSWORD: "password"},
        )

    assert entry_result["type"] is FlowResultType.FORM
    assert entry_result["errors"] == {"base": "cannot_connect"}


async def test_form_unknown_error(hass: HomeAssistant) -> None:
    """Test unknown error form."""
    flow = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert flow["type"] is FlowResultType.FORM
    assert flow["errors"] == {}

    with patch(
        "homeassistant.custom_components.sonnenbackup.config_flow.real_time_api",
        side_effect=Exception,
    ):
        entry_result = await hass.config_entries.flow.async_configure(
            flow["flow_id"],
            {CONF_IP_ADDRESS: "192.168.100.200", CONF_PORT: 80, CONF_PASSWORD: "password"},
        )

    assert entry_result["type"] is FlowResultType.FORM
    assert entry_result["errors"] == {"base": "unknown"}

"""Config flow for sonnen batterie integration."""

from __future__ import annotations

import logging
from typing import Any

from sonnen_api_v2.sonnen import Sonnen as Batterie
from sonnen_api_v2.discovery import DiscoveryError
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_IP_ADDRESS, CONF_API_TOKEN, CONF_PORT, CONF_DEVICE_ID, CONF_API_VERSION
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

DEFAULT_PORT = 80
DEFAULT_API_VERSION = 'V2'

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_IP_ADDRESS): cv.string,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
        vol.Required(CONF_API_TOKEN): cv.string,
        vol.Optional(CONF_API_VERSION, default=DEFAULT_API_VERSION): cv.string,
        vol.Required(CONF_DEVICE_ID): cv.string,
    }
)


async def validate_api(data) -> str:
    """Validate the credentials."""

    api = await Batterie(
        data[CONF_API_TOKEN],
        data[CONF_IP_ADDRESS],
        data[CONF_PORT],
    )
    response = await api.get_data()
    return response.version


class SonnenConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Sonnen Batterie."""

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, Any] = {}
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
            )
        serial_number = user_input[CONF_DEVICE_ID]

        try:
            version = await validate_api(user_input)
        except (ConnectionError, DiscoveryError):
            errors["base"] = "cannot_connect"
        except Exception:
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            await self.async_set_unique_id(serial_number)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=serial_number, data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

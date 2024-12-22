"""Config flow for sonnen batterie integration."""

from __future__ import annotations

import logging
from typing import Any

from sonnen_api_v2 import Batterie
from sonnen_api_v2.discovery import DiscoveryError
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.core import callback
from homeassistant.const import CONF_IP_ADDRESS, CONF_API_TOKEN, CONF_PORT, CONF_DEVICE_ID, CONF_API_VERSION, CONF_MODEL
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, CONFIG_SCHEMA

_LOGGER = logging.getLogger(__name__)

DEFAULT_PORT = '80'
DEFAULT_API_VERSION = 'V2'


async def validate_api(data) -> str:
    """Validate the credentials."""

    _batterie = Batterie(
        data[CONF_API_TOKEN],
        data[CONF_IP_ADDRESS],
        data[CONF_PORT],
    )
    response = await _batterie.get_data()
    return response.version


class SonnenConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Sonnen Batterie."""
    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, Any] = {}
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=CONFIG_SCHEMA, errors=errors
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
            step_id="user", data_schema=CONFIG_SCHEMA, errors=errors
        )

    async def async_step_progress(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Displaying rogress for two tasks"""
        _LOGGER.info("async_step_progress")
        task = asyncio.sleep(3)
        _LOGGER.info("scheduling task")
 #       self.task_one = self.hass.async_create_task(self._async_do_task(task))
        progress_action = "user_task"
        _LOGGER.info("showing_progress: %s", progress_action)
        return self.async_show_progress(
            step_id="progress",
            progress_action=progress_action,
        )
        _LOGGER.info("async_step_progress - all tasks done")
        return self.async_show_progress_done(next_step_id="finish")

    async def async_step_finish(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        _LOGGER.info("async_step_finish")
        return self.async_create_entry(
            title="SonnenBackup",
            data={},
        )



    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler(config_entry)



OPTIONS_SCHEMA = vol.Schema(
    {
        vol.Optional(
            CONF_SCAN_INTERVAL,
            default=self.config_entry.options.get(
                CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
            ),
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
    }
)

class SonnenOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:

        if user_input is not None:
            return self.async_create_entry(title="XxX", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema = self.add_suggested_values_to_schema(
                OPTIONS_SCHEMA, self.entry.options
            )
        )
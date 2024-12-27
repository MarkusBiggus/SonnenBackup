"""Config flow for sonnenbackup batterie integration."""

from __future__ import annotations

import logging
from typing import Any

from sonnen_api_v2 import Batterie, BatterieAuthError, BatterieError

import voluptuous as vol

#from homeassistant import config_entries, core, exceptions

from homeassistant.config_entries import (
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
    CONN_CLASS_LOCAL_POLL,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.const import (
        CONF_IP_ADDRESS,
        CONF_API_TOKEN,
        CONF_PORT,
        CONF_MODEL,
        CONF_DEVICE_ID,
        CONF_SCAN_INTERVAL,
        )
import homeassistant.helpers.config_validation as cv
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, CONFIG_SCHEMA, DEFAULT_SCAN_INTERVAL, DEFAULT_PORT

_LOGGER = logging.getLogger(__name__)

async def validate_api(user_input) -> str:
    """Validate credentials."""

    _batterie = Batterie(
        user_input[CONF_API_TOKEN],
        user_input[CONF_IP_ADDRESS],
        user_input[CONF_PORT],
    )
    try:
        response = await _batterie.get_response()
    except BatterieAuthError:
        raise InvalidAuth
    except BatterieError:
        raise CannotConnect

    return response.version


class SonnenConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SonnenBackup."""
    VERSION = 1

    CONNECTION_CLASS = CONN_CLASS_LOCAL_POLL

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
            version:str = await validate_api(user_input)
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except (ConnectionError, BatterieError):
            errors["base"] = "cannot_connect"
        except Exception:
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            await self.async_set_unique_id(serial_number)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=f'Sonnen Batterie ({serial_number})', data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=CONFIG_SCHEMA, errors=errors
        )

#     async def async_step_progress(
#         self, user_input: dict[str, Any] | None = None
#     ) -> ConfigFlowResult:
#         """Displaying rogress for two tasks"""
#         _LOGGER.info("async_step_progress")
#         task = asyncio.sleep(3)
#         _LOGGER.info("scheduling task")
#  #       self.task_one = self.hass.async_create_task(self._async_do_task(task))
#         progress_action = "user_task"
#         _LOGGER.info("showing_progress: %s", progress_action)
#         return self.async_show_progress(
#             step_id="progress",
#             progress_action=progress_action,
#         )
#         _LOGGER.info("async_step_progress - all tasks done")
#         return self.async_show_progress_done(next_step_id="finish")

#     async def async_step_finish(
#         self, user_input: dict[str, Any] | None = None
#     ) -> ConfigFlowResult:
#         _LOGGER.info("async_step_finish")
#         return self.async_create_entry(
#             title="SonnenBackup",
#             data={},
#         )


    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return SonnenBackupOptionsFlow(config_entry)

OPTIONS_SCHEMA = vol.Schema(
    {
        vol.Optional(
            CONF_SCAN_INTERVAL,
            default=DEFAULT_SCAN_INTERVAL
        ): cv.Number,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
    }
)

class SonnenBackupOptionsFlow(OptionsFlow):
    """SonnenBackup options."""
    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:

        if user_input is not None:
            return self.async_create_entry(title=f'Sonnen Batterie ({self.options[CONF_DEVICE_ID]})', data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema = self.add_suggested_values_to_schema(
                OPTIONS_SCHEMA, self.entry.options
            )
        )

class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""

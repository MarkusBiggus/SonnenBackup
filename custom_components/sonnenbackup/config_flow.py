"""Config flow for sonnenbackup batterie integration."""

from __future__ import annotations

import logging
from typing import Any

from sonnen_api_v2 import Batterie, BatterieAuthError, BatterieHTTPError, BatterieError

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
        )
import homeassistant.helpers.config_validation as cv
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, CONFIG_SCHEMA, OPTIONS_SCHEMA

_LOGGER = logging.getLogger(__name__)

async def _validate_api(user_input) -> str:
    """Validate credentials."""

    _batterie = Batterie(
        user_input[CONF_API_TOKEN],
        user_input[CONF_IP_ADDRESS],
        user_input[CONF_PORT],
    )
    try:
        success = await _batterie.async_validate_token()
    except BatterieAuthError as error:
        raise InvalidAuth (f'{str(error)}')
    except BatterieHTTPError as error:
        raise DeviceAPIError (f'{str(error)}')
    except BatterieError as error:
        raise CannotConnect(f'Batterie connection fail. {str(error)}')

    if success is False:
        raise InvalidAuth ('Invalid Token or IP address')

    return success


class SonnenBackupConfigFlow(ConfigFlow, domain=DOMAIN):
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
        batterie_model = user_input[CONF_MODEL]

        try:
            await _validate_api(user_input)
        except InvalidAuth as error:
            errors["base"] = 'invalid_auth'
            errors["message"] = f'{str(error)}'
        except DeviceAPIError as error:
            errors["base"] = 'device_api_error'
            errors["message"] = f'{str(error)}'
        except (ConnectionError, CannotConnect) as error:
            errors["base"] = 'cannot_connect'
            errors["message"] = f'{str(error)}'
        except Exception as error:
            _LOGGER.exception('Unexpected exception')
            errors["base"] = "unknown"
            errors["message"] = f'{str(error)}'
        else:
            await self.async_set_unique_id(serial_number)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=f'SonnenBackup {batterie_model} ({serial_number})', data=user_input)

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

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None):
        """Handle the reconfiguration step."""

        errors: dict[str, Any] = {}
        if user_input is None:
            return self.async_show_form(
                step_id="reconfigure", data_schema=CONFIG_SCHEMA, errors=errors
            )

        serial_number = user_input[CONF_DEVICE_ID] # can't be changed!
        batterie_model = user_input[CONF_MODEL]

        try:
            await _validate_api(user_input)
        except InvalidAuth as error:
            errors["base"] = 'invalid_auth'
            errors["message"] = f'{str(error)}'
        except DeviceAPIError as error:
            errors["base"] = 'device_api_error'
            errors["message"] = f'{str(error)}'
        except (ConnectionError, CannotConnect) as error:
            errors["base"] = 'cannot_connect'
            errors["message"] = f'{str(error)}'
        except Exception as error:
            _LOGGER.exception('Unexpected exception')
            errors["base"] = "unknown"
            errors["message"] = f'{str(error)}'
        else:
            self.async_set_unique_id(serial_number)
            self._abort_if_unique_id_mismatch()
            return self.async_update_reload_and_abort(
                self._get_reconfigure_entry(),
                title=f'SonnenBackup {batterie_model} ({serial_number})',
                data_updates=user_input,
            )

        return self.async_show_form(
            step_id="reconfigure", data_schema=CONFIG_SCHEMA, errors=errors
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
            return self.async_create_entry(title=f'SonnenBackup {self.options[CONF_MODEL]} ({self.options[CONF_DEVICE_ID]})', data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema = self.add_suggested_values_to_schema(
                OPTIONS_SCHEMA, self.entry.options
            )
        )

class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""

class DeviceAPIError(HomeAssistantError):
    """Error to indicate device API error."""

class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""

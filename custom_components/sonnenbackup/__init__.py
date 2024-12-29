"""The SonnenBackup batterie backup component."""

from __future__ import annotations

from datetime import timedelta
import logging
import json

from sonnen_api_v2 import BatterieResponse, BatterieBackup, BatterieAuthError, BatterieHTTPError, BatterieError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_IP_ADDRESS,
    CONF_API_TOKEN,
    CONF_PORT,
    CONF_DEVICE_ID,
    CONF_SCAN_INTERVAL,
)
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import UpdateFailed

from .coordinator import SonnenBackupUpdateCoordinator, SonnenBackupAPI

from .const import (
    DOMAIN,
    PLATFORMS,
    DEFAULT_SCAN_INTERVAL,
    )

SCAN_INTERVAL = timedelta(seconds=DEFAULT_SCAN_INTERVAL)


type SonnenBackupConfigEntry = ConfigEntry[SonnenBackupAPI]

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config_entry: SonnenBackupConfigEntry):
    """Set up SonnenBackup component."""

# !!!!!!!!!!!!!! config_entry is empty !!!!!!!!!!!!!
    entity_id = f'{DOMAIN}.{'987789'}' #data[CONF_DEVICE_ID]}'
    hass.states.async_set(entity_id, {})

    # Return boolean to indicate that initialization was successful.
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: SonnenBackupConfigEntry) -> bool:
    """Set up SonnenBackup from a config entry."""

    _LOGGER.info("SonnenBackupConfigEntry: " + json.dumps(dict(config_entry.data)))

    try:
        _batterie:BatterieBackup = BatterieBackup(
            config_entry.data[CONF_API_TOKEN],
            config_entry.data[CONF_IP_ADDRESS],
            config_entry.data[CONF_PORT],
        )
    except Exception as error:
        raise ConfigEntryNotReady from error

    async def _async_update() -> BatterieResponse:
        try:
            return await _batterie.get_response()
        except (BatterieAuthError, BatterieHTTPError, BatterieError) as error:
            raise UpdateFailed from error
        # except Exception as error:
        #     raise UpdateFailed from error

    coordinator = SonnenBackupUpdateCoordinator(
        hass,
        logger=_LOGGER,
        name=f"{config_entry.title} coordinator",
        update_interval=SCAN_INTERVAL,
        update_method=_async_update,
    )
    await coordinator.async_config_entry_first_refresh()

    config_entry.runtime_data = SonnenBackupAPI(api=_batterie, coordinator=coordinator, serial_number=config_entry.data[CONF_DEVICE_ID])
    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    hass_data = dict(config_entry.data)
    # Registers update listener to update config entry when options are updated.
    unsub_options_update_listener = config_entry.add_update_listener(options_update_listener)
    # Store a reference to the unsubscribe function to cleanup if an entry is unloaded.
    hass_data["unsub_options_update_listener"] = unsub_options_update_listener
    hass.data[DOMAIN][config_entry.entry_id] = hass_data

    return True

async def options_update_listener(hass: HomeAssistant, config_entry: SonnenBackupConfigEntry):
    """Handle options update."""

    coordinator: SonnenBackupUpdateCoordinator = config_entry.runtime_data["coordinator"]
    coordinator.update_interval(timedelta(seconds=config_entry.options[CONF_SCAN_INTERVAL]))
    await hass.config_entries.async_reload(config_entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, config_entry: SonnenBackupConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(config_entry, PLATFORMS)

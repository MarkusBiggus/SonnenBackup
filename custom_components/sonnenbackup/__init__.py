"""The SonnenBackup batterie backup component."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
import logging

from sonnen_api_v2 import BatterieResponse, BatterieBackup, BatterieAuthError, BatterieHTTPError, BatterieError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_IP_ADDRESS, CONF_API_TOKEN, CONF_PORT, CONF_DEVICE_ID
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import UpdateFailed

from .coordinator import SonnenBackupUpdateCoordinator

from .const import (
    DOMAIN,
    PLATFORMS,
    DEFAULT_SCAN_INTERVAL
    )

SCAN_INTERVAL = timedelta(seconds=DEFAULT_SCAN_INTERVAL)


@dataclass(slots=True)
class SonnenBackupAPI:
    """Sonnenbackup batterie API context."""

    api: BatterieBackup
    coordinator: SonnenBackupUpdateCoordinator
    serial_number: str


type SonnenBackupConfigEntry = ConfigEntry[SonnenBackupAPI]

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config):
    hass.states.async_set(DOMAIN, {})

    # Return boolean to indicate that initialization was successful.
    return True

async def async_setup_entry(hass: HomeAssistant, entry: SonnenBackupConfigEntry) -> bool:
    """Set up SonnenBackup from a config entry."""

    try:
        _batterie:BatterieBackup = BatterieBackup(
            entry.data[CONF_API_TOKEN],
            entry.data[CONF_IP_ADDRESS],
            entry.data[CONF_PORT],
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
        name=f"sonnenbackup {entry.title}",
        update_interval=SCAN_INTERVAL,
        update_method=_async_update,
    )
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = SonnenBackupAPI(api=_batterie.BatterieBackup, coordinator=coordinator, serial_number=entry.data[CONF_DEVICE_ID])
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: SonnenBackupConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

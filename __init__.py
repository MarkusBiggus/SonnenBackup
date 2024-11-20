"""The sonnen component."""

from dataclasses import dataclass
from datetime import timedelta
import logging

from sonnen_api_v2.sonnen import BatterieResponse, RealTimeAPI, Sonnen, BatterieError
#from sonnen.inverter import InverterError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_IP_ADDRESS, CONF_API_TOKEN, CONF_PORT, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import UpdateFailed

from .coordinator import SonnenDataUpdateCoordinator

PLATFORMS = [Platform.SENSOR]

SCAN_INTERVAL = timedelta(seconds=30)


@dataclass(slots=True)
class SonnenData:
    """Class for storing sonnen data."""

    api: RealTimeAPI
    coordinator: SonnenDataUpdateCoordinator


type SonnenConfigEntry = ConfigEntry[SonnenData]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: SonnenConfigEntry) -> bool:
    """Set up the sensors from a ConfigEntry."""

    try:
        api = await Sonnen(
            entry.data[CONF_API_TOKEN],
            entry.data[CONF_IP_ADDRESS],
            entry.data[CONF_PORT],
        )
    except Exception as err:
        raise ConfigEntryNotReady from err

    async def _async_update() -> BatterieResponse:
        try:
            return await api.get_data()
        except BatterieError as err:
            raise UpdateFailed from err

    coordinator = SonnenDataUpdateCoordinator(
        hass,
        logger=_LOGGER,
        name=f"sonnen {entry.title}",
        update_interval=SCAN_INTERVAL,
        update_method=_async_update,
    )
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = SonnenData(api=api, coordinator=coordinator)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: SonnenConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

"""The SonnenBackup batterie component."""

from __future__ import annotations

from datetime import timedelta
import logging
import voluptuous as vol

from sonnen_api_v2 import BatterieResponse, BatterieBackup, BatterieAuthError, BatterieHTTPError, BatterieError

from homeassistant.data_entry_flow import section
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_IP_ADDRESS,
    CONF_API_TOKEN,
    CONF_PORT,
    CONF_MODEL,
    CONF_DEVICE_ID,
    CONF_SCAN_INTERVAL,
)
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import UpdateFailed
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

from .coordinator import SonnenBackupUpdateCoordinator, SonnenBackupAPI

from .const import (
    PLATFORMS,
    MANUFACTURER,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_PORT
)

DOMAIN = "sonnenbackup"
CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_IP_ADDRESS): cv.string,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): cv.port,
        vol.Required(CONF_API_TOKEN): cv.string,
        "details": section(
#            {'fields':
                vol.Schema(
                    {
                        vol.Required(CONF_MODEL): cv.string,
                        vol.Required(CONF_DEVICE_ID): cv.string,
                    }
                ),
#            },
        # Whether or not the section is initially collapsed (default = False)
            {"collapsed": False},
        )
    }
)

SCAN_INTERVAL = timedelta(seconds=DEFAULT_SCAN_INTERVAL)

type SonnenBackupConfigEntry = ConfigEntry[SonnenBackupAPI]

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config_entry: dict):
    """Set up SonnenBackup component."""

    hass.data.setdefault(DOMAIN, {})

    # Return boolean to indicate that initialization was successful.
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: SonnenBackupConfigEntry) -> bool:
    """Set up SonnenBackup from a config entry."""

#    _LOGGER.info("SonnenBackupConfigEntry: " + json.dumps(dict(config_entry.data)))
    _LOGGER.info("SonnenBackupConfigEntry setup")

    try:
        _batterie = BatterieBackup(
            config_entry.data[CONF_API_TOKEN],
            config_entry.data[CONF_IP_ADDRESS],
            config_entry.data[CONF_PORT],
        )
    except Exception as error:
        raise ConfigEntryNotReady from error

    async def _async_update() -> BatterieResponse:
        """Update Batterie data caches"""

        _LOGGER.info("SonnenBackup component async_update")
        try:
            return await _batterie.refresh_response() # returned into coordinator.data
        except (BatterieAuthError, BatterieHTTPError, BatterieError) as error:
            raise UpdateFailed from error
        # except Exception as error:
        #     raise UpdateFailed from error


    # coordinator.data is BatterieResponse from update_method
    coordinator = SonnenBackupUpdateCoordinator(
        hass,
        logger=_LOGGER,
        name=f"{config_entry.title} coordinator",
        update_interval=SCAN_INTERVAL,
        update_method=_async_update,
    )
    await coordinator.async_config_entry_first_refresh()

    config_entry.runtime_data = SonnenBackupAPI(
        api=_batterie,
        coordinator=coordinator,
        serial_number=config_entry.data['details'][CONF_DEVICE_ID],
        version=coordinator.data.version,
        last_updated=coordinator.data.last_updated
    )
    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    hass_data = dict(config_entry.data[DOMAIN][config_entry.entry_id])
    # Registers update listener to update config entry when options are updated.
    unsub_options_update_listener = config_entry.add_update_listener(options_update_listener)
    # Store a reference to the unsubscribe function to cleanup if an entry is unloaded.
    hass_data["unsub_options_update_listener"] = unsub_options_update_listener
    hass.data[DOMAIN][config_entry.entry_id] = hass_data
#    print(f'hass.data: {hass.data[DOMAIN]}  {config_entry}')

    return True

async def options_update_listener(hass: HomeAssistant, config_entry: SonnenBackupConfigEntry):
    """Handle options update."""

    _LOGGER.info("SonnenBackupConfigEntry reload")
    coordinator: SonnenBackupUpdateCoordinator = config_entry.runtime_data.coordinator
    coordinator.update_interval = timedelta(seconds=config_entry.options[CONF_SCAN_INTERVAL])
    await hass.config_entries.async_reload(config_entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, config_entry: SonnenBackupConfigEntry) -> bool:
    """Unload a config entry."""

    _LOGGER.info("SonnenBackupConfigEntry unload")
    if unload_ok := await hass.config_entries.async_unload_platforms(config_entry, PLATFORMS):
        # Remove config entry from domain.
        if config_entry.entry_id in hass.data[DOMAIN]:
    #        print(f'remove hass.data: {hass.data[DOMAIN]}  {config_entry}')
            config_data = hass.data[DOMAIN].pop(config_entry.entry_id)
            # Remove options_update_listener.
            config_data["unsub_options_update_listener"]()

    return unload_ok

# class SonnenBackupUpdatableEntity(Entity):
#     """Base entity for SonnenBackup."""

#     _attr_should_poll = False

#     def __init__(self, device: BatterieBackup) -> None:
#         """Initialize a SonnenBackup entity."""
#         self._device = device
#         self._attr_name = config_entry.model
#         self._attr_available = device.available
#         self._attr_unique_id = config_entry.serial_number
#         self._device_name = config_entry.model
#         self._device_manufacturer = MANUFACTURER
#         self._device_id = config_entry.serial_number
#         info = DeviceInfo(
#             identifiers={(DOMAIN, str(device.unique_id))},
#             manufacturer=MANUFACTURER,
#             name=self._attr_name,
# #            suggested_area=device.zone,
#         )
#         self._attr_device_info = info

#     @property
#     def available(self) -> bool:
#         """Check availability of the device."""
#         return self._attr_available
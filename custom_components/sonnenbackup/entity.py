"""SonnenBackupEntity class."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    # CONF_IP_ADDRESS,
    # CONF_API_TOKEN,
    # CONF_PORT,
    CONF_MODEL,
    CONF_DEVICE_ID,
)

from sonnen_api_v2 import BatterieResponse

from .const import (
    DOMAIN,
    LOGGER,
    MANUFACTURER,
    ATTRIBUTION,
)
from .coordinator import SonnenBackupUpdateCoordinator, SonnenBackupAPI


class SonnenBackupCoordinatorEntity(CoordinatorEntity[SonnenBackupUpdateCoordinator]):
    """SonnenBackupCoordinator Entity."""

    _attr_attribution = ATTRIBUTION
    _sensor_last_time_full = None

    def __init__(self, coordinator: SonnenBackupUpdateCoordinator) -> None:
        """Initialize Coordinator Entity."""

        super().__init__(coordinator)
        config_entry = coordinator.config_entry
        # runtime_data: SonnenBackupAPI = config_entry.runtime_data
        # serial_number = runtime_data.serial_number
        # version = runtime_data.version
        serial_number=config_entry.data[CONF_DEVICE_ID],
        model=config_entry.data[CONF_MODEL],
        version=coordinator.data.version,
        self._attr_unique_id = config_entry.entry_id
        self._attr_name = model
#        self._attr_available = device.available
#        self._attr_unique_id = config_entry.runtime_data.serial_number
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, serial_number)},
            manufacturer=MANUFACTURER,
            model=model,
            name=f"BackupBatterie {serial_number}",
            sw_version=version,
        )

    @property
    def available(self) -> bool:
        """Device Availability."""
        return self._attr_available

    def cache_repeating_values(self, batterie_response: BatterieResponse
    ) -> BatterieResponse:
        """Repeating values cached until new non-repeated value."""

        """seconds_since_full is zero each update whilst battery is fully charged.
            Cache the update time when first zero value until non-zero, then
            clear cache and use response values.
        """
        if batterie_response.sensor_values.get('seconds_since_full') == 0:
            if self._sensor_last_time_full is None:
                self._sensor_last_time_full = batterie_response.sensor_values.get('last_updated')
            batterie_response.sensor_values.put('last_time_full', self._sensor_last_time_full)
        elif self._sensor_last_time_full is not None:
            self._sensor_last_time_full = None

        return batterie_response



# class SonnenBackupEntity(Entity):
#     """Base entity for SonnenBackup."""

#     _attr_should_poll = False

#     def __init__(self, device: BatterieBackup) -> None:
#         """Initialize SonnenBackup entity."""
#         self._device = device
#         self._attr_name = config_entry.model
#         self._attr_available = device.available
#         self._attr_unique_id = config_entry.serial_number
#         info = DeviceInfo(
#             identifiers={(DOMAIN, str(device.unique_id))},
#             manufacturer=MANUFACTURER,
#             name=self._attr_name,
# #            suggested_area=device.zone,
#         )
#         self._attr_device_info = info

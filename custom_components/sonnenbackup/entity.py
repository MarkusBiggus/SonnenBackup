"""SonnenBackupEntity class."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
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
from .coordinator import SonnenBackupUpdateCoordinator, SonnenBackupRTData, BatterieData


class SonnenBackupEntity(CoordinatorEntity[DataUpdateCoordinator[BatterieData]]):
    """DataUpdateCoordinator SonnenBackupEntity."""

    _attr_attribution = ATTRIBUTION
    _sensor_last_time_full = None

    def __init__(self, sonnenbackup: SonnenBackupRTData) -> None:
        """Initialize Coordinator SonnenBackupEntity."""

        super().__init__(sonnenbackup.coordinator)
#        config_entry = sonnenbackup.coordinator.config_entry
        model=sonnenbackup.model # config_entry.data[CONF_MODEL],
        self._attr_unique_id = "SonnenBackup_Batteries" # config_entry.entry_id
        self._attr_name = f"SonnenBackup {model}"
        self._attr_available = True #device.available
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.unique_id)},
            manufacturer=MANUFACTURER,
            model=model,
            name="SonnenBackup Batteries",
#            sw_version=sonnenbackup.version,
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
            clear cache and use response values until zero again.
        """
        if batterie_response.sensor_values.get('seconds_since_full') == 0:
            if self._sensor_last_time_full is None:
                self._sensor_last_time_full = batterie_response.sensor_values.get('last_updated')
            batterie_response.sensor_values.put('last_time_full', self._sensor_last_time_full)
        elif self._sensor_last_time_full is not None:
            self._sensor_last_time_full = None

        return batterie_response

class BatterieEntity(CoordinatorEntity[SonnenBackupUpdateCoordinator[BatterieData]]):
    """Base class for SonnenBackup BatterieEntity."""

    _attr_has_entity_name = True

    def __init__(self, sonnenbackup: SonnenBackupRTData) -> None:
        """Initialize the BatterieEntity."""

        coordinator = sonnenbackup.coordinator
        assert coordinator is not None
        super().__init__(coordinator)
        self.batterie = sonnenbackup.api
        self.serial_number = sonnenbackup.serial_number
        self._unique_id = f"BackupBatterie_{sonnenbackup.serial_number}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.unique_id)},
            manufacturer=MANUFACTURER,
            model=sonnenbackup.model,
            name=self.unique_id, # f"BackupBatterie_{sonnenbackup.serial_number}",
            sw_version=sonnenbackup.version,
            # name=base_info.site_info.site_name,
            # configuration_url=base_info.url,
        )

    @property
    def data(self) -> BatterieData:
        """Return the coordinator data."""
        return self.coordinator.data



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

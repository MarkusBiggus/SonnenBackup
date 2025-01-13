"""Support for SonnenBackup Batterie via local API V2."""

from __future__ import annotations

import logging
from collections.abc import Callable
#from typing import Any

from sonnen_api_v2 import BatterieBackup

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
#    SensorEntityDescription,
    SensorStateClass,
)
#from homeassistant import config_entries, core
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity, UpdateFailed
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
)
from .const import (
    DOMAIN,
    MANUFACTURER,
    SENSOR_DESCRIPTIONS,
)
from .coordinator import SonnenBackupAPI
from .PowerUnitEVO import PowerUnitEVO

#from . import SonnenConfigEntry
type SonnenBackupConfigEntry = ConfigEntry[SonnenBackupAPI]

#DOMAIN = _DOMAIN
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: SonnenBackupConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Entry setup."""

    _LOGGER.info('Setup sensor entries')

    # api is BatterieBackup class
    api:BatterieBackup = config_entry.runtime_data.api
    serial_number = config_entry.runtime_data.serial_number
    coordinator = config_entry.runtime_data.coordinator
    batterie_response = coordinator.data
    version = batterie_response.version
#    hass_data = hass.data[DOMAIN][config_entry.entry_id]
    # hass_data = hass.data[DOMAIN] # setdefault(DOMAIN, {})
    # _LOGGER.info(f'hass_data: {hass_data}')
    # hass_data_entry = hass_data.get(config_entry.entry_id)
    # _LOGGER.debug(f'hass_data_entry: {hass_data_entry}')
    # _LOGGER.debug(f'config rtd: {config_entry.runtime_data}')
    device_info = DeviceInfo(
        identifiers={(DOMAIN, serial_number)},
        manufacturer=MANUFACTURER,
        model=config_entry.runtime_data.model,
        name=f"{MANUFACTURER} {serial_number}",
        sw_version=version,
    )
    battery_sensors = PowerUnitEVO(api)
    sensor_values = battery_sensors.map_response()

    entities: list[BatterieSensorEntity] = []
    for sensor, (idx, measurement, alias) in battery_sensors.sensor_map().items():
    #    _LOGGER.debug(f'sensor: {sensor}  idx:{idx}  measurement: {measurement}')
        description = SENSOR_DESCRIPTIONS[(measurement.unit, measurement.is_monotonic)]
        uid = f"SB{serial_number}-{idx}"
    #    _LOGGER.debug(f'sensor: {sensor}  uid:{uid}  description: {description}')
        entities.append(
            BatterieSensorEntity(
                config_entry,
                # coordinator,
                # MANUFACTURER,
                # uid,
                # serial_number,
                # version,
                device_info,
                uid,
                sensor,
                idx,
                alias,
                description.native_unit_of_measurement,
                description.state_class,
                description.device_class,
            )
        )
    async_add_entities(entities)

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: Callable,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""

    _LOGGER.info('Setup sensor platform')


class BatterieSensorEntity(CoordinatorEntity, SensorEntity):
    """Class for a sensor."""

    _attr_should_poll = False
    _attr_icon = "mdi:battery-outline"

    def __init__(
        self,
        config_entry: SonnenBackupConfigEntry,
        device_info: DeviceInfo,
        uid: str,
        sensor: str,
        sensor_idx: int,
        alias: str,
        unit: str | None,
        state_class: SensorStateClass | str | None,
        device_class: SensorDeviceClass | None,
    ) -> None:
        """Initialize a battery sensor."""
        super().__init__(config_entry.runtime_data.coordinator)

        serial_number = config_entry.runtime_data.serial_number
        self._batterybackup = config_entry.runtime_data.api
        self._unique_id = uid
        self._name = f"{DOMAIN} {alias} {serial_number}"
        self._has_entity_name = True
        self._native_unit_of_measurement = unit
        self._state_class = state_class
        self._device_class = device_class
        self._device_info = device_info
        self._available = True
        self.key = sensor
        self._idx = sensor_idx
        self.alias = alias
        self._state = 'on'

    #    _LOGGER.debug(f'Setup sensor: {sensor} value: {self.native_value}')

    @property
    def device_info(self):
        """Return DeviceInfo object."""
        return self._device_info

    @property
    def native_value(self):
        """Value of this sensor from mapped battery property."""
        _LOGGER.debug(f'Native sensor: {self.key} value: {self.coordinator.data[self._unique_id]}')
#        return self.coordinator.data[self._unique_id] # ??????????????????
        return self._batterybackup.get_sensor_value(self.key)

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name if self._has_entity_name else '*noname*'

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return self._unique_id

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    @property
    def state(self) -> str | None:
        """Return entity state."""
    #    print(f'Sensor: {self.key}: {self.coordinator.data[self._unique_id]}')
        return self._state
    #    _LOGGER.debug(f'State sensor: {self.key} value: {self.coordinator.data[self._unique_id]}')
    #    return self.coordinator.data[self._unique_id] # ??????????????????

    # async def async_update(self) -> None:
    #     """Update all sensors."""
    #     try:
    #         await self.coordinator["update_method"]()


    #         self._available = True
    #     except (UpdateFailed, BatterieError):
    #         self._available = False
    #         _LOGGER.exception(
    #             "Error retrieving data from GitHub for sensor %s", self.name
    #         )
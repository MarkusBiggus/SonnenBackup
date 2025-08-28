"""Support for SonnenBackup Batterie via local API V2."""

from __future__ import annotations

import logging
from collections.abc import Callable
#from typing import Any


from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
#from homeassistant import config_entries, core
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
)
from homeassistant.const import (
    EntityCategory,
)
from .const import (
    DOMAIN,
    LOGGER,
    MANUFACTURER,
    SENSOR_DESCRIPTIONS,
    SENSOR_GROUP_UNITS,
    SENSOR_GROUP_TIMESTAMP,
    SENSOR_GROUP_DELTATIME,
    SENSOR_GROUP_ENUM,
)
from . import BatterieBackup
from .coordinator import SonnenBackupAPI
from .PowerUnitEVO import PowerUnitEVO, SonnenBackupSensorEntityDescription

type SonnenBackupConfigEntry = ConfigEntry[SonnenBackupAPI]

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: SonnenBackupConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Batterie sensors based on config entry."""

    LOGGER.info('Setup sensor entities')

# from example, where is device defined before this call?
#    device: ExampleDevice = hass.data[DOMAIN][config_entry.entry_id]

    api:BatterieBackup = config_entry.runtime_data.api
    serial_number = config_entry.runtime_data.serial_number
    coordinator = config_entry.runtime_data.coordinator
    batterie_response = coordinator.data
    version = batterie_response.version
#    hass_data = hass.data[DOMAIN][config_entry.entry_id]
    # hass_data = hass.data[DOMAIN] # setdefault(DOMAIN, {})
    # LOGGER.info(f'hass_data: {hass_data}')
    # hass_data_entry = hass_data.get(config_entry.entry_id)
    # LOGGER.debug(f'hass_data_entry: {hass_data_entry}')
    # LOGGER.debug(f'config rtd: {config_entry.runtime_data}')
    device_info = DeviceInfo(
        configuration_url=config_entry.runtime_data.api.url,
        identifiers={(DOMAIN, serial_number)},
        manufacturer=MANUFACTURER,
        model=config_entry.runtime_data.model,
        name=f"SonnenBackup {serial_number}",
        sw_version=version,
    )


    battery_sensors = PowerUnitEVO(api)
    entities: list[BatterieSensorEntity] = []
    for alias, (idx, measurement, sensor, group, options) in battery_sensors.mapped_sensors().items():
        if group == SENSOR_GROUP_UNITS:
    #       LOGGER.debug(f'{SENSOR_GROUP_UNITS}: {sensor}  idx:{idx}  measurement: {measurement}')
            description = SENSOR_DESCRIPTIONS[SENSOR_GROUP_UNITS][(measurement.unit, measurement.is_monotonic)]
        elif group == SENSOR_GROUP_TIMESTAMP:
            description = SENSOR_DESCRIPTIONS[SENSOR_GROUP_TIMESTAMP][(measurement.unit, measurement.is_monotonic)] # only (Units.NONE, False)
        elif group == SENSOR_GROUP_DELTATIME:
            description = SENSOR_DESCRIPTIONS[SENSOR_GROUP_DELTATIME][(measurement.unit, measurement.is_monotonic)] # only (Units.NONE, False)
        elif group == SENSOR_GROUP_ENUM:
            description = SENSOR_DESCRIPTIONS[SENSOR_GROUP_ENUM][(measurement.unit, measurement.is_monotonic)]
            if description.options is None:
                description = SensorEntityDescription(
                    description.key,
                    description.device_class,
                    options=options
                )
        else:
            raise ValueError(f'Sensor {sensor} unknown group: {group}')

        uid = f"SonnenBackup_{serial_number}-{idx}"
    #    LOGGER.info(f'sensor: {sensor}  uid:{uid}  description: {description}')
        entities.append(
            BatterieSensorEntity(
                config_entry,
                device_info,
                uid,
                sensor,
                idx,
                alias,
                description
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

    LOGGER.info('Setup sensor platform') #######  NOT called!!!!!!!!!!!????


class BatterieSensorEntity(CoordinatorEntity, SensorEntity):
    """Represent a battery sensor."""

    _attr_should_poll = False
    _attr_icon = "mdi:battery-outline"
    _attr_has_entity_name = True
    _attr_entity_category = (
            EntityCategory.DIAGNOSTIC
    )
    entity_description: SonnenBackupSensorEntityDescription

    def __init__(
        self,
        config_entry: SonnenBackupConfigEntry,
        device_info: DeviceInfo,
        uid: str,
        sensor: str,
        sensor_idx: int,
        alias: str,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize a battery sensor."""
        super().__init__(config_entry.runtime_data.coordinator)

        self.entity_description = description
#        serial_number = config_entry.runtime_data.serial_number
        self._batterybackup = config_entry.runtime_data.api
        self._unique_id = uid
#        self._name = f"{DOMAIN} {alias}"
        self._name = alias
        self._has_entity_name = True
        self._native_unit_of_measurement = description.native_unit_of_measurement
        self._suggested_display_precision = description.suggested_display_precision
        self._state_class = description.state_class
        self._device_class = description.device_class
        self._options = description.options
        self._device_info = device_info
        self._available = True
        self.key = sensor
        self._idx = sensor_idx
        self.alias = alias
        self._state = 'on'

    @property
    def device_info(self):
        """Return DeviceInfo object."""
        return self._device_info

    @property
    def native_value(self):
        """Value of this sensor from mapped battery property."""
        # self.coordinator.data is last BatterieResponse from async_setup_entry._async_update
        self._attr_native_value = self.coordinator.data.sensor_values.get(self.alias) #self._batterybackup.get_sensor_value(self.key)
        LOGGER.debug(f'Alias: {self.alias} value: {self._attr_native_value} Sensor: {self.key} Name: {self._name}')
        return self._attr_native_value

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

### Was never called!
### https://developers.home-assistant.io/docs/core/entity/#property-implementation
    # def update(self) -> None:
    #         """Update entity state."""
    #         # try:
    # #            self._attr_native_value self._batterybackup.get_sensor_value(self.key)
    #         # except BatterieSensorError:
    #         #     if self.available:  # Read current state, no need to prefix with _attr_
    #         #         LOGGER.warning(f'Sensor {self.key} update failed! ID: {entity_id}')
    #         #     self._attr_available = False  # Set property value
    #         #     return
    #         # self._attr_available = Ture

    #         #self._attr_available = True
    #         # We don't need to check if device available here
    #         LOGGER.debug(f'Alias: {self.alias} value: {self._attr_native_value} Native: {self.key}')
    #         self._attr_native_value = self.coordinator.data.sensor_values.get(self.alias) # data coordinator gets sensor_values from device
    #         # self._attr_native_value = self.entity_description.value_fn(
    #         #     self._device
    #         # )
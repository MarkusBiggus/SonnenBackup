"""Support for SonnenBackup Batterie via local API V2."""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

from sonnen_api_v2 import BatterieError
from sonnen_api_v2.units import Units

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfTemperature,
)
from homeassistant import config_entries, core
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity, UpdateFailed
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
)
from .const import DOMAIN, MANUFACTURER
from .coordinator import SonnenBackupUpdateCoordinator, SonnenBackupAPI

#from . import SonnenConfigEntry
type SonnenBackupConfigEntry = ConfigEntry[SonnenBackupAPI]

_LOGGER = logging.getLogger(__name__)

SENSOR_DESCRIPTIONS: dict[tuple[Units, bool], SensorEntityDescription] = {
    (Units.C, False): SensorEntityDescription(
        key=f"{Units.C}_{False}",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    (Units.KWH, False): SensorEntityDescription(
        key=f"{Units.KWH}_{False}",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    (Units.KWH, True): SensorEntityDescription(
        key=f"{Units.KWH}_{True}",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    (Units.V, False): SensorEntityDescription(
        key=f"{Units.V}_{False}",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    (Units.A, False): SensorEntityDescription(
        key=f"{Units.A}_{False}",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    (Units.W, False): SensorEntityDescription(
        key=f"{Units.W}_{False}",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    (Units.PERCENT, False): SensorEntityDescription(
        key=f"{Units.PERCENT}_{False}",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    (Units.HZ, False): SensorEntityDescription(
        key=f"{Units.HZ}_{False}",
        device_class=SensorDeviceClass.FREQUENCY,
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    (Units.NONE, False): SensorEntityDescription(
        key=f"{Units.NONE}_{False}",
    ),
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SonnenBackupConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Entry setup."""
    api = entry.runtime_data.api
    coordinator = entry.runtime_data.coordinator
    resp = coordinator.data
    serial_number = entry.runtime_data.serial_number
    version = resp.version
    entities: list[BatterieSensorEntity] = []
    for sensor, (idx, measurement) in api.battery.sensor_map().items():
        description = SENSOR_DESCRIPTIONS[(measurement.unit, measurement.is_monotonic)]

        uid = f"{serial_number}-{idx}"
        entities.append(
            BatterieSensorEntity(
                coordinator,
                api.battery.manufacturer,
                uid,
                serial_number,
                version,
                sensor,
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

    # github = GitHubAPI(session, "requester", oauth_token=config[CONF_ACCESS_TOKEN])
    # sensors = [GitHubRepoSensor(github, repo) for repo in config[CONF_REPOS]]
    # async_add_entities(sensors, update_before_add=True)



class BatterieSensorEntity(CoordinatorEntity, SensorEntity):
    """Class for a sensor."""

    _attr_should_poll = False

    def __init__(
        self,
        coordinator: SonnenBackupUpdateCoordinator,
        manufacturer: str,
        uid: str,
        serial_number: str,
        version: str,
        key: str,
        unit: str | None,
        state_class: SensorStateClass | str | None,
        device_class: SensorDeviceClass | None,
    ) -> None:
        """Initialize a battery sensor."""
        super().__init__(coordinator)
        self._unique_id = uid
        self._name = f"{DOMAIN} {serial_number} {key}"
        self._has_entity_name = True
        self._native_unit_of_measurement = unit
        self._state_class = state_class
        self._device_class = device_class
        self._device_info = DeviceInfo(
            identifiers={(DOMAIN, serial_number)},
            manufacturer=MANUFACTURER,
            name=f"{manufacturer} {serial_number}",
            sw_version=version,
        )
        self._available = True
        self.key = key

    @property
    def device_info(self):
        """Return DeviceInfo object."""
        return self._device_info

    @property
    def native_value(self):
        """Value of this battery attribute."""
        return self.coordinator.data[self.key]

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
        return self._state

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
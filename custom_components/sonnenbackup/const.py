"""Constants for the sonnenbackup integration."""

import voluptuous as vol

from sonnen_api_v2.units import Units

import homeassistant.helpers.config_validation as cv
from homeassistant.data_entry_flow import section
from homeassistant.components.sensor import (
    SensorDeviceClass,
#    SensorEntity,
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

from homeassistant.const import (
    Platform,
    CONF_IP_ADDRESS,
    CONF_API_TOKEN,
    CONF_PORT,
    CONF_MODEL,
    CONF_DEVICE_ID,
    CONF_SCAN_INTERVAL,
)
DOMAIN = "sonnenbackup"
MANUFACTURER = "Sonnen GmbH"
DEFAULT_SCAN_INTERVAL = 10
ATTR_SONNEN_DEBUG = "sonnenbackup_debug"
DEFAULT_PORT = 80

PLATFORMS: list[Platform] = [Platform.SENSOR]

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_IP_ADDRESS): cv.string,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): cv.port,
        vol.Required(CONF_API_TOKEN): cv.string,
        "details": section(
            vol.Schema(
                {
                    vol.Required(CONF_MODEL): cv.string,
                    vol.Required(CONF_DEVICE_ID): cv.string,
                }
            ),
        # Whether or not the section is initially collapsed (default = False)
        {"collapsed": False},
        )
    }
)

OPTIONS_SCHEMA = vol.Schema(
    {
    #    vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): cv.Number,
        vol.Required("sonnen_debug", default=False): bool
    }
)

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

SENSOR_TIMESTAMP: dict[tuple[Units, bool], SensorEntityDescription] = {
    (Units.NONE, False): SensorEntityDescription(
        key=f"{Units.NONE}_{False}",
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
}
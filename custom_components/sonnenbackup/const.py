"""Constants for the sonnenbackup integration."""

import voluptuous as vol
#from collections import namedtuple
from logging import Logger, getLogger

import homeassistant.helpers.config_validation as cv
#from homeassistant.data_entry_flow import section
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

from custom_components.sonnenbackup.units import Units

DOMAIN = "sonnenbackup"
MANUFACTURER = "Sonnen"
ATTRIBUTION = "Data provided by sonnen_api_v2 package"
DEFAULT_SCAN_INTERVAL = 10
MIN_SCAN_INTERVAL = 3
MAX_SCAN_INTERVAL = 120

ATTR_SONNEN_DEBUG = "sonnenbackup_debug"
DEFAULT_PORT = 80
MIN_PORT = 1
MAX_PORT = 49151 # below ephemeral range

LOGGER: Logger = getLogger(__package__)

PLATFORMS: list[Platform] = [Platform.SENSOR]

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_IP_ADDRESS): cv.string,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): cv.port,
        vol.Required(CONF_API_TOKEN): cv.string,
        # "details": section(
        #     vol.Schema(
        #         {
        vol.Required(CONF_MODEL): cv.string,
        vol.Required(CONF_DEVICE_ID): cv.string,
                # }
            # ),
        # Whether or not the section is initially collapsed (default = False)
        # {"collapsed": False},
        # )
    }
) #: cv.config_entry_only_config_schema

OPTIONS_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_SCAN_INTERVAL,
                     vol.Clamp(min=MIN_SCAN_INTERVAL, max=MAX_SCAN_INTERVAL),
                     default=DEFAULT_SCAN_INTERVAL,
                    ): int #,
#        vol.Required("sonnenbackup_debug", default=False): cv.boolean
    }
)

SENSOR_GROUP_UNITS = 'UNITS'
SENSOR_GROUP_TIMESTAMP = 'TIMESTAMP'
SENSOR_GROUP_ENUM = 'ENUM'

SENSOR_DESCRIPTIONS: dict[str, dict[tuple[Units, bool], SensorEntityDescription]] = {
    SENSOR_GROUP_UNITS: {
        (Units.C, False): SensorEntityDescription(
            key=f"{Units.C}_{False}",
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            suggested_display_precision = 1,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        (Units.KWH, False): SensorEntityDescription(
            key=f"{Units.KWH}_{False}",
            device_class=SensorDeviceClass.ENERGY_STORAGE,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision = 2,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        (Units.KWH, True): SensorEntityDescription(
            key=f"{Units.KWH}_{True}",
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision = 2,
            state_class=SensorStateClass.TOTAL,
        ),
        (Units.WH, False): SensorEntityDescription(
            key=f"{Units.WH}_{False}",
            device_class=SensorDeviceClass.ENERGY_STORAGE,
            native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
            suggested_display_precision = 1,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        (Units.WH, True): SensorEntityDescription(
            key=f"{Units.WH}_{True}",
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
            suggested_display_precision = 1,
            state_class=SensorStateClass.TOTAL,
        ),
        (Units.V, False): SensorEntityDescription(
            key=f"{Units.V}_{False}",
            device_class=SensorDeviceClass.VOLTAGE,
            native_unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision = 1,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        (Units.A, False): SensorEntityDescription(
            key=f"{Units.A}_{False}",
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision = 1,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        (Units.W, False): SensorEntityDescription(
            key=f"{Units.W}_{False}",
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision = 0,
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
    },
#SENSOR_TIMESTAMP: dict[tuple[Units, bool], SensorEntityDescription] = {
    SENSOR_GROUP_TIMESTAMP: {
        (Units.NONE, False): SensorEntityDescription(
            key=f"{Units.NONE}_{False}",
            device_class=SensorDeviceClass.TIMESTAMP,
        ),
    },
#SENSOR_ENUM: dict[tuple[Units, bool], SensorEntityDescription] = {
    SENSOR_GROUP_ENUM: {
        (Units.NONE, False): SensorEntityDescription(
            key=f"{Units.NONE}_{False}",
            device_class=SensorDeviceClass.ENUM, # all non-boolean enumerated types
            options=[] # overriden when sensor created
        ),
        (Units.NONE, True): SensorEntityDescription(
            key=f"{Units.NONE}_{True}",
            device_class=SensorDeviceClass.ENUM,
            options=[False,True] # special boolean description
        ),
    }
}
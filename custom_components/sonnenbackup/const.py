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
    Platform,
    CONF_IP_ADDRESS,
    CONF_API_TOKEN,
    CONF_PORT,
    CONF_MODEL,
    CONF_DEVICE_ID,
    CONF_SCAN_INTERVAL,
)

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

"""Constants for the sonnenbackup integration."""
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.data_entry_flow import section

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
DEFAULT_PORT = '80'

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
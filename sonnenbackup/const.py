"""Constants for the sonnen backup batterie integration."""
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
)
DOMAIN = "sonnenbackup"
MANUFACTURER = "Sonnen GmbH"
DEFAULT_SCAN_INTERVAL = 15
ATTR_SONNEN_DEBUG = "sonnenbackup_debug"
DEFAULT_PORT = '80'

PLATFORMS: list[Platform] = [Platform.SENSOR]

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_IP_ADDRESS): cv.string,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): cv.string,
        vol.Required(CONF_API_TOKEN): cv.string,
        vol.Required(CONF_MODEL): cv.string,
        vol.Required(CONF_DEVICE_ID): cv.string,
        "options": section(
            vol.Schema(
                {
                    vol.Required("SCAN_INTERVAL", default=DEFAULT_SCAN_INTERVAL): int,
                    vol.Required("SONNEN_DEBUG", default=False): bool,
                }
            ),
        # Whether or not the section is initially collapsed (default = False)
        {"collapsed": False},
        )
    }
)

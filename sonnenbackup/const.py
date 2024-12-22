"""Constants for the sonnen batterie integration."""

DOMAIN = "sonnenbackup"

MANUFACTURER = "Sonnen GmbH"

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_IP_ADDRESS): cv.string,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): cv.string,
        vol.Required(CONF_API_TOKEN): cv.string,
        vol.Optional(CONF_API_VERSION, default=DEFAULT_API_VERSION): cv.string,
        vol.Required(CONF_MODEL): cv.string,
        vol.Required(CONF_DEVICE_ID): cv.string,
    }
)


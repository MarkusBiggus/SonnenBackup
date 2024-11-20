"""Constants for the sonnen integration."""

from sonnen_api_v2.sonnen import BatterieResponse # InverterResponse

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator


class SonnenDataUpdateCoordinator(DataUpdateCoordinator[BatterieResponse]):
    """DataUpdateCoordinator for sonnen."""

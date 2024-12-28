"""Coordinator for the sonnenbackup integration."""

from sonnen_api_v2.sonnen import BatterieResponse

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

class SonnenBackupUpdateCoordinator(DataUpdateCoordinator[BatterieResponse]):
    """DataUpdateCoordinator for sonnenbackup."""
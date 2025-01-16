"""Coordinator for the sonnenbackup integration."""

from dataclasses import dataclass
from datetime import datetime
from sonnen_api_v2 import BatterieBackup, BatterieResponse

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator


class SonnenBackupUpdateCoordinator(DataUpdateCoordinator[BatterieResponse]):
    """DataUpdateCoordinator for sonnenbackup."""

@dataclass(slots=True)
class SonnenBackupAPI:
    """SonnenBackup Batterie API context."""

    _attr_icon = "mdi:battery-outline"

    api: BatterieBackup
    coordinator: SonnenBackupUpdateCoordinator
    serial_number: str
    model: str
    version: str
    last_updated: datetime
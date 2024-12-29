"""Coordinator for the sonnenbackup integration."""

from dataclasses import dataclass

from sonnen_api_v2 import BatterieBackup, BatterieResponse

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator


class SonnenBackupUpdateCoordinator(DataUpdateCoordinator[BatterieResponse]):
    """DataUpdateCoordinator for sonnenbackup."""

@dataclass(slots=True)
class SonnenBackupAPI:
    """SonnenBackup Batterie API context."""

    api: BatterieBackup
    coordinator: SonnenBackupUpdateCoordinator
    serial_number: str

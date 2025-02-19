"""Coordinator for the sonnenbackup integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict
from datetime import datetime
import logging

from sonnen_api_v2 import BatterieBackup, BatterieResponse

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
# from .const import (
#     LOGGER,
# )


#@dataclass(slots=True)
class BatterieData:
    """Poll data for the sonnenbackup integration.
        extended by updatecorordinator.
    """

#    charge: float
#    site_master: SiteMasterResponse
    meters: Dict[str, Any] # from BatterieSensors.map_response
#    grid_services_active: bool
#    grid_status: str
#    backup_reserve: float | None
#    batteries: dict[str, BatterieResponse]

#class SonnenBackupUpdateCoordinator(DataUpdateCoordinator[BatterieResponse]):
class SonnenBackupUpdateCoordinator(DataUpdateCoordinator[BatterieData]):
    """DataUpdateCoordinator for sonnenbackup."""

    def __init__(self,
        hass: HomeAssistant,
        logger: logging.Logger,
        **kwargs
    ) -> None:
        """Initialize SonnenBackupUpdateCoordinator Entity."""

        logger.info('Setup SonnenBackupUpdateCoordinator entity')
        super().__init__(hass, logger, **kwargs)


#@dataclass(slots=True)
class SonnenBackupRTData:
    """SonnenBackup Batterie runtime data.
        extended by config_entry.
    """

    _attr_icon = "mdi:battery-outline"

    api: BatterieBackup
    coordinator: SonnenBackupUpdateCoordinator
    serial_number: str
    model: str
    version: str
    last_updated: datetime

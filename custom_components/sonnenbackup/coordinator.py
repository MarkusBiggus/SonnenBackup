"""Coordinator for sonnenbackup integration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import logging

from sonnen_api_v2 import BatterieBackup, BatterieResponse

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .const import (
    LOGGER,
)

class SonnenBackupUpdateCoordinator(DataUpdateCoordinator[BatterieResponse]):
    """DataUpdateCoordinator for sonnenbackup."""

    def __init__(self,
        hass: HomeAssistant,
        logger: logging.Logger,
        **kwargs
    ) -> None:
        """Initialize SonnenBackupUpdateCoordinator Entity."""

        LOGGER.info('Setup SonnenBackupUpdateCoordinator entity')
        super().__init__(hass, logger, **kwargs)



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
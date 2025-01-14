"""pytest tests/test_batterieresponse.py -s -v -x

    Async update called from an async method to
    get BatterieResponse as used by HA component.
"""
import datetime
import os
import sys
import logging
import pytest
from freezegun import freeze_time

from sonnen_api_v2 import Batterie, BatterieResponse, BatterieBackup
from .mock_sonnenbatterie_v2_charging import __mock_configurations

from .battery_charging_asyncio import fixture_battery_charging

LOGGER_NAME = None # "sonnenapiv2" #

logging.getLogger("BatterieResponse").setLevel(logging.WARNING)

if LOGGER_NAME is not None:
    filename=f'/tests/logs/{LOGGER_NAME}.log'
    logging.basicConfig(filename=filename, level=logging.DEBUG)
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(LOGGER_NAME)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    # create file handler which logs debug messages
    fh = logging.FileHandler(filename=filename, mode='a')
    fh.setLevel(logging.DEBUG)
    # console handler display logs messages to console
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.info ('Response for HA mock data tests')


@pytest.mark.asyncio
@pytest.mark.usefixtures("battery_charging")
@freeze_time("20-11-2023 17:00:00")
async def test_batterieresponse(battery_charging: Batterie) -> None:
    """BatterieBackup Response using mock data."""

    _batterie = BatterieBackup('fakeToken', 'fakeHost')

    response = await _batterie.refresh_response()

    #print(f'response: {response}')

    assert isinstance(response, BatterieResponse) is True
    assert response == BatterieResponse(
        version='1.14.5',
        last_updated=datetime.datetime(2023, 11, 20, 17, 0),
        sensor_values={}
    )

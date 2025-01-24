"""pytest tests/test_batterieresponse.py -s -v -x
1. Async update called from an async method.
"""
import datetime
import os
import sys
import logging

#for tests only
import pytest
from freezegun import freeze_time
import tzlocal

from sonnen_api_v2 import Batterie, BatterieResponse, BatterieBackup

from .battery_charging_asyncio import fixture_battery_charging

LOGGER_NAME = None # "sonnenapiv2" #

logging.getLogger("batterieResponse").setLevel(logging.WARNING)

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
        last_updated=datetime.datetime(2023, 11, 20, 17, 0, tzinfo=tzlocal.get_localzone()),
        sensor_values={}
    )

    assert _batterie.get_sensor_value('installed_capacity') == 20000
    assert _batterie.get_sensor_value('seconds_since_full') == 3720
    since_full = datetime.timedelta(seconds=3720)

    print(f'since full: {since_full.strftime("%D %H:%M:%S")}')
    assert _batterie.get_sensor_value('time_since_full') == since_full

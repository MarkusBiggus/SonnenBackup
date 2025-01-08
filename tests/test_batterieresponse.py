"""pytest tests/test_batterieresponse.py -s -v -x
1. Async update called from an async method.
"""
import datetime
import os
import sys
import logging
import urllib3

#for tests only
import pytest
from freezegun import freeze_time
from unittest.mock import patch

from sonnen_api_v2 import Batterie, BatterieBackup, BatterieResponse, BatterieAuthError, BatterieHTTPError, BatterieError

from .battery_charging_asyncio import fixture_battery_charging
from .mock_battery_responses import (
    __battery_configurations_auth200,
    __battery_configurations_auth401,
    __battery_configurations_auth500,
)
from .mock_sonnenbatterie_v2_charging import __mock_configurations

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
@patch.object(urllib3.HTTPConnectionPool, 'urlopen', __battery_configurations_auth200)
async def test_batterieresponse_works(battery_charging: Batterie) -> None:
    """Batterie Response using mock data"""

    _batterie = BatterieBackup('fakeToken', 'fakeHost')

    response = await _batterie.validate_token()

    assert isinstance(response, BatterieResponse) is True
    assert response == BatterieResponse(
        version='1.14.5',
        last_updated=datetime.datetime(2023, 11, 20, 17, 0),
        configurations=__mock_configurations()
    )

    response = await _batterie.refresh_response()

    #print(f'response: {response}')

    assert isinstance(response, BatterieResponse) is True
    assert response == BatterieResponse(
        version='1.14.5',
        last_updated=datetime.datetime(2023, 11, 20, 17, 0),
        configurations=__mock_configurations()
    )

    sensor_value = _batterie.get_sensor_value('configuration_de_software')
    assert sensor_value == '1.14.5'


async def __mock_async_validate_token(self):
    """Mock validation failed."""
    return False

@pytest.mark.asyncio
@patch.object(Batterie, 'async_validate_token', __mock_async_validate_token)
async def test_batterieresponse_AuthError(battery_charging: Batterie) -> None:
    """Batterie Response using mock coroutine"""

    _batterie = BatterieBackup('fakeToken', 'fakeHost')

    with pytest.raises(BatterieAuthError, match='BatterieBackup: Error validating API token!'):
        await _batterie.validate_token()

@pytest.mark.asyncio
@pytest.mark.usefixtures("battery_charging")
@patch.object(urllib3.HTTPConnectionPool, 'urlopen', __battery_configurations_auth401)
async def test_batterieresponse_AuthError401(battery_charging: Batterie) -> None:
    """Batterie 401 Response using mock data"""

    _batterie = BatterieBackup('fakeToken', 'fakeHost')

    with pytest.raises(BatterieAuthError, match='Invalid token "fakeToken" status: 401'):
        await _batterie.validate_token()


async def __mock_async_update(self):
    """Mock update failed."""
    return False

@pytest.mark.asyncio
@pytest.mark.usefixtures("battery_charging")
@freeze_time("20-11-2023 17:00:00")
@patch.object(urllib3.HTTPConnectionPool, 'urlopen', __battery_configurations_auth200)
@patch.object(Batterie, 'async_update', __mock_async_update)
async def test_batterieresponse_BatterieError(battery_charging: Batterie) -> None:
    """Batterie Response using mock data"""

    _batterie = BatterieBackup('fakeToken', 'fakeHost')

    response = await _batterie.validate_token()

    assert isinstance(response, BatterieResponse) is True
    assert response == BatterieResponse(
        version='1.14.5',
        last_updated=datetime.datetime(2023, 11, 20, 17, 0),
        configurations=__mock_configurations()
    )

    with pytest.raises(BatterieError, match='BatterieBackup: Error updating batterie data!'):
        await _batterie.refresh_response()


@pytest.mark.asyncio
@pytest.mark.usefixtures("battery_charging")
@patch.object(urllib3.HTTPConnectionPool, 'urlopen', __battery_configurations_auth500)
async def test_batterieresponse_BatterieHTTPError(battery_charging: Batterie) -> None:
    """Batterie 500 Response using mock data"""

    _batterie = BatterieBackup('fakeToken', 'fakeHost')

    with pytest.raises(BatterieHTTPError, match='HTTP Error fetching endpoint "http://fakeHost:80/api/v2/configurations" status: 500'):
        await _batterie.validate_token()

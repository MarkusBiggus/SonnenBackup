"""pytest tests/test_batterieresponse.py -s -v -x -k test_batterieoffgridresponse
1. Async update called from an async method.
"""
import datetime
import os
import sys
import logging

#for tests only
import pytest
from freezegun import freeze_time
from freezegun.api import FakeDatetime
import tzlocal

from sonnen_api_v2 import Batterie, BatterieResponse, BatterieBackup

from custom_components.sonnenbackup.utils import strfdelta
from .battery_charging_asyncio import fixture_battery_charging
#from .battery_discharging_reserve_asyncio import fixture_battery_discharging_reserve
from .battery_discharging_offgrid_asyncio import fixture_battery_discharging_offgrid

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
    """BatterieBackup Response charging using mock data."""

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

#    print(f'since full: {strfdelta(since_full)}')
    assert _batterie.get_sensor_value('time_since_full') == since_full
    assert strfdelta(since_full) == '0d 01:02:00'

    assert _batterie.get_sensor_value('microgrid_enabled') is False
    assert _batterie.get_sensor_value('mg_minimum_soc_reached') is False
    assert _batterie.get_sensor_value('dc_minimum_rsoc_reached') is False

    assert _batterie.get_sensor_value('interval_to_fully_charged') == "0d 00:00:00"

@pytest.mark.asyncio
@pytest.mark.usefixtures("battery_discharging")
@freeze_time("20-11-2023 17:00:00")
async def test_batteriedischargeresponse(battery_discharging: Batterie) -> None:
    """BatterieBackup Response discharging using mock data."""

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
    assert _batterie.get_sensor_value('seconds_since_full') == 9574
    since_full = datetime.timedelta(seconds=9574)

#    print(f'since full: {strfdelta(since_full)}')
    assert _batterie.get_sensor_value('time_since_full') == since_full
    assert strfdelta(since_full) == '0d 02:39:34'

    assert _batterie.get_sensor_value('microgrid_enabled') is False
    assert _batterie.get_sensor_value('mg_minimum_soc_reached') is False
    assert _batterie.get_sensor_value('dc_minimum_rsoc_reached') is False

#    assert _batterie.get_sensor_value('interval_to_fully_discharged') == "0d 00:00:00"
#    assert _batterie.get_sensor_value('interval_to_reserve') == "0d 00:00:00"
    assert _batterie.get_sensor_value('time_to_fully_discharged') == datetime.timedelta(seconds=6060)
    assert _batterie.get_sensor_value('time_to_reserve') is None

@pytest.mark.asyncio
@pytest.mark.usefixtures("battery_discharging_offgrid")
@freeze_time("20-11-2023 17:00:00")
async def test_batterieoffgridresponse(battery_discharging_offgrid: Batterie) -> None:
    """BatterieBackup Response OffGrid using mock data."""

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
    assert _batterie.get_sensor_value('seconds_since_full') == 9574
    since_full = datetime.timedelta(seconds=9574)

#    print(f'since full: {strfdelta(since_full)}')
    assert _batterie.get_sensor_value('time_since_full') == since_full
    assert strfdelta(since_full) == '0d 02:39:34'

    assert _batterie.get_sensor_value('microgrid_enabled') is True
    assert _batterie.get_sensor_value('mg_minimum_soc_reached') is False
    assert _batterie.get_sensor_value('dc_minimum_rsoc_reached') is False
    assert _batterie.get_sensor_value('last_time_full') == datetime.datetime(2023, 11, 20, 14, 21, 16, tzinfo=tzlocal.get_localzone())

#    assert _batterie.get_sensor_value('interval_to_fully_discharged') == "0d 00:00:00"
#    assert _batterie.get_sensor_value('interval_to_reserve') == "0d 00:00:00"
    assert _batterie.get_sensor_value('time_to_fully_discharged') == datetime.timedelta(seconds=6060)
    assert _batterie.get_sensor_value('time_to_reserve') is None

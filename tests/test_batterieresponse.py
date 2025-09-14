"""pytest tests/test_batterieresponse.py -s -v -x -k test_batterieoffgridresponse
1. Async update called from an async method.

    These tests ensure the underlying sonnen_api_v2 module is installed
    and working correctly for sonnenbackup integration.
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
from .battery_discharging_asyncio import fixture_battery_discharging
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
@freeze_time("20-11-2023 17:00:00.543210")
async def test_batteriechargeresponse(battery_charging: Batterie) -> None:
    """BatterieBackup Response charging using mock data.
        Charging above backup reserve capacity.
    """

    _batterie = BatterieBackup('fakeToken', 'fakeHost')

    response:BatterieResponse = await _batterie.refresh_response()

    #print(f'response: {response}')

    # batterie firmware 1.18.x
    assert battery_charging.led_state == "Pulsing White 100%"
    assert battery_charging.led_state_text == "Normal Operation."
    assert battery_charging.led_status == "0x01 - ONGRID_READY"

    assert isinstance(response, BatterieResponse) is True
    assert response == BatterieResponse(
        version='0.5.15',
        last_updated=datetime.datetime(2023, 11, 20, 17, 0, 0, 543210, tzinfo=tzlocal.get_localzone()),
        sensor_values={},
        package_build = '48'
    )

    assert response.version == '0.5.15'
    assert response.package_build == '48'
    assert _batterie.get_sensor_value('configuration_de_software') == '1.14.5'
    assert _batterie.get_sensor_value('installed_capacity') == 20000
    assert _batterie.get_sensor_value('seconds_since_full') == 3720
    since_full = datetime.timedelta(seconds=3720)

#    print(f'since full: {strfdelta(since_full)}')
    assert _batterie.get_sensor_value('time_since_full') == since_full
    assert strfdelta(since_full) == '0d 01:02:00'

    assert _batterie.get_sensor_value('microgrid_enabled') is False
    assert _batterie.get_sensor_value('mg_minimum_soc_reached') is False
    assert _batterie.get_sensor_value('dc_minimum_rsoc_reached') is False

    assert _batterie.get_sensor_value('configuration_em_reenable_microgrid') is True
    assert _batterie.get_sensor_value('configuration_blackstart_time1') == "08:00"
    assert _batterie.get_sensor_value('configuration_blackstart_time2') == "09:05"
    assert _batterie.get_sensor_value('configuration_blackstart_time3') == "10:10"

#    assert _batterie.get_sensor_value('interval_to_fully_charged') == "0d 00:00:00"
    assert _batterie.get_sensor_value('time_to_fully_charged') == datetime.timedelta(seconds=6412)
    assert _batterie.get_sensor_value('time_to_reserve') is None
    assert _batterie.get_sensor_value('capacity_until_reserve') == 12314.1
    assert _batterie.get_sensor_value('capacity_to_reserve') is None

@pytest.mark.asyncio
@pytest.mark.usefixtures("battery_discharging")
@freeze_time("20-11-2023 17:00:00.543210")
async def test_batteriedischargeresponse(battery_discharging: Batterie) -> None:
    """BatterieBackup Response discharging using mock data.
        Discharging above backup reserve capacity.
    """

    _batterie = BatterieBackup('fakeToken', 'fakeHost')

    response = await _batterie.refresh_response()

    #print(f'response: {response}')

    assert isinstance(response, BatterieResponse) is True
    assert response == BatterieResponse(
        version='0.5.15',
        last_updated=datetime.datetime(2023, 11, 20, 17, 0, 0, 543210, tzinfo=tzlocal.get_localzone()),
        sensor_values={},
        package_build = '48'
    )

    assert _batterie.get_sensor_value('installed_capacity') == 20000
    assert _batterie.get_sensor_value('seconds_since_full') == 574
    since_full = datetime.timedelta(seconds=574)

#    print(f'since full: {strfdelta(since_full)}')
    assert _batterie.get_sensor_value('time_since_full') == since_full
    assert strfdelta(since_full) == '0d 00:09:34'

    assert _batterie.get_sensor_value('microgrid_enabled') is False
    assert _batterie.get_sensor_value('mg_minimum_soc_reached') is False
    assert _batterie.get_sensor_value('dc_minimum_rsoc_reached') is False

#    assert _batterie.get_sensor_value('interval_to_fully_discharged') == "0d 00:00:00"
#    assert _batterie.get_sensor_value('interval_to_reserve') == "0d 00:00:00"
    assert _batterie.get_sensor_value('time_until_fully_discharged') == datetime.timedelta(seconds=37661)
    assert _batterie.get_sensor_value('time_to_reserve') ==  datetime.timedelta(seconds=28362)
    assert _batterie.get_sensor_value('capacity_until_reserve') == 12314.1
    assert _batterie.get_sensor_value('capacity_to_reserve') is None


@pytest.mark.asyncio
@pytest.mark.usefixtures("battery_discharging_offgrid")
@freeze_time("20-11-2023 17:00:00.543210")
async def test_batterieoffgridresponse(battery_discharging_offgrid: Batterie) -> None:
    """BatterieBackup Response OffGrid using mock data.
        Discharging below backup reserve capacity.
    """

    _batterie = BatterieBackup('fakeToken', 'fakeHost')

    response = await _batterie.refresh_response()

    #print(f'response: {response}')

    assert isinstance(response, BatterieResponse) is True
    assert response == BatterieResponse(
        version='0.5.15',
        last_updated=datetime.datetime(2023, 11, 20, 17, 0, 0, 543210, tzinfo=tzlocal.get_localzone()),
        sensor_values={},
        package_build = '48'
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
    assert _batterie.get_sensor_value('last_time_full') == FakeDatetime(2023, 11, 20, 14, 21, 25, tzinfo=tzlocal.get_localzone())

#    assert _batterie.get_sensor_value('interval_to_fully_discharged') == "0d 00:00:00"
#    assert _batterie.get_sensor_value('interval_to_reserve') == "0d 00:00:00"
    assert _batterie.get_sensor_value('time_until_fully_discharged') == datetime.timedelta(seconds=6060)
    assert _batterie.get_sensor_value('time_to_reserve') is None
    assert _batterie.get_sensor_value('capacity_until_reserve') is None
    assert _batterie.get_sensor_value('capacity_to_reserve') == 1615.0

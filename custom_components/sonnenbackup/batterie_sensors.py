#from abc import abstractmethod
from typing import Any, Callable, Dict, Generator, Optional, Tuple, Union, Unpack
from datetime import datetime

import voluptuous as vol
import logging

from sonnen_api_v2 import BatterieBackup

from .utils import PackerBuilderResult
from .units import Measurement, Units, SensorUnit
from .const import (
    SENSOR_GROUP_UNITS,
    # SENSOR_GROUP_TIMESTAMP,
    # SENSOR_GROUP_ENUM,
    )


ProcessorTuple = Tuple[Callable[[Any], Any], ...]
SensorIndexSpec = Union[int, PackerBuilderResult]
ResponseDecoder = Dict[
    str,
    Tuple[SensorIndexSpec, SensorUnit, Unpack[ProcessorTuple]],
]
_LOGGER = logging.getLogger(__name__)

class BatterieSensors:
    """Base functions for batterie model sensor maps"""


    # pylint: enable=C0301
    _schema = vol.Schema({})  # type: vol.Schema

    def __init__(self, batterieAPI:BatterieBackup):
        """Base methods to process the sensor map defined
            by extensions to this class.
        """

        _LOGGER.info('Init BatterieSensors')
        self._response_decoder = type(self).response_decoder()
        # self.manufacturer = MANUFACTURER
        # self._serial_number = serial_number
        self.batterieAPI = batterieAPI
        self.decoded_map = self._decode_map()

    def map_response(self) -> Dict[str, Any]:
        """Called by sensor.async_setup_entry to prepare sensor definitions
            for a particular device model's set of sensors.
            There are 3 sensor groups:
            UNITS: All sensors that have units of measurment
            TIMESTAMPS: All timestamps
            ENUM: All that have a set of possible values. Bool is a special case here.
        """

        result = {}
        for sensor_name, (sensor_group, mapping) in self.decoded_map.items():
            (unit_or_measurement, alias, *_) = mapping

            result[alias] = self.batterieAPI.get_sensor_value(sensor_name)

            if sensor_group == SENSOR_GROUP_UNITS:
                for sensor_name, processor in self._postprocess_gen():
            #        print(f'{sensor_name}  processor: {processor}')
                    result[alias] = processor(result[alias])
                    _LOGGER.info(f'{alias}  processed result: {result[alias]}')



        return result

    def _decode_map(self) -> Dict[str, SensorIndexSpec]:
        """Decode the map creating a single list of mappings used
            to hydrate sensors.
        """
        sensors: Dict[str, SensorIndexSpec] = {}
        for sensor_group, sensor_map in self._response_decoder.items():
            for sensor_name, mapping in sensor_map.items():
                if sensor_name == "*skip*":
                    continue
                if len(mapping) == 1:
                    mapping = (mapping[0], sensor_name) # add alias
                sensors[sensor_name] = (sensor_group, mapping)
#                _LOGGER.info(f'decoded name: {sensor_name}  mapping:{mapping}')
        return sensors

    def _postprocess_gen(
        self,
    ) -> Generator[Tuple[str, Callable[[Any], Any]], None, None]:
        """
        Return map of functions to be applied to each UNITS sensor measurement.
        """

        for name, mapping in self._response_decoder.get(SENSOR_GROUP_UNITS).items():
            if len(mapping) > 2:
                (_, _, alias, *processors) = mapping
                alias = name if alias is None else alias
            else:
                continue
            for processor in processors:
                yield alias, processor


    @classmethod
    def sensor_map(cls) -> Dict[str, Tuple[int, Measurement]]:
        """
        Return sensor map to create BatterieSensorEntity in sensor.async_setup_entry.
        """
        _LOGGER.info('BatterieSensors sensor_map')

        iidx = 0
        idx_groups =[0,100,200] # max 100 per group
        sensors: Dict[str, Tuple[int, Measurement]] = {}
        for sensor_group, sensor_map in cls.response_decoder().items():
            idx = idx_groups[iidx]
            iidx += 1
            for sensor_name, mapping in sensor_map.items():
                if sensor_name == "*skip*":
                    continue
                option = None
                if len(mapping) == 1:
                    (unit_or_measurement, *_) = mapping
                    alias = sensor_name
                elif len(mapping) == 2:
                    (unit_or_measurement, alias, *_) = mapping
                else:
                    (unit_or_measurement, alias, option, *_) = mapping

                alias = sensor_name if alias is None else alias

                if sensor_group == SENSOR_GROUP_UNITS:
                    if isinstance(unit_or_measurement, Units):
                        unit = Measurement(unit_or_measurement)
                    elif issubclass(unit_or_measurement, SensorUnit):
                        unit = unit_or_measurement
                    else:
                        raise ValueError(f'{SENSOR_GROUP_UNITS} sensor {sensor_name} wrong type: {type(unit_or_measurement)}')
                else:
                    if type(option) is bool:
                        unit = Measurement(Units.NONE, is_monotonic = option)
                    else:
                        unit = Measurement(Units.NONE, False)
                sensors[alias] = (idx, unit, sensor_name, sensor_group, option)
                idx += 1
        return sensors

    # Post processors for UNITS measurements (still required??)
    @classmethod
    def _decode_operating_mode(cls, operating_mode) -> str:

        """Return name of Operating Mode."""

        return {
            1: "Manual",
            2: "Automatic",
            6: "Extension module",
            10: "Time of Use"
        }.get(operating_mode)

    @classmethod
    def _format_datetime(cls, TimeStamp: datetime = None) -> str:

        """Return datime formatted: d-m-Y H:M:S."""

        return TimeStamp.strftime("%d-%b-%Y %H:%M:%S") if TimeStamp is not None else 'na'

    @classmethod
    def _format_deltatime(cls, TimeStamp: datetime = None) -> str:

        """Return delta time formatted: D H:M:S."""

        return TimeStamp.strftime("%D %H:%M:%S") if TimeStamp is not None else 'na'

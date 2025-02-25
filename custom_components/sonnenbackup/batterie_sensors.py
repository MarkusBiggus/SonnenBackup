from __future__ import annotations

#from abc import abstractmethod
from typing import Any, Callable, Dict, Generator, Optional, Tuple, Union, Unpack
from datetime import timedelta, datetime

import voluptuous as vol
import logging

from sonnen_api_v2 import BatterieBackup

from .utils import strfdelta # , PackerBuilderResult
from .units import Measurement, Units, SensorUnit
from .const import (
    LOGGER,
    SENSOR_GROUP_UNITS,
    # SENSOR_GROUP_TIMESTAMP,
    SENSOR_GROUP_ENUM,
    )

SensorAlias = str | None
ProcessorTuple = Tuple[Callable[[Any], Any], ...]
#SensorMap = Union[int, PackerBuilder]
SensorMap = Tuple[SensorUnit, SensorAlias, Unpack[ProcessorTuple]]
ResponseDecoder = Dict[
    str, SensorMap
#    Tuple[SensorUnit,  Unpack[ProcessorTuple]],
]

class BatterieSensors:
    """Base functions for SonnenBatterie sensor maps.
        Sensor names are mapped to SonnenBattery properties.
    """

    # pylint: enable=C0301
    _schema = vol.Schema({})  # type: vol.Schema

    def __init__(self, batterieAPI:BatterieBackup):
        """Base methods to process the sensor map defined
            by extensions to this class.
        """

        LOGGER.info('Init BatterieSensors')
        self._response_decoder = type(self).response_decoder()
        # self.manufacturer = MANUFACTURER
        # self._serial_number = serial_number
        self.batterieAPI = batterieAPI
        self.decoded_map = self._decode_map()
#        LOGGER.info(f'Decoded_Map:{self.decoded_map}')

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
            (unit_or_measurement, alias, *processors) = mapping

            result[alias] = self.batterieAPI.get_sensor_value(sensor_name)
#            LOGGER.info(f'Sensor: {alias}  value:{result[alias]}')
            if sensor_group == SENSOR_GROUP_UNITS:
#                LOGGER.info(f'UNIT name: {sensor_name}  mapping:{mapping}')
                for alias, processor in self._postprocess_gen(mapping):
                    try:
                        result[alias] = getattr(self, processor)(result[alias])
        #                result[alias] = processor(result[alias])
#                        LOGGER.info(f'Sensor: {alias}  PROCESSED:{result[alias]}')
                    except (TypeError) as error:
                        LOGGER.error(f"map_response {sensor_name} failed: {repr(error)}")
                        raise ValueError(f'{sensor_group} sensor {sensor_name} bad processor: {processor}')
        return result

    def _decode_map(self) -> Dict[str, SensorMap]:
        """Decode the map creating a single list of mappings used
            to hydrate sensors.
        """

        LOGGER.info('BatterieSensors _decode_map')
        sensors: Dict[str, SensorMap] = {}
        for sensor_group, sensor_map in self._response_decoder.items():
            for sensor_name, mapping in sensor_map.items():
                if sensor_name[:5] == "*skip": #and sensor_name[-1:] == "*":
                    continue
                if len(mapping) == 1:
                    mapping = (mapping[0], sensor_name) # add alias as sensor_name
                elif len(mapping) > 2:
                    (_, alias, *processors) = mapping
                    if alias is None:
                        mapping = (mapping[0], sensor_name, mapping[2])
                sensors[sensor_name] = (sensor_group, mapping)
#                LOGGER.info(f'decoded name: {sensor_name}  mapping:{mapping}')
        return sensors

    def _postprocess_gen(
        self, mapping
    ) -> Generator[Tuple[str, Callable[[Any], Any]], None, None]:
        """
        Return map of functions to be applied to each UNITS sensor measurement.
        """

        if len(mapping) > 2:
            (_, alias, *processors) = mapping
        else:
            return
        for processor in processors:
    #        LOGGER.info(f'Alias: {alias}  processor: {processor}')
            yield alias, processor


    @classmethod
    def mapped_sensors(cls) -> Dict[str, Tuple[int, Measurement]]:
        """
        Return sensor map to create BatterieSensorEntity in sensor.async_setup_entry.
        """
        LOGGER.info('BatterieSensors mapped_sensors')

        iidx = 0
        idx_groups = [0,100,200] # max 100 per group
        sensors: Dict[str, Tuple[int, Measurement]] = {}
        for sensor_group, sensor_map in cls.response_decoder().items():
            idx = idx_groups[iidx]
            iidx += 1
            for sensor_name, mapping in sensor_map.items():
                if sensor_name[:5] == "*skip": #and sensor_name[-1:] == "*":
                    idx += 1
                    continue
                option = None
                if len(mapping) == 1:
                    (unit_or_measurement, *_) = mapping
                    alias = None
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
                elif sensor_group == SENSOR_GROUP_ENUM:
                    if type(option) is bool:
                        unit = Measurement(Units.NONE, is_monotonic = option)
                    else:
                        unit = Measurement(Units.NONE, False)
                sensors[alias] = (idx, unit, sensor_name, sensor_group, option)
                idx += 1
#        LOGGER.info(f'SENSOR_Map:{sensors}')
        return sensors

    # Post processors for UNITS measurements
    @classmethod
    def _decode_operatingmode(cls, operating_mode: int) -> str:
        """Return Operating Mode name."""

        return {
            1: "Manual",
            2: "Automatic",
            6: "Extension module",
            10: "Time of Use"
        }.get(operating_mode, f"unknown: {operating_mode}")

    @classmethod
    def _format_datetime(cls, TimeStamp: datetime = None) -> str:
        """Return datime formatted: d-m-Y H:M:S."""

        return TimeStamp.strftime("%d-%b-%Y %H:%M:%S") if TimeStamp is not None else 'na'

    @classmethod
    def _format_deltatime(cls, DeltaTimeStamp: int | timedelta | None) -> str:
        """Return delta time formatted: D H:M:S."""

        return strfdelta(DeltaTimeStamp) if DeltaTimeStamp is not None else 'na'

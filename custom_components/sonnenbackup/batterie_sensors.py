#from abc import abstractmethod
from typing import Any, Callable, Dict, Generator, Optional, Tuple, Union, Unpack
from datetime import datetime

import voluptuous as vol
from .const import MANUFACTURER

from sonnen_api_v2 import BatterieBackup
from sonnen_api_v2.utils import PackerBuilderResult
from sonnen_api_v2.units import Measurement, Units, SensorUnit


ProcessorTuple = Tuple[Callable[[Any], Any], ...]
SensorIndexSpec = Union[int, PackerBuilderResult]
ResponseDecoder = Dict[
    str,
    Tuple[SensorIndexSpec, SensorUnit, Unpack[ProcessorTuple]],
]

class BatterieSensors:
    """Base functions for batterie model sensor maps"""

    # @classmethod
    # def response_decoder(cls) -> ResponseDecoder:
    #     """
    #     Inverter implementations should override
    #     this to return a decoding map
    #     """
    #     raise NotImplementedError()

    # pylint: enable=C0301
    _schema = vol.Schema({})  # type: vol.Schema

    def __init__(self, batterieAPI:BatterieBackup): #, serial_number: str):
        """Base methods to process the sensor map defined
            by extensions to this class.
        """
        self._response_decoder = type(self).response_decoder()
        # self.manufacturer = MANUFACTURER
        # self._serial_number = serial_number
        self.batterieAPI = batterieAPI

    def _decode_map(self) -> Dict[str, SensorIndexSpec]:
        sensors: Dict[str, SensorIndexSpec] = {}
        for name, mapping in self._response_decoder.items():
            sensors[name] = mapping#[0]
    #        print(f'decoded name: {name}  mapping:{mapping}')
        return sensors

    def _postprocess_gen(
        self,
    ) -> Generator[Tuple[str, Callable[[Any], Any]], None, None]:
        """
        Return map of functions to be applied to each sensor value
        """
        for name, mapping in self._response_decoder.items():
            if len(mapping) > 3:
                (_, _, alias, *processors) = mapping
                alias = name if alias is None else alias
            else:
                continue
            for processor in processors:
                yield alias, processor

    def map_response(self) -> Dict[str, Any]:
        result = {}
        for sensor_name, decode_info in self._decode_map().items():
            # if isinstance(decode_info, (tuple, list)):
            #     indexes = decode_info[0]
            #     packer = decode_info[1]
            #     values = tuple(resp_data[i] for i in indexes)
            #     val = packer(*values)
            # else:
            #val = resp_data[decode_info]
            alias = decode_info[2] if len(decode_info) >2 and decode_info[2] is not None else sensor_name
    #        print(f'sensor name: {sensor_name}  alias: {alias}  decode_info: {decode_info}')
            result[alias] = self.batterieAPI.get_sensor_value(sensor_name)
    #        print(f'sensor name: {alias}  result: {result[alias]}')
        for sensor_name, processor in self._postprocess_gen():
    #        print(f'{sensor_name}  processor: {processor}')
            result[sensor_name] = processor(result[sensor_name])
    #        print(f'{sensor_name}  processed result: {result[sensor_name]}')
        return result

    @classmethod
    def sensor_map(cls) -> Dict[str, Tuple[int, Measurement]]:
        """
        Return sensor map
        Warning, HA depends on this
        """
        sensors: Dict[str, Tuple[int, Measurement]] = {}
        for name, mapping in cls.response_decoder().items():
            if len(mapping) > 2:
                (idx, unit_or_measurement, alias, *_) = mapping
                alias = name if alias is None else alias
            else:
                (idx, unit_or_measurement, *_) = mapping
                alias = name

            if isinstance(unit_or_measurement, Units):
                unit = Measurement(unit_or_measurement)
            else:
                unit = unit_or_measurement
            # if isinstance(idx, tuple):
            #     sensor_indexes = idx[0]
            #     first_sensor_index = sensor_indexes[0]
            #     idx = first_sensor_index
            sensors[name] = (idx, unit, alias)
        return sensors

    # @classmethod
    # def schema(cls) -> vol.Schema:
    #     """
    #     Return schema
    #     """
    #     return cls._schema

    @classmethod
    def _decode_operating_mode(cls, operating_mode) -> str:
        """Return name of Operating Mode"""
        return {
            1: "Manual",
            2: "Automatic",
            6: "Extension module",
            10: "Time of Use"
        }.get(operating_mode)

    @classmethod
    def _format_datetime(cls, TimeStamp: datetime = None) -> str:
        """Return datime formatted: d-m-Y H:M:S"""

        return TimeStamp.strftime("%d-%b-%Y %H:%M:%S") if TimeStamp is not None else 'na'


    # @property
    # def serial_number(self) -> str:
    # #    raise NotImplementedError  # pragma: no cover
    #     return self._serial_number

    # def __str__(self) -> str:
    #     return f"{self.__class__.__name__}::{self.http_client}"

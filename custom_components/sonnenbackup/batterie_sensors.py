#from abc import abstractmethod
from typing import Any, Callable, Dict, Generator, Optional, Tuple, Union, Unpack
from datetime import datetime

import voluptuous as vol
#from .const import MANUFACTURER

from sonnen_api_v2 import BatterieBackup

from .utils import PackerBuilderResult
from .units import Measurement, Units, Total, DailyTotal, BatteryCapacity, SensorUnit


ProcessorTuple = Tuple[Callable[[Any], Any], ...]
SensorIndexSpec = Union[int, PackerBuilderResult]
ResponseDecoder = Dict[
    str,
    Tuple[SensorIndexSpec, SensorUnit, Unpack[ProcessorTuple]],
]

class BatterieSensors:
    """Base functions for batterie model sensor maps"""


    # pylint: enable=C0301
    _schema = vol.Schema({})  # type: vol.Schema

    def __init__(self, batterieAPI:BatterieBackup):
        """Base methods to process the sensor map defined
            by extensions to this class.
        """

        self._response_decoder = type(self).response_decoder()
        # self.manufacturer = MANUFACTURER
        # self._serial_number = serial_number
        self.batterieAPI = batterieAPI
        self.decoded_map = self._decode_map() #None

    def map_response(self) -> Dict[str, Any]:
        """Called by sensor.async_setup_entry to prepare sensor definitions
            for a particular device model's set of sensors.
            There are 3 sensor groups:
            UNITS: All sensors that have units of measurment
            TIMESTAMPS: All timestamps
            ENUM: All that have a set of possible values. Bool is a special case here.
        """
#        if self.decoded_map is None:
#            self.decoded_map = self._decode_map()

        result = {}
        for sensor_name, (sensor_group, decode_info) in self.decoded_map.items():
            alias = decode_info[2] if len(decode_info) >2 and decode_info[2] is not None else sensor_name
    #        print(f'sensor name: {sensor_name}  alias: {alias}  decode_info: {decode_info}')
            result[alias] = self.batterieAPI.get_sensor_value(sensor_name)
    #        print(f'sensor name: {alias}  result: {result[alias]}')
            if sensor_group == 'UNITS':
                for sensor_name, processor in self._postprocess_gen():
            #        print(f'{sensor_name}  processor: {processor}')
                    result[alias] = processor(result[sensor_name])
            #        print(f'{sensor_name}  processed result: {result[sensor_name]}')

        return result

    def _decode_map(self) -> Dict[str, SensorIndexSpec]:
        """Decode the map creating a single list of mappings used
            to hydrate sensors.
        """
        sensors: Dict[str, SensorIndexSpec] = {}
        for sensor_group, sensor_map in self._response_decoder.items():
            for name, mapping in sensor_map.items():
                sensors[name] = (sensor_group, mapping)
        #        print(f'decoded name: {name}  mapping:{mapping}')
        return sensors

    def _postprocess_gen(
        self,
    ) -> Generator[Tuple[str, Callable[[Any], Any]], None, None]:
        """
        Return map of functions to be applied to each UNITS sensor measurement.
        """

        for name, mapping in self._response_decoder.get('UNITS').items():
            if len(mapping) > 3:
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

        sensors: Dict[str, Tuple[int, Measurement]] = {}
        for sensor_group, sensor_map in cls.response_decoder().items():
            for name, mapping in sensor_map.items():
                option = None
                if len(mapping) > 2:
                    if len(mapping) > 3:
                        (idx, unit_or_measurement, alias, option, *_) = mapping
                    else:
                        (idx, unit_or_measurement, alias, *_) = mapping
                    alias = name if alias is None else alias
                else:
                    (idx, unit_or_measurement, *_) = mapping
                    alias = name

                if sensor_group == 'UNITS':
    #                print(f'{unit_or_measurement}: type: {type(unit_or_measurement)}')
    #                print(f'mapping : {mapping}')
                    if isinstance(unit_or_measurement, Units):
                        unit = Measurement(unit_or_measurement)
                    elif issubclass(unit_or_measurement, SensorUnit):
    #                elif type(unit_or_measurement) in SensorUnit:
                #    elif type(unit_or_measurement) in fieldtypes:
            #        else: # Assumed valid!
                        unit = unit_or_measurement
                    else:
                        raise ValueError(f'UNITS sensor {name} wrong type: {type(unit_or_measurement)}')
                else:
                    if type(option) is bool:
                        unit = Measurement(Units.NONE, is_monotonic = option)
                    else:
                        unit = Measurement(Units.NONE, False)
                sensors[alias] = (idx, unit, name, sensor_group, option)
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

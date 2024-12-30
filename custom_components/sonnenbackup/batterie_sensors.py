#from abc import abstractmethod
from typing import Any, Dict, Optional, Tuple
from datetime import datetime

import voluptuous as vol
from .const import MANUFACTURER

from sonnen_api_v2 import utils
# from solax.inverter_http_client import InverterHttpClient, Method
# from solax.response_parser import InverterResponse, ResponseDecoder, ResponseParser
from sonnen_api_v2.units import Measurement, Units


# class InverterError(Exception):
#     """Indicates error communicating with inverter"""


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

#    def __init__(self, http_client: InverterHttpClient):
    def __init__(self, serial_number: str):
        """Base methods to process the sensor map defined
            by extensions to this class.
        """

        self.manufacturer = MANUFACTURER
        self._serial_number = serial_number

#        self.http_client = http_client

#        schema = type(self).schema()
#        response_decoder = type(self).response_decoder()
#        dongle_serial_number_getter = type(self).dongle_serial_number_getter
#        serial_number_getter = type(self).serial_number_getter
        # self.response_parser = ResponseParser(
        #     schema,
        #     response_decoder,
        #     dongle_serial_number_getter,
        #     serial_number_getter,
        # )

    # @classmethod
    # def _build(cls, host, port, pwd="", params_in_query=True):
    #     url = utils.to_url(host, port)
    #     http_client = InverterHttpClient(url=url, method=Method.POST, pwd=pwd)
    #     if params_in_query:
    #         http_client = http_client.with_default_query()
    #     else:
    #         http_client = http_client.with_default_data()

    #     return cls(http_client)

    # @classmethod
    # def build_all_variants(cls, host, port, pwd=""):
    #     versions = {
    #         cls._build(host, port, pwd, True),
    #         cls._build(host, port, pwd, False),
    #     }
    #     return versions

    # async def get_data(self) -> InverterResponse:
    #     try:
    #         data = await self.make_request()
    #     except aiohttp.ClientError as ex:
    #         msg = "Could not connect to inverter endpoint"
    #         raise InverterError(msg, str(self.__class__.__name__)) from ex
    #     except vol.Invalid as ex:
    #         msg = "Received malformed JSON from inverter"
    #         raise InverterError(msg, str(self.__class__.__name__)) from ex
    #     return data

    # async def make_request(self) -> InverterResponse:
    #     """
    #     Return instance of 'InverterResponse'
    #     Raise exception if unable to get data
    #     """
    #     raw_response = await self.http_client.request()
    #     return self.response_parser.handle_response(raw_response)

    @classmethod
    def sensor_map(cls) -> Dict[str, Tuple[int, Measurement]]:
        """
        Return sensor map
        Warning, HA depends on this
        """
        sensors: Dict[str, Tuple[int, Measurement]] = {}
        for name, mapping in cls.response_decoder().items():
            unit = Measurement(Units.NONE)

            (idx, unit_or_measurement, *_) = mapping

            if isinstance(unit_or_measurement, Units):
                unit = Measurement(unit_or_measurement)
            else:
                unit = unit_or_measurement
            if isinstance(idx, tuple):
                sensor_indexes = idx[0]
                first_sensor_index = sensor_indexes[0]
                idx = first_sensor_index
            sensors[name] = (idx, unit)
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

        return TimeStamp.strftime("%d-%b-%Y %H:%M:%S") if TimeStamp is not None else '*none*'


    @property
    def serial_number(self) -> str:
    #    raise NotImplementedError  # pragma: no cover
        return self._serial_number

    # def __str__(self) -> str:
    #     return f"{self.__class__.__name__}::{self.http_client}"

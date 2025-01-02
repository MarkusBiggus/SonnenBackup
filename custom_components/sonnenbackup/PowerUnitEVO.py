"""Sensor definitions for Sonnen Batterie model Power Unit EVO"""

from sonnen_api_v2.units import DailyTotal, Total, Units, BatteryCapacity
#from sonnen_api_v2.utils import div10, div100 #, pack_u16, to_signed, to_signed32, twoway_div10

from .batterie_sensors import BatterieSensors

class PowerUnitEVO(BatterieSensors):
    """Sonnen Power Unit EVO v1.14.x"""

    def __init__(self, *args, **kwargs):
        """At least 1 param expected for device serial_number:str"""
        super(PowerUnitEVO, self).__init__(*args, **kwargs)

    @classmethod
    def response_decoder(cls) -> dict:
        """sonnen_api_v2 properties used as sensor values"""

        return {
            "configuration_em_operatingmode": (0, Units.NONE, cls._decode_operating_mode),
            "configuration_em_usoc": (1, Units.PERCENT),
            "last_configurations": (2, Units.NONE, cls._format_datetime),
            "system_status": (3, Units.NONE),
            "system_status_timestamp": (4, Units.NONE, cls._format_datetime),
            "battery_activity_state": (5, Units.NONE),
            "fully_charged_at": (6, Units.NONE, cls._format_datetime),
            "fully_discharged_at": (7, Units.NONE, cls._format_datetime),
            "battery_cycle_count": (8, Units.NONE),
            "battery_full_charge_capacity_wh":(9, BatteryCapacity),
            "battery_remaining_capacity_wh":(10, BatteryCapacity),
            "capacity_until_reserve":(11, BatteryCapacity),
            "backup_reserve_at": (12, Units.NONE),
            "backup_buffer_capacity_wh":(13, BatteryCapacity),
            "kwh_consumed": (14, Units.KWH),
            "kwh_produced": (15, Units.KWH),
            # "Grid 1 Voltage": (0, Units.V, div10),
            # "Grid 2 Voltage": (1, Units.V, div10),
            # "Grid 3 Voltage": (2, Units.V, div10),
            # "Grid 1 Current": (3, Units.A, twoway_div10),
            # "Grid 2 Current": (4, Units.A, twoway_div10),
            # "Grid 3 Current": (5, Units.A, twoway_div10),
            # "Grid 1 Power": (6, Units.W, to_signed),
            # "Grid 2 Power": (7, Units.W, to_signed),
            # "Grid 3 Power": (8, Units.W, to_signed),
            # "PV1 Voltage": (9, Units.V, div10),
            # "PV2 Voltage": (10, Units.V, div10),
            # "PV3 Voltage": (11, Units.V, div10),
            # "PV1 Current": (12, Units.A, div10),
            # "PV2 Current": (13, Units.A, div10),
            # "PV3 Current": (14, Units.A, div10),
            # "PV1 Power": (15, Units.W),
            # "PV2 Power": (16, Units.W),
            # "PV3 Power": (17, Units.W),
            # "Grid 1 Frequency": (18, Units.HZ, div100),
            # "Grid 2 Frequency": (19, Units.HZ, div100),
            # "Grid 3 Frequency": (20, Units.HZ, div100),
            # "Total Yield": (pack_u16(22, 23), Total(Units.KWH), div10),
            # "Daily Yield": (24, DailyTotal(Units.KWH), div10),
            # "Feed-in Power ": (pack_u16(72, 73), Units.W, to_signed32),
            # "Total Feed-in Energy": (pack_u16(74, 75), Total(Units.KWH), div100),
            # "Total Consumption": (pack_u16(76, 77), Total(Units.KWH), div100),
        }

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

        """format: api.property : (index, Units, Alias, Formatter)
            Alias is only used when api.property name is unsuitable as a sensor name.
        """
        return {
            "configuration_em_operatingmode": (0, Units.NONE, "operatingmode", cls._decode_operating_mode),
            "configuration_em_usoc": (1, Units.PERCENT, "usoc"),
            "last_configurations": (2, Units.NONE, None, cls._format_datetime),
            "system_status": (3, Units.NONE),
            "system_status_timestamp": (4, Units.NONE, "status_timestamp", cls._format_datetime),
            "battery_activity_state": (5, Units.NONE, "activity_state"),
            "fully_charged_at": (6, Units.NONE, None, cls._format_datetime),
            "fully_discharged_at": (7, Units.NONE, None, cls._format_datetime),
            "battery_cycle_count": (8, Units.NONE),
            "battery_full_charge_capacity_wh":(9, BatteryCapacity, "full_charge_capacity"),
            "battery_remaining_capacity_wh":(10, BatteryCapacity, "remaining_capacity"),
            "capacity_until_reserve":(11, BatteryCapacity),
            "backup_reserve_at": (12, Units.NONE),
            "backup_buffer_capacity_wh":(13, BatteryCapacity, "backup_buffer_capacity"),
            "kwh_consumed": (14, Units.KWH),
            "kwh_produced": (15, Units.KWH),
            "consumption_average" : (16, Units.W),
            "status_frequency": (17, Units.HZ, "frequency"),
            "status_battery_charging": (18, Units.NONE, "charging"),
            "status_battery_discharging": (19, Units.NONE, "discharging"),
            # "Total Yield": (pack_u16(22, 23), Total(Units.KWH), div10),
            # "Daily Yield": (24, DailyTotal(Units.KWH), div10),
            # "Feed-in Power ": (pack_u16(72, 73), Units.W, to_signed32),
            # "Total Feed-in Energy": (pack_u16(74, 75), Total(Units.KWH), div100),
            # "Total Consumption": (pack_u16(76, 77), Total(Units.KWH), div100),
        }

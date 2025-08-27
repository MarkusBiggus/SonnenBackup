"""Sensor definitions for Sonnen Batterie model Power Unit EVO"""

from dataclasses import dataclass
from homeassistant.components.sensor import (
    SensorEntityDescription,
    # SensorDeviceClass,
    # SensorEntity,
    # SensorStateClass,
)
from homeassistant.helpers.typing import StateType

#from .utils import div10, div100 #, pack_u16, to_signed, to_signed32, twoway_div10

from .const import (
    SENSOR_GROUP_UNITS,
    SENSOR_GROUP_TIMESTAMP,
    SENSOR_GROUP_DELTATIME,
    SENSOR_GROUP_ENUM,
    )
from .units import Units, BatteryCapacity, TotalKWH #, DailyTotal, DailyTotalW, Total
from .batterie_sensors import BatterieSensors

class PowerUnitEVO(BatterieSensors):
    """Sonnen Power Unit EVO.
        Could be a differnce response_decoder for each model with varying sensors.
    """

    def __init__(self, *args, **kwargs):
        """At least 1 param expected for batterieAPI:BatterieBackup"""
        super(PowerUnitEVO, self).__init__(*args, **kwargs)

    @classmethod
    def response_decoder(cls) -> dict:
        """sonnen_api_v2 properties used as hass sensor values."""

        """format: api.property : (index, Units, Alias, Formatter)
            Alias is only used when api.property name is unsuitable as a sensor name.
            Assigned index is unique for each group - they become one list of sensors, eventually.
            Add new sensors only to the end of a group.
            Deleting will create new sensors for all after that point.
            Use *skipN* to preserve index sequence for a deleted sensor, or
            Replace inline to remove a sensor.
        """
        return {
            SENSOR_GROUP_UNITS: {
                "configuration_de_software": (Units.NONE, "firmware_version"),
                "led_state": (Units.NONE,),
                "system_status": (Units.NONE,),
                "battery_activity_state": (Units.NONE, "activity_state"),
                "battery_cycle_count": (Units.NONE,),
                "*skip*": ("deleted sensor: index is skipped", "replace later with a new sensor"),
                "installed_capacity": (BatteryCapacity,),
#                "full_charge_capacity": (BatteryCapacity,),
                "battery_full_charge_capacity_wh": (BatteryCapacity, "full_charge_capacity"),
#                "battery_usable_remaining_capacity_wh": (BatteryCapacity, "usable_capacity"),
                "usable_remaining_capacity_wh": (BatteryCapacity, "usable_capacity"),
#                "unusable_capacity_wh": (BatteryCapacity, "unusable_capacity"),
                "battery_unusable_capacity_wh": (BatteryCapacity, "unusable_capacity"),
                "battery_average_current": (Units.A,), # "mdi:flash-triangle-outline"
                "configuration_blackstart_time1": (Units.NONE, "blackstart_time1"),
                "configuration_blackstart_time2": (Units.NONE, "blackstart_time2"),
#                "battery_remaining_capacity_wh": (BatteryCapacity, "remaining_capacity"),
                "remaining_capacity_wh": (BatteryCapacity, "remaining_capacity"),
#                "status_remaining_capacity_wh": (BatteryCapacity, "remaining_capacity"),
                "capacity_until_reserve": (BatteryCapacity,),
                "backup_buffer_capacity_wh": (BatteryCapacity, "reserve_capacity"),
#                "status_usable_capacity_wh": (BatteryCapacity, "usable_remaining_capacity"),
                "configuration_blackstart_time3": (Units.NONE, "blackstart_time3"),
                "kwh_consumed": (TotalKWH,), #Total(Units.KWH)),
                "kwh_produced": (TotalKWH,), #Total(Units.KWH)),
                "consumption_average": (Units.W,), #DailyTotal(Units.W)),
                "status_frequency": (Units.HZ, "frequency"),
                "status_backup_buffer": (Units.PERCENT, "reserve_charge"),

#            """Latest data values seem to be adjusted to be consistent with related sensors"""
                # "battery_rsoc": (Units.PERCENT, "relative_state_of_charge"),
                # "battery_usoc": (Units.PERCENT, "usable_state_of_charge"),
                "r_soc": (Units.PERCENT, "relative_state_of_charge"),
                "u_soc": (Units.PERCENT, "usable_state_of_charge"),

#            """These consumption/production daily numbers seem to be meaningless"""
                "*skip9*": (Units.W, "consumption_daily"),# "consumption_total_w"
                "*skip0*": (Units.W, "production_daily"),# "production_total_w"
            #
                "consumption": (Units.W, "consumption_now"), # "mdi:meter-electric-outline"
                "production": (Units.W, "production_now"),
                "status_grid_export": (Units.W, "grid_export"),
                "status_grid_import": (Units.W, "grid_import"),
                "inverter_pac_total": (Units.W, "ongrid_pac"),
                "inverter_pac_microgrid": (Units.W, "offgrid_pac"),
                "battery_min_cell_temp": (Units.C, "min_battery_temp"),
                "battery_max_cell_temp": (Units.C, "max_battery_temp"), # "mdi:thermometer-alert"
                "state_bms": (Units.NONE,),
                "state_inverter": (Units.NONE,),
                "seconds_since_full": (Units.NONE,), #seconds_since_full
                "time_to_fully_charged": (Units.NONE,), #seconds_until_fully_charged
                "time_to_fully_discharged": (Units.NONE,), # seconds_until_fully_discharged
                "time_to_reserve": (Units.NONE,), # seconds_until_reserve
                "discharging": (Units.W, "discharge_power"),
                "charging": (Units.W, "charge_power"),
                "battery_dod_limit": (Units.PERCENT, "depth_of_discharge_limit"),
                "battery_module_dc_voltage": (Units.V, "module_dc_voltage"), # "mdi:current-ac"
                "time_since_full": (Units.NONE,),
                "led_state_text": (Units.NONE,),
                "battery_used_capacity_wh": (BatteryCapacity, "used_capacity"),
                "status_grid_feedin": (Units.W, "grid_feedin"), #"mdi:transmission-tower-import"
                "capacity_to_reserve": (BatteryCapacity,),
                "configuration_em_operatingmode": (Units.NONE, "operating_mode", "_decode_operatingmode"),
#       1082bytes         "dc_shutdown_reason": (Units.NONE,),
#       394bytes          "microgrid_status": (Units.NONE,),
            },

            SENSOR_GROUP_TIMESTAMP: {
                "system_status_timestamp": (Units.NONE, "status_timestamp"), # "mdi:battery-outline"
                "fully_charged_at": (Units.NONE,),
                "fully_discharged_at": (Units.NONE,),
                "backup_reserve_at": (Units.NONE, "reserve_at"),
                "last_time_full": (Units.NONE,),
                "last_updated": (Units.NONE,),
            },

            SENSOR_GROUP_ENUM: {
                "status_battery_charging": (Units.NONE, "charging", True),
                "status_battery_discharging": (Units.NONE, "discharging", True),
                "configuration_em_reenable_microgrid": (Units.NONE, "blackstart_enabled", True),
                "microgrid_enabled": (Units.NONE, None, True),
                "mg_minimum_soc_reached": (Units.NONE, 'microgrid_minimum_soc', True),
                "dc_minimum_rsoc_reached": (Units.NONE, 'dc_minimum_rsoc', True),
            },

            SENSOR_GROUP_DELTATIME: {
                "time_to_fully_charged": (Units.NONE, "interval_to_fully_charged", "_format_deltatime"), #seconds_until_fully_charged
                "time_to_fully_discharged": (Units.NONE, "interval_to_fully_discharged", "_format_deltatime"), # seconds_until_fully_discharged
                "time_to_reserve": (Units.NONE, "interval_to_reserve", "_format_deltatime"), # seconds_until_reserve
                "time_since_full": (Units.NONE, "interval_since_full", "_format_deltatime"), # seconds_since_full
            },
        }

@dataclass(frozen=True)
class SonnenBackupSensorEntityDescription(SensorEntityDescription):
    """Describes SonnenBackup sensor entity."""

    default_value: StateType | None = None
    invalid_when_falsy: bool = False
    response_key: str | None = None

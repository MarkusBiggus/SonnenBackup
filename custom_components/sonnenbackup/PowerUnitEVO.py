"""Sensor definitions for Sonnen Batterie model Power Unit EVO"""

from dataclasses import dataclass
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    EntityCategory,
    UnitOfApparentPower,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfReactivePower,
    UnitOfTemperature,
)
from homeassistant.helpers.typing import StateType

#from .utils import div10, div100 #, pack_u16, to_signed, to_signed32, twoway_div10

from .const import (
    SENSOR_GROUP_UNITS,
    SENSOR_GROUP_TIMESTAMP,
    SENSOR_GROUP_ENUM,
    )
from .units import Units, BatteryCapacity, DailyTotal, TotalKWH, DailyTotalW #Total
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
        """sonnen_api_v2 properties used as hass sensor values"""

        """format: api.property : (index, Units, Alias, Formatter)
            Alias is only used when api.property name is unsuitable as a sensor name.
            Assigned index is unique for each group - they become one list of sensors, eventually.
            Add new sensors only to the end of a group.
            Deleting will create new sensors for all after that point.
            Use *skip* to preserve index sequence for a deleted sensor, or
            Replace inline to remove a sensor.
        """
        return {
            SENSOR_GROUP_UNITS: {
                "configuration_de_software": (Units.NONE, "firmware_version"),
                "led_state": (Units.NONE,),
                "system_status": (Units.NONE,),
                "battery_activity_state": (Units.NONE, "sonnenbackup_state"),
                "battery_cycle_count": (Units.NONE,),
                "*skip*": ("deleted sensor: index is skipped", "replace later with a new sensor"),
                "installed_capacity": (BatteryCapacity,),
#                "full_charge_capacity": (BatteryCapacity,),
                "battery_full_charge_capacity_wh": (BatteryCapacity, "full_charge_capacity"),
#                "battery_usable_remaining_capacity_wh": (BatteryCapacity, "usable_capacity"),
                "usable_remaining_capacity_wh": (BatteryCapacity, "usable_capacity"),
#                "unusable_capacity_wh": (BatteryCapacity, "unusable_capacity"),
                "battery_unusable_capacity_wh": (BatteryCapacity, "unusable_capacity"),
                "battery_average_current": (Units.A,),
                "*skip1*": (BatteryCapacity, "battery_remaining_capacity"),
                "*skip2*": (BatteryCapacity, "unusable_capacity"),
#                "battery_remaining_capacity_wh": (BatteryCapacity, "remaining_capacity"),
                "remaining_capacity_wh": (BatteryCapacity, "remaining_capacity"),
#                "status_remaining_capacity_wh": (BatteryCapacity, "remaining_capacity"),
                "capacity_until_reserve": (BatteryCapacity,),
                "backup_buffer_capacity_wh": (BatteryCapacity, "reserve_capacity"),
#                "status_usable_capacity_wh": (BatteryCapacity, "usable_remaining_capacity"),
                "*skip4*": (BatteryCapacity, "usable_remaining_capacity"),
                "kwh_consumed": (TotalKWH,), #Total(Units.KWH)),
                "kwh_produced": (TotalKWH,), #Total(Units.KWH)),
                "consumption_average": (Units.W,), #DailyTotal(Units.W)),
                "status_frequency": (Units.HZ, "frequency"),
                "status_backup_buffer": (Units.PERCENT, "reserve_charge"),
                # "battery_rsoc": (Units.PERCENT, "relative_state_of_charge"),
                # "battery_usoc": (Units.PERCENT, "usable_state_of_charge"),
                "r_soc": (Units.PERCENT, "relative_state_of_charge"),
                "u_soc": (Units.PERCENT, "usable_state_of_charge"),

            """These consumption/production daily numbers seem to be meaningless"""
                "consumption_total_w": (Units.W, "consumption_daily"),
                "production_total_w": (Units.W, "production_daily"),
            #
                "consumption": (Units.W, "consumption_now"),
                "production": (Units.W, "production_now"),
                "status_grid_export": (Units.W, "grid_export"),
                "status_grid_import": (Units.W, "grid_import"),
                "inverter_pac_total": (Units.W, "ongrid_pac"),
                "inverter_pac_microgrid": (Units.W, "offgrid_pac"),
                "battery_min_cell_temp": (Units.C, "min_battery_temp"),
                "battery_max_cell_temp": (Units.C, "max_battery_temp"),
                "state_bms": (Units.NONE,),
                "state_inverter": (Units.NONE,),
                "*skip5*": (Units.NONE,), #seconds_since_full
                "*skip6*": (Units.NONE,), #seconds_until_fully_charged
                "*skip7*": (Units.NONE,), # seconds_until_fully_discharged
                "*skip8*": (Units.NONE,), # seconds_until_reserve
                "discharging": (Units.W, "discharge_power"),
                "charging": (Units.W, "charge_power"),
                "battery_dod_limit": (Units.PERCENT, "depth_of_discharge_limit"),
                "battery_module_dc_voltage": (Units.V, "module_dc_voltage"),
                "time_since_full": (Units.NONE,"interval_since_full", "_format_deltatime"),
                "led_state_text": (Units.NONE,),
                "battery_used_capacity_wh": (BatteryCapacity, "used_capacity"),
                "status_grid_feedin": (Units.W, "grid_feedin"),
                "capacity_to_reserve": (BatteryCapacity,),
                "configuration_em_operatingmode": (Units.NONE, "operating_mode", "_decode_operatingmode"),
#       1082bytes         "dc_shutdown_reason": (Units.NONE,),
#       394bytes          "microgrid_status": (Units.NONE,),

                # "Total Yield": (pack_u16(22, 23), Total(Units.KWH), div10),
                # "Daily Yield": (24, DailyTotal(Units.KWH), div10),
                # "Feed-in Power ": (pack_u16(72, 73), Units.W, to_signed32),
                # "Total Feed-in Energy": (pack_u16(74, 75), Total(Units.KWH), div100),
                # "Total Consumption": (pack_u16(76, 77), Total(Units.KWH), div100),
            },

            SENSOR_GROUP_TIMESTAMP: {
                "system_status_timestamp": (Units.NONE, "status_timestamp"),
                "fully_charged_at": (Units.NONE,),
                "fully_discharged_at": (Units.NONE,),
                "backup_reserve_at": (Units.NONE, "reserve_at"),
                "last_time_full": (Units.NONE,),
                "last_updated": (Units.NONE,),
            },

            SENSOR_GROUP_ENUM: {
                "status_battery_charging": (Units.NONE, "charging", True),
                "status_battery_discharging": (Units.NONE, "discharging", True),
                "*skip*": (Units.NONE, ), #"operating_mode", [1: "Manual",2: "Automatic",6: "Extension module",10: "Time of Use"]),
                "microgrid_enabled": (Units.NONE, None, True),
                "mg_minimum_soc_reached": (Units.NONE, 'microgrid_minimum_soc', True),
                "dc_minimum_rsoc_reached": (Units.NONE, 'dc_minimum_rsoc', True),
            },
        }

@dataclass(frozen=True)
class SonnenBackupSensorEntityDescription(SensorEntityDescription):
    """Describes SonnenBackup sensor entity."""

    default_value: StateType | None = None
    invalid_when_falsy: bool = False
    response_key: str | None = None
#    value_fn: Callable[[StateType], StateType] | None = None


# @classmethod
# def battery_sensors(cls) -> dict:
#     """sonnen_api_v2 properties used as sensor values"""

#     return BATTERY_ENTITY_DESCRIPTIONS


# BATTERY_ENTITY_DESCRIPTIONS: list[SonnenBackupSensorEntityDescription] = [
#     SonnenBackupSensorEntityDescription(
#         key="kwh_produced",
#         native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
#         device_class=SensorDeviceClass.ENERGY,
#         state_class=SensorStateClass.TOTAL_INCREASING,
#     ),
#     SonnenBackupSensorEntityDescription(
#         key="kwh_consumed",
#         native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
#         device_class=SensorDeviceClass.ENERGY,
#         state_class=SensorStateClass.TOTAL_INCREASING,
#     ),
#     SonnenBackupSensorEntityDescription(
#         key="consumption_average",
#         native_unit_of_measurement=UnitOfPower.WATT,
#         device_class=SensorDeviceClass.POWER,
#         state_class=SensorStateClass.MEASUREMENT,
#     ),
#     SonnenBackupSensorEntityDescription(
#         key="status_frequency",
#         default_value=0,
#         native_unit_of_measurement=UnitOfFrequency.HERTZ,
#         device_class=SensorDeviceClass.FREQUENCY,
#         state_class=SensorStateClass.MEASUREMENT,
#     #    entity_registry_enabled_default=False,
#     ),
    # SonnenBackupSensorEntityDescription(
    #     key="current_ac",
    #     default_value=0,
    #     native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
    #     device_class=SensorDeviceClass.CURRENT,
    #     state_class=SensorStateClass.MEASUREMENT,
    # ),
    # SonnenBackupSensorEntityDescription(
    #     key="current_dc",
    #     default_value=0,
    #     native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
    #     device_class=SensorDeviceClass.CURRENT,
    #     state_class=SensorStateClass.MEASUREMENT,
    # ),
    # SonnenBackupSensorEntityDescription(
    #     key="current_dc_2",
    #     default_value=0,
    #     native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
    #     device_class=SensorDeviceClass.CURRENT,
    #     state_class=SensorStateClass.MEASUREMENT,
    # ),
    # SonnenBackupSensorEntityDescription(
    #     key="power_ac",
    #     default_value=0,
    #     native_unit_of_measurement=UnitOfPower.WATT,
    #     device_class=SensorDeviceClass.POWER,
    #     state_class=SensorStateClass.MEASUREMENT,
    # ),
    # SonnenBackupSensorEntityDescription(
    #     key="voltage_ac",
    #     default_value=0,
    #     native_unit_of_measurement=UnitOfElectricPotential.VOLT,
    #     device_class=SensorDeviceClass.VOLTAGE,
    #     state_class=SensorStateClass.MEASUREMENT,
    #     entity_registry_enabled_default=False,
    # ),
    # SonnenBackupSensorEntityDescription(
    #     key="voltage_dc",
    #     default_value=0,
    #     native_unit_of_measurement=UnitOfElectricPotential.VOLT,
    #     device_class=SensorDeviceClass.VOLTAGE,
    #     state_class=SensorStateClass.MEASUREMENT,
    # ),
    # SonnenBackupSensorEntityDescription(
    #     key="voltage_dc_2",
    #     default_value=0,
    #     native_unit_of_measurement=UnitOfElectricPotential.VOLT,
    #     device_class=SensorDeviceClass.VOLTAGE,
    #     state_class=SensorStateClass.MEASUREMENT,
    # ),
    # device status entities
    # SonnenBackupSensorEntityDescription(
    #     key="system_status",
    #     entity_category=EntityCategory.DIAGNOSTIC,
    # ),
    # SonnenBackupSensorEntityDescription(
    #     key="system_status_timestamp",
    #     entity_category=EntityCategory.DIAGNOSTIC,
    #     device_class=SensorDeviceClass.TIMESTAMP,
#        entity_registry_enabled_default=False,
    # ),
    # SonnenBackupSensorEntityDescription(
    #     key="error_message",
    #     response_key="error_code",
    #     entity_category=EntityCategory.DIAGNOSTIC,
    #     device_class=SensorDeviceClass.ENUM,
    #     options=list(dict.fromkeys(BATTERY_ERROR_CODES.values())),
    #     value_fn=BATTERY_ERROR_CODES.get,  # type: ignore[arg-type]
    # ),
#     SonnenBackupSensorEntityDescription(
#         key="battery_activity_state",
#         entity_category=EntityCategory.DIAGNOSTIC,
# #        entity_registry_enabled_default=False,
#     ),
    # SonnenBackupSensorEntityDescription(
    #     key="status_message",
    #     response_key="status_code",
    #     entity_category=EntityCategory.DIAGNOSTIC,
    #     device_class=SensorDeviceClass.ENUM,
    #     options=[opt.value for opt in InverterStatusCodeOption],
    #     value_fn=get_inverter_status_message,
    # ),
    # SonnenBackupSensorEntityDescription(
    #     key="led_state",
    #     entity_category=EntityCategory.DIAGNOSTIC,
    #     entity_registry_enabled_default=False,
    # ),
    # SonnenBackupSensorEntityDescription(
    #     key="led_color",
    #     entity_category=EntityCategory.DIAGNOSTIC,
    #     entity_registry_enabled_default=False,
    # ),
# ]

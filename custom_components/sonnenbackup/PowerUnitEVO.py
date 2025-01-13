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
            "configuration_em_operatingmode": (0, Units.NONE, "operating_mode", cls._decode_operating_mode),
            "status_backup_buffer": (1, Units.PERCENT),
            "last_configurations": (2, Units.NONE, None, cls._format_datetime),
            "system_status": (3, Units.NONE),
            "system_status_timestamp": (4, Units.NONE, "status_timestamp", cls._format_datetime),
            "battery_activity_state": (5, Units.NONE, "sonnenbackup_state"),
            "fully_charged_at": (6, Units.NONE, None, cls._format_datetime),
            "fully_discharged_at": (7, Units.NONE, None, cls._format_datetime),
            "battery_cycle_count": (8, Units.NONE),
            "battery_full_charge_capacity_wh":(9, BatteryCapacity, "full_charge_capacity"),
            "battery_remaining_capacity_wh":(10, BatteryCapacity, "remaining_capacity"),
            "capacity_until_reserve":(11, BatteryCapacity),
            "backup_reserve_at": (12, Units.NONE),
            "backup_buffer_capacity_wh":(13, BatteryCapacity, "backup_reserve_capacity"),
            "kwh_consumed": (14, Units.KWH),
            "kwh_produced": (15, Units.KWH),
            "consumption_average" : (16, Units.W),
            "status_frequency": (17, Units.HZ, "frequency"),
            "status_battery_charging": (18, Units.NONE, "charging"),
            "status_battery_discharging": (19, Units.NONE, "discharging"),
            "status_rsoc": (20, Units.PERCENT, "relative_state_of_charge"),
            "status_usoc": (21, Units.PERCENT, "usable_state_of_charge"),
            # "Total Yield": (pack_u16(22, 23), Total(Units.KWH), div10),
            # "Daily Yield": (24, DailyTotal(Units.KWH), div10),
            # "Feed-in Power ": (pack_u16(72, 73), Units.W, to_signed32),
            # "Total Feed-in Energy": (pack_u16(74, 75), Total(Units.KWH), div100),
            # "Total Consumption": (pack_u16(76, 77), Total(Units.KWH), div100),
        }

@dataclass(frozen=True)
class SonnenBackupSensorEntityDescription(SensorEntityDescription):
    """Describes SonnenBackup sensor entity."""

    default_value: StateType | None = None
    invalid_when_falsy: bool = False
    response_key: str | None = None
#    value_fn: Callable[[StateType], StateType] | None = None


@classmethod
def battery_sensors(cls) -> dict:
    """sonnen_api_v2 properties used as sensor values"""

    return BATTERY_ENTITY_DESCRIPTIONS


BATTERY_ENTITY_DESCRIPTIONS: list[SonnenBackupSensorEntityDescription] = [
    SonnenBackupSensorEntityDescription(
        key="kwh_produced",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SonnenBackupSensorEntityDescription(
        key="kwh_consumed",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SonnenBackupSensorEntityDescription(
        key="consumption_average",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SonnenBackupSensorEntityDescription(
        key="status_frequency",
        default_value=0,
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
    #    entity_registry_enabled_default=False,
    ),
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
    SonnenBackupSensorEntityDescription(
        key="system_status",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
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
    SonnenBackupSensorEntityDescription(
        key="battery_activity_state",
        entity_category=EntityCategory.DIAGNOSTIC,
#        entity_registry_enabled_default=False,
    ),
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
]

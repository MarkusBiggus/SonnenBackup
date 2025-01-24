""" Units and different measurement types"""

from enum import Enum
from typing import NamedTuple, Union


class Units(Enum):
    """All known Units."""

    W = "W"
    KWH = "kWh"
    WH = "Wh"
    A = "A"
    V = "V"
    C = "°C"
    HZ = "Hz"
    PERCENT = "%"
    NONE = ""


class Measurement(NamedTuple):
    """Representation of measurement with a given unit and arbitrary values."""

    unit: Units
    is_monotonic: bool = False
    resets_daily: bool = False
    storage: bool = False


class Total(Measurement):
    """A Measurement where the values are continuously increasing."""

    is_monotonic: bool = True


class TotalKWH(Measurement):
    """A Measurement where the kWh value is continuously increasing."""

    unit: Units = Units.KWH
    is_monotonic: bool = True


class DailyTotal(Measurement):
    """A Measurement where the values are reset daily."""

    is_monotonic: bool = False
    resets_daily: bool = True

class DailyTotalW(Measurement):
    """A Measurement where the Watt values are reset daily."""

    unit: Units = Units.W
    is_monotonic: bool = False
    resets_daily: bool = True

class BatteryCapacity(Measurement):
    """A percent Measurement of Battery Capacity."""

    unit: Units = Units.WH
    is_monotonic: bool = False
    storage: bool = True

SensorUnit = Union[Measurement, TotalKWH, DailyTotalW, BatteryCapacity] #, Total, DailyTotal

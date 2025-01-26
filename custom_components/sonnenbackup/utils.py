""" Utility for processing battery response to sensor values"""

from numbers import Number
from typing import List, Protocol, Tuple

from voluptuous import Invalid
from string import Formatter
from datetime import timedelta, datetime
import tzlocal


# class Packer(Protocol):  # pragma: no cover
#     # pylint: disable=R0903
#     """
#     Pack multiple raw values from the inverter
#      data into one raw value
#     """

#     def __call__(self, *vals: float) -> float: ...


# PackerBuilderResult = Tuple[Tuple[int, ...], Packer]


# class PackerBuilder(Protocol):  # pragma: no cover
#     # pylint: disable=R0903
#     """
#     Build a packer by identifying the indexes of the
#     raw values to be fed to the packer
#     """

#     def __call__(self, *indexes: int) -> PackerBuilderResult: ...


# def __u16_packer(*values: float) -> float:
#     accumulator = 0.0
#     stride = 1
#     for value in values:
#         accumulator += value * stride
#         stride *= 2**16
#     return accumulator


# def pack_u16(*indexes: int) -> PackerBuilderResult:
#     """
#     Some values are expressed over 2 (or potentially
#     more 16 bit [aka "short"] registers). Here we combine
#     them, in order of least to most significant.
#     """
#     return (indexes, __u16_packer)


def startswith(something):
    def inner(actual):
        if isinstance(actual, str):
            if actual.startswith(something):
                return actual
        raise Invalid(f"{str(actual)} does not start with {something}")

    return inner


def div10(val):
     return val / 10

def div100(val):
     return val / 100

def div1K(val):
    return val / 1000

# INT16_MAX = 0x7FFF
# INT32_MAX = 0x7FFFFFFF


# def to_signed(val):
#     if val > INT16_MAX:
#         val -= 2**16
#     return val


# def to_signed32(val):
#     if val > INT32_MAX:
#         val -= 2**32
#     return val


# def twoway_div10(val):
#     return to_signed(val) / 10


# def twoway_div100(val):
#     return to_signed(val) / 100


# def to_url(host, port):
#     return f"http://{host}:{port}/"


def contains_none_zero_value(value: List[Number]):
    """Validate that at least one element is not zero.
    Args:
        value (List[Number]): list to validate
    Raises:
        Invalid: if all elements are zero
    """

    if isinstance(value, list):
        if len(value) != 0 and any((v != 0 for v in value)):
            return value
    raise Invalid("All elements in the list are zero: {value}")


def strfdelta(tdelta: int | timedelta | datetime, fmt='{D:01}d {H:02}:{M:02}:{S:02}', inputtype:str = 's'):
    """Convert a datetime.timedelta object or a regular number to a custom-
    formatted string, just like the stftime() method does for datetime.datetime
    objects.
    A datetime object will calculate seconds from now to the datetime provided.

    The fmt argument allows custom formatting to be specified.  Fields can
    include seconds, minutes, hours, days, and weeks.  Each field is optional.

    Some examples:
        '{D:01}d {H:02}:{M:02}:{S:02}' --> '5d 08:04:02' (default)
        '{D:01}d {H:02}h {M:02}m {S:02}s' --> '5d 08h 04m 02s'
        '{W}w {D}d {H}:{M:02}:{S:02}'     --> '4w 5d 8:04:02'
        '{D:2}d {H:2}:{M:02}:{S:02}'      --> ' 5d  8:04:02'
        '{H}h {S}s'                       --> '72h 800s'

    The inputtype argument allows tdelta to be a regular number instead of the
    default, which is a datetime.timedelta object.  Valid inputtype strings:
        's', 'seconds',
        'm', 'minutes',
        'h', 'hours',
        'd', 'days',
        'w', 'weeks'
    """
    WEEK_SECONDS = 604800
    DAY_SECONDS = 86400
    HOUR_SECONDS = 3600
    MINUTE_SECONDS = 60
    FORMAT_UNITS = {'W': WEEK_SECONDS, 'D': DAY_SECONDS, 'H': HOUR_SECONDS, 'M': MINUTE_SECONDS, 'S': 1}

    sign=''
    # Convert tdelta to integer seconds.
    if isinstance(tdelta, timedelta):
        remainder = int(tdelta.total_seconds())
    elif isinstance(tdelta, datetime):
        '''this bit doesn't work
            - datetime has huge problems with negatives and/or timezones.
        '''
        tz = tdelta.tzinfo
        if tz is None:
            now = datetime.now() # naive
        else:
            now = datetime.now(tz) # aware
    #        print(f"now:{datetime.now(tz)}")
    #    print(f"tdelta:{tdelta}")
        delta = tdelta - now
        remainder = int(delta.total_seconds())
    #    print (f'seconds: {remainder} ')
        return strfdelta(remainder, fmt)

    elif type(tdelta) is int:
        if tdelta < 0:
            sign = '-'
            tdelta = abs(tdelta)
        if inputtype.lower() in ['s', 'seconds']:
            remainder = tdelta
        elif inputtype.lower() in ['m', 'minutes']:
            remainder = tdelta * MINUTE_SECONDS
        elif inputtype.lower() in ['h', 'hours']:
            remainder = tdelta * HOUR_SECONDS
        elif inputtype.lower() in ['d', 'days']:
            remainder = tdelta * DAY_SECONDS
        elif inputtype.lower() in ['w', 'weeks']:
            remainder = tdelta * WEEK_SECONDS
        else:
            raise ValueError (f"Wrong inputtype! {inputtype} is not one of: 'W' | 'D' | 'H' | 'M' | 'S'")
    else:
        raise ValueError (f'Wrong tdelta type! {type(tdelta)} is not one of: int | timedelta | datetime')


    fmtr = Formatter()
    desired_fields = [field_tuple[1] for field_tuple in fmtr.parse(fmt)]
    possible_fields = ('W', 'D', 'H', 'M', 'S')
    values = {}
    for field in possible_fields:
        if field in desired_fields and field in FORMAT_UNITS:
#            print(f"remain:{remainder}  field:{field}  unit:{FORMAT_UNITS[field]}  divmod:{divmod(remainder, FORMAT_UNITS[field])}")
            values[field], remainder = divmod(remainder, FORMAT_UNITS[field])
    return sign+fmtr.format(fmt, **values)
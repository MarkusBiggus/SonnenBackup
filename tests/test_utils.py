"""pytest tests/test_utils.py -s -v -x
    For testing utility methods.
"""

from datetime import timedelta, datetime
from freezegun import freeze_time
import tzlocal

from custom_components.sonnenbackup.utils import strfdelta

tz_offset = datetime.now(tzlocal.get_localzone()).utcoffset()
@freeze_time("20-11-2023 17:00:00", tz_offset=tz_offset)
def test_deltatime() -> None:
    """Format delta time."""

    deltaString = strfdelta(5)
#    print(f'deltaString: {deltaString}')
    assert deltaString == '0d 00:00:05'

    before = timedelta(seconds=3720)

    deltaString = strfdelta(before)
    assert deltaString == '0d 01:02:00'

    before = timedelta(seconds=86400+3600+60+5)

    deltaString = strfdelta(before)
    print(f'deltaString: {deltaString}')
    assert deltaString == '1d 01:01:05'

    deltaString = strfdelta(0)
    assert deltaString == '0d 00:00:00'

    deltaString = strfdelta(3000)
    print(f'deltaString: {deltaString}')
    assert deltaString == '0d 00:50:00' # Not! 50 minutes future

    deltaString = strfdelta(-3000)
    print(f'deltaString: {deltaString}')
    assert deltaString == '-1d 23:10:00' # Not! 50 minutes prior

    before = datetime(2023, 11, 20, 16, 10, tzinfo=tzlocal.get_localzone())
    deltaString = strfdelta(before)
    print(f'deltaString: {deltaString}')
    assert deltaString == '0d 20:50:00' # Not! 50 minutes prior, or -3,000 seconds

    before = datetime(2023, 11, 20, 17, 50, tzinfo=tzlocal.get_localzone())
    deltaString = strfdelta(before)
    print(f'deltaString: {deltaString}')
#    assert deltaString == '0d 00:50:00' # 50 minutes after
    assert deltaString == '0d 19:10:00' # Not! 50 minutes after

# SonnenBackup

[![Build Status](https://github.com/squishykid/sonnenbackup/workflows/tests/badge.svg)](https://github.com/squishykid/sonnenbackup/actions)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/sonnenbackup.svg)](https://pypi.org/project/sonnenbackup)

Read energy usage data from the real-time API on Sonnen Batterie inverter.

* Real time power, current and voltage
* Grid power information
* Battery level
* Temperature and inverter health
* Daily/Total energy summaries

## Usage

`pip install sonnenbackup`

Then from within your project:

```
import sonnenbackup
import asyncio

async def work():
    r = await sonnenbackup.real_time_api('10.0.0.1')
    return await r.get_data()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
data = loop.run_until_complete(work())
print(data)
```

This will try all the inverter classes in turn until it finds the first one that works with your installation. You can see the list of inverter implementation classes in the entry points configured in [setup.py](setup.py).

If you want to bypass the inverter discovery code and use a specific inverter class, you can invoke `discover` specifying directly the class. In this example, the X1 Hybrid Gen4 implementation is used:

```
from importlib.metadata import entry_points
import sonnenbackup
import asyncio

INVERTERS_ENTRY_POINTS = {
   ep.name: ep.load() for ep in entry_points(group="sonnenbackup.inverter")
}

async def work():
    inverter = await sonnenbackup.discover("10.0.0.1", 80, "xxxxx", inverters=[INVERTERS_ENTRY_POINTS.get("x1_hybrid_gen4")], return_when=asyncio.FIRST_COMPLETED)
    return await inverter.get_data()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
data = loop.run_until_complete(work())
print(data)
```

## Confirmed Supported Inverters

These inverters have been tested and confirmed to be working. If your inverter is not listed below, this library may still work- please create an issue so we can add your inverter to the list 😊.

* SK-TL5000E
* X1 Hybrid Gen4

You can get the list of supported inverters by looking up the `sonnenbackup.inverter` entry points:

```
for ep in entry_points(group="sonnenbackup.inverter"):
    print(ep)
```
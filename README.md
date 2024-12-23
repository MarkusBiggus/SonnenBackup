# SonnenBackup

Read energy usage data from the real-time API on Sonnen Batterie batterie.

* Real time power, current and voltage
* Grid power information
* Battery level
* Temperature and batterie health
* Daily/Total energy summaries

## Usage

`pip install sonnenbackup`

Then from within your project:

```
from sonnen_api_v2 import BatterieBackup, BatterieResponse,
import asyncio

async def work():
    _batterie = await BatterieBackup(auth_token, ip_address, port)
    return await _batterie.get_response()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
data = loop.run_until_complete(work())
print(data)
```

## Confirmed Supported Batterie

These batteries have been tested and confirmed to be working. If your batterie is not listed below, this library may still work provided your battery admin portal can generate an API read token and responds to Sonnen API V2 endpoints.

* Power unit Evo IP56
